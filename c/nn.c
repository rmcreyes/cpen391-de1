#define DOT_BASE 0x80
#define WRITE_OFF 0x0
#define READ_OFF 0x0
#define WEIGHT_OFF 0x2
#define INPUT_OFF 0x3
#define LENGTH 0x5

#define MEM_BASE 0xC0001000 
#define FPGA_MEM_BASE MEM_BASE - 0xC0000000
#define MEM_SIZE 1024 * 1024 * 20

#define DOT 0xFF202000
#define DOT_SIZE 0x4 * 0xF

#define FPGA_SRAM0 0x8000000
#define HPS_SRAM0 0xC0000000 + FPGA_SRAM0
#define SRAM_SIZE 0x1000

#define FPGA_SRAM1 FPGA_SRAM0 + SRAM_SIZE
#define HPS_SRAM1 0xC0000000 + FPGA_SRAM1


#include "mapping.h"
#include <string.h>
#include "nn.h"

#define SW 0
#define SRAM 1

int *sram0;
int sram_addr0;

int *sram1;
int sram_addr1;

int *nn;
int *l1;
int *l2;
int *l3;
int *init_addr;
int *input;
int * mem_base;
int * dot_base;

int fd = -1;

int* l1_bias;
int* l1_weight;
int* l2_bias;
int* l2_weight;
int* l3_bias;
int* l3_weight;

int l1_size_glb;
int l2_size_glb;
int l3_size_glb;
int image_size;
int size;


int l1_b_addr;
int l1_w_addr;
int l1_addr;

int l2_b_addr;
int l2_w_addr;
int l2_addr;

int l3_b_addr;
int l3_w_addr;
int l3_addr;

int in_addr;


int init_accel(int *nn_in, int in_size, int l1_size, int l2_size, int l3_size) {
    image_size = in_size;
    l1_size_glb = l1_size;
    l2_size_glb = l2_size;
    l3_size_glb = l3_size;

    fd = open_physical(fd);
    if (fd < 0) {
        return -1;
    }
    
    nn = map_physical(fd, MEM_BASE, MEM_SIZE);
    dot_base = (int*) map_physical(fd, DOT, DOT_SIZE + DOT_BASE) + DOT_BASE / sizeof(int);
    sram0 = (int*) map_physical(fd, HPS_SRAM0, 2 * SRAM_SIZE);
    sram1 = sram0 + SRAM_SIZE / sizeof(int);

    sram_addr0 = FPGA_SRAM0;
    sram_addr1 = FPGA_SRAM1;


    l1_bias = nn;
    l1_weight = l1_bias + l1_size;

    l2_bias = l1_weight + in_size * l1_size;
    l2_weight = l2_bias + l2_size;

    l3_bias = l2_weight + l1_size * l2_size;
    l3_weight = l3_bias + l3_size;

    

    size = l1_size + (in_size * l1_size) + l2_size + (l1_size * l2_size) + l3_size + (l2_size * l3_size);
    l1 = nn + size + 0x100;
    l2 = l1 + l1_size + 0x100;
    l3 = l2 + l2_size + 0x100;


    l1_b_addr = FPGA_MEM_BASE;
    l1_w_addr = l1_b_addr + l1_size * sizeof(int);
    l1_addr = FPGA_MEM_BASE + sizeof(int) * (size+0x100);

    l2_b_addr = l1_w_addr + sizeof(int) * (in_size * l1_size);
    l2_w_addr = l2_b_addr + sizeof(int) * l2_size;
    l2_addr = l1_addr + sizeof(int) * (l1_size+0x100);

    l3_b_addr = l2_w_addr + sizeof(int) * (l1_size * l2_size);
    l3_w_addr = l3_b_addr + sizeof(int) * l3_size;
    l3_addr = l2_addr + sizeof(int) * (l2_size+0x100);

    input = l3 + (l2_size * l3_size) + 0x100;
    in_addr = l3_addr + sizeof(int) * ((l2_size * l3_size) + 0x100);
    

    for (int i = 0; i < size; i++) {
        nn[i] = nn_in[i];
    }

    return 0;
}

// Hardware dot product
int dot(int vec1, int vec2, int row_len) {
    *(dot_base + 2) = (unsigned) vec1;
    *(dot_base + 3) = (unsigned) vec2;
    *(dot_base + 5) = (unsigned) row_len;
    *dot_base = 5;
    return *dot_base;
}

// Software dot product. Used for testing.
int dot_sw(volatile int* vec1, volatile int* vec2, int row_len) {
    int sum = 0;
    for (unsigned i = 0; i < row_len; ++i) {
        sum += (int) (((long long) vec1[i] * (long long) vec2[i]) >> 16);
    }
    return sum;
}

// Apply a layer in software. Used for testing.
void layer_sw(volatile int* in, volatile int* out, volatile int* weight, volatile int* bias, int row_len, int out_len, int relu) {
    int sum;
    for (int i = 0; i < out_len; i++, weight += row_len) {
        sum = bias[i] + dot_sw(in, weight, row_len);
        if (relu) {
            sum = sum < 0 ? 0 : sum;
        }
        out[i] = sum;
    }
}

// Apply a layer in hardware.
void layer_hw(int in, int* out, int weight, int* bias, int row_len, int out_len, int relu) {
    int sum;
    for (int i = 0; i < out_len; i++, weight += row_len * sizeof(int)) {
        sum = bias[i] + dot(in, weight, row_len);
        if (relu) {
            sum = sum < 0 ? 0 : sum;
        }
        out[i] = sum;
    }
}

// Free resources for the HW accelerator.
int destroy_accel() {
    int err;
    err  = unmap_physical(mem_base, MEM_SIZE);
    if (!err)
        goto fail;
    err = unmap_physical(dot_base, DOT_SIZE + DOT_BASE);
    if (!err)
        goto fail;
    close_physical(fd);
    return 0;
    fail:
        return -1;
}

// Find the max index in an array.
int max(volatile int* arr, int size) {
    int max = 0;
    for (int i = 0; i < size; i++) {
        if(arr[i] > arr[max]) 
            max = i;
    }
    return max;
}


// Runs the ML algorithm.
// in: the input data
// returns: the result. Numerial numbers are just their decimal representation. Alphabet characters start from 10.
int run(int *in) {

    #if SW
        layer_sw(in, l1, l1_weight, l1_bias, image_size, l1_size_glb, 1);
        layer_sw(l1, l2, l2_weight, l2_bias, l1_size_glb, l2_size_glb, 1);
        layer_sw(l2, l3, l3_weight, l3_bias, l2_size_glb, l3_size_glb, 0);
    #else
        #if SRAM
            for (int i = 0; i < image_size; i++) {
                sram0[i] = in[i];
            }   
            layer_hw(sram_addr0, sram1, l1_w_addr, l1_bias, image_size, l1_size_glb, 1);
            layer_hw(sram_addr1, sram0, l2_w_addr, l2_bias, l1_size_glb, l2_size_glb, 1);
            layer_hw(sram_addr0, sram1, l3_w_addr, l3_bias, l2_size_glb, l3_size_glb, 0);
            return max(sram1, l3_size_glb);
        #else
            for (int i = 0; i < image_size; i++) {
                input[i] = in[i];
            }   
            layer_hw(in_addr, l1, l1_w_addr, l1_bias, image_size, l1_size_glb, 1);
            layer_hw(l1_addr, l2, l2_w_addr, l2_bias, l1_size_glb, l2_size_glb, 1);
            layer_hw(l2_addr, l3, l3_w_addr, l3_bias, l2_size_glb, l3_size_glb, 0);
        #endif
    #endif

    return max(l3, l3_size_glb);
    
}