#include <stdio.h>
#include "rfs.h"
#include "wifi.h"
#include <stdlib.h>

int main(int argc, char ** argv) {
    char * buf = calloc(100,1);
    char * id = calloc(100,1);
    Init_RFS();
    initWifi();
    notify(argv[1], buf, 100, 1);
    printf("Notify Park: %s\n", buf);
    notify(argv[1], buf, 100, 1);
    printf("Notify Park: %s\n", buf);
    notify(argv[1], buf, 100, 1);
    printf("Notify Park: %s\n", buf);
    printf("ID: ");
    gets(id);
    confirm_wifi(id, argv[1], buf, 100, 1);
    printf("Confirm: %s\n", buf);
    close_wifi();
    return 0;
}