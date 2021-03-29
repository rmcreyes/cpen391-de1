#include <stdio.h>
#include <stdlib.h>
#include "nn.h"
#include <time.h>
#include <string.h>


#define IMAGE_SIZE 784
#define L1_SIZE 256
#define L2_SIZE 256
#define L3_SIZE 36


int * nn;
int * in;

// Expected argument format: nn.bin, ImageSize(# of ints), L1 Size(# of ints), L2 Size(# of ints), L3 Size (# of ints)

int main(int argc, char ** argv) {

    if (argc < 2) {
    printf("No argument to NN file\n");
    return 0;
    }

    FILE *nnFile = fopen(argv[1], "rb");
    if (!nnFile) {
    printf("Couldn't open NN file\n");
    return 0;
    }
    if (fseek(nnFile, 0, SEEK_END)) {
    printf("Couldn't seek until end of file\n");
    return 0;
    }
    long nnSize = ftell(nnFile);
    if (fseek(nnFile, 0, SEEK_SET)){
    printf("Couldn't go back to beginning of file\n");
    return 0;
    }

    nn = malloc(nnSize);
    fread(nn, sizeof(int), nnSize/sizeof(int), nnFile);
    fclose(nnFile);

    if(init_accel(nn, atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]))) {
        printf("Couldn't init accel");
        return 0;
    }

    char imageName[100];

    while(1) {
        printf("Enter the image name:");
        scanf("%s", imageName);
        FILE * imageFile = fopen(imageName, "rb");
        if(!imageFile) {
        printf("Couldn't open image file\n");
        continue;
        }
        if (fseek(imageFile, 0, SEEK_END)) {
        printf("Couldn't seek until end of file\n");
        continue;
        }
        long imageSize = ftell(imageFile);
        if (fseek(imageFile, 0, SEEK_SET)){
        printf("Couldn't go back to beginning of file\n");
        continue;
        }

        in = malloc(imageSize);
        fread(in, sizeof(int), imageSize/sizeof(int), imageFile);
        fclose(imageFile);

        float start = (float)clock()/CLOCKS_PER_SEC;
        int res = run(in);
        float end = (float)clock()/CLOCKS_PER_SEC;
        float timeElapsed = end - start;
        printf("Result: %d, Took: %f seconds\n", res, timeElapsed);
    }
    return 0;
}