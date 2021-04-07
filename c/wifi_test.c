#include <stdio.h>
#include "wifi.h"
#include "rfs.h"
#include <stdlib.h>

int main(int argc, char ** argv) {
    char * buf = calloc(100,1);
    Init_RFS();
    initWifi();
    notify(argv[1], buf, 100, 1);
    printf("Notify Park: %s\n", buf);
    return 0;
}