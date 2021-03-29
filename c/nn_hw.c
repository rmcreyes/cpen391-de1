/*
 *
 *
 *
 *
 *
 *
 * WARNING
 *
 *
 * Much of this code has been modified from it's prior version.
 *
 * The prior version (visible in git history) was tested. This version has not been tested.
 *
 *
 *
 *
 *
 *
 */


#include <stdio.h>
#include <stdlib.h>

#define L1_IN  784
#define L1_OUT 256
#define L2_IN L1_OUT
#define L2_OUT 256
#define L3_IN L2_OUT
#define L3_OUT 36
#define NPARAMS (L1_OUT + L1_IN * L1_OUT + L2_OUT + L2_IN * L2_OUT + L3_OUT + L3_IN * L3_OUT)
#define DOT_OFFSET 0x80

/* normally these would be contiguous but it's nice to know where they are for debugging */
int *nn     ; /* neural network biases and weights */
int *input  ; /* input image */
int *l1_acts; /* activations of layer 1 */
int *l2_acts; /* activations of layer 2 */
int *l3_acts; /* activations of layer 3 (outputs) */

// note: at most one of the 3 options below should be 1
// if multiples are set to 1, the topmost takes priority
// if all are set to 0, no accelerator is used (pure software)
#define DO_TASK7 0
#define DO_TASK6 0
#define DO_TASK5 0


// ----------------------------------------------------------------
// Two ways of computing dot product

// use software to compute the dot product of w[i]*ifmap[i]
// BASELINE
int dotprod_sw(int n_in,  int *w,  int *ifmap)
{
  int sum = 0;
  for (unsigned i = 0; i < n_in; ++i) { /* Q16 dot product */
      sum += (int) (((long long) w[i] * (long long) ifmap[i]) >> 16);
  }
  return sum;
}

// ----------------------------------------------------------------

// BASELINE, TASK5 and TASK6:  compute dot products
// optionally use accelerator to compute dot product only
void apply_layer_dot(int n_in, int n_out, int *b, int *w, int use_relu, int *ifmap, int *ofmap)
{
    for (unsigned o = 0, wo = 0; o < n_out; ++o, wo += n_in) {
        int sum = b[o]; /* bias for the current output index */
        sum += dotprod_sw( n_in, &w[wo], ifmap );
        if (use_relu) sum = (sum < 0) ? 0 : sum; /* ReLU activation */
        ofmap[o] = sum;
    }
}


// ----------------------------------------------------------------

int max_index(int n_in, int *ifmap)
{
    int max_sofar = 0;
    for( int i = 1; i < n_in; ++i ) {
        if( ifmap[i] > ifmap[max_sofar] ) max_sofar = i;
    }
    return max_sofar;
}


int main(int argc, char ** argv)
{

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


  int *l1_b = nn;                    /* layer 1 bias */
  int *l1_w = l1_b + L1_OUT;         /* layer 1 weights */
  int *l2_b = l1_w + L1_IN * L1_OUT; /* layer 2 bias */
  int *l2_w = l2_b + L2_OUT;         /* layer 2 weights */
  int *l3_b = l2_w + L2_IN * L2_OUT; /* layer 3 bias */
  int *l3_w = l3_b + L3_OUT;         /* layer 3 weights */

  int result;

  l1_acts = malloc(sizeof(int) * L1_OUT);
  l2_acts = malloc(sizeof(int) * L2_OUT);
  l3_acts = malloc(sizeof(int) * L3_OUT);

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

    input = malloc(imageSize);
    fread(input, sizeof(int), imageSize/sizeof(int), imageFile);
    fclose(imageFile);
    apply_layer_dot( L1_IN, L1_OUT, l1_b, l1_w, 1,   input, l1_acts );
    apply_layer_dot( L2_IN, L2_OUT, l2_b, l2_w, 1, l1_acts, l2_acts );
    apply_layer_dot( L3_IN, L3_OUT, l3_b, l3_w, 0, l2_acts, l3_acts );
    result = max_index( L3_OUT, l3_acts );
    printf("%d\n", result);
    free(input);
  }
  return 0;
}
