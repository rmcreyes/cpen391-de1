#include "rfs.h"
#include "bt.h"
#include "wifi.h"
#include <stdio.h>

int main(int argc, char ** argv){
    Init_RFS();
    char ret[100];
    confirm_BT(argv[1],ret,100);
    printf("%s",ret);
}