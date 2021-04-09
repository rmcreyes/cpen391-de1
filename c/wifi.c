#include "rfs.h"
#include "wifi.h"
#include <unistd.h>
#include <string.h>

#define MS_TO_US 1000
#define MAX_BUF 100

char * exec = "dofile(\"send_http_requests.lua\")";
char send_buf[MAX_BUF];

const char * parked_func = "OCCUPIED,";
const char * left_func = "LEFT,";
const char * correct = "CORRECT,";
const char * incorrect = "INCORRECT,";
const char * reset_str = "RESET";
const char * send_payment_str = "PAYMENT,";
const char * quit = "QUIT";

// DO NOT INCLUDE \r\n in your payload.
void send_str(char * str) {
    char * c;
    for(c = str; *c != 0; c++){
        putcharRS232(*c);
    }
    putcharRS232('\r');
    putcharRS232('\n');
}

int receiveLine(char * buf, int bufSize) {
    char * c = buf;
    int i = 0;
    do {
        *c = getcharRS232();
        if (*c == '\n')
            break;
        c++;
    } while(1);
    *c = 0;
    RS232Flush();
    return i;
}

char * craft_notify(char * plate) {
    strcat(send_buf, plate);
    return send_buf;
}

char * craft_park(char * plate) {
    strcat(send_buf, parked_func);
    return craft_notify(plate);
}

char * craft_left(char * plate) { 
    strcat(send_buf, left_func);
    return craft_notify(plate);
}

char * craft_confirm(char * id, char * plate) {
    strcat(send_buf, id);
    strcat(send_buf, ",");
    strcat(send_buf, plate);
    return send_buf;
}

char * craft_correct(char * id, char * plate){
    strcat(send_buf, correct);
    return craft_confirm(id, plate);
}

char * craft_incorrect(char * id, char * plate){
    strcat(send_buf, incorrect);
    return craft_confirm(id, plate);
}

int initWifi(){
    memset(send_buf, 0, MAX_BUF);
    send_str(exec);
    int c;
    while(c = getcharRS232(), c != '1' && c != '5');
    sleep(10);
    for(c = 0; c < 3; c++){
        reset_meter(0,0);
        sleep(1);
    }
    RS232Flush();
    return 0;
}

int notify(char * plate, char * buf, int bufSize, int parked) {
    int n = 0;
    if (parked)
        craft_park(plate);
    else
        craft_left(plate);
    send_str(send_buf);
    if (buf)
        n= receiveLine(buf, bufSize);
    memset(send_buf, 0, MAX_BUF);
    return n;
}


int confirm_wifi(char * id, char * plate, char * buf, int bufSize, int correct) {
    int n = 0;
    if (correct)
        craft_correct(id, plate);
    else
        craft_incorrect(id, plate);

    send_str(send_buf);
    if (buf)
        n = receiveLine(buf, bufSize);
    memset(send_buf, 0, MAX_BUF);
    return n;
}

int reset_meter(char * buf, int bufSize) {
    int n;
    strcat(send_buf, reset_str);
    send_str(send_buf);
    if (buf)
        n= receiveLine(buf, bufSize);
    memset(send_buf, 0, MAX_BUF);
    return n;
}

int send_payment(char * parking_id, char * card_num, char * exp, char * cvv, char * buf, int bufSize) {
    int n;
    strcat(send_buf, send_payment_str);
    strcat(send_buf, parking_id);
    strcat(send_buf, ",");
    strcat(send_buf, card_num);
    strcat(send_buf, ",");
    strcat(send_buf, exp);
    strcat(send_buf, ",");
    strcat(send_buf, cvv);
    send_str(send_buf);
    if (buf)
        n = receiveLine(buf, bufSize);
    memset(send_buf, 0, MAX_BUF);
    return n;
}

int close_wifi() {
    send_str(quit);
    memset(send_buf, 0, MAX_BUF);
    return 0;
}