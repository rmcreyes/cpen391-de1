#include "rs232.h"
#include <unistd.h>
#include <string.h>

#define MS_TO_US 1000
#define MAX_BUF 100

char * exec = "dofile(\"send_http_requests.lua\")";
char send_buf[MAX_BUF];

const char * parked_func = "notify_license_plate_occupied(\"";
const char * left_func = "notify_license_plate_left(\"";
const char * correct = "confirm_parking_correct_license_plate(\"";
const char * incorrect = "confirm_parking_incorrect_license_plate(\"";

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

    while(getcharRS232() != '\n');
    while(getcharRS232() != ' ');
    do {
        *c = getcharRS232();
        if (*c == '\r')
            break;
        c++;
    } while(1);
    *c = 0;
    RS232Flush();
    return i;
}

char * craft_notify(char * plate) {
    strcat(send_buf, plate);
    strcat(send_buf, "\")");
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
    strcat(send_buf, "\", \"");
    strcat(send_buf, plate);
    strcat(send_buf, "\")");
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
    int err = Init_RS232();
    if (err) {
        return err;
    }
    putcharRS232('\r');
    putcharRS232('\n');
    putcharRS232('\r');
    putcharRS232('\n');
    putcharRS232('\r');
    putcharRS232('\n');
    sleep(1);
    RS232Flush();
    send_str(exec);
    sleep(5);
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


int confirm(char * id, char * plate, char * buf, int bufSize, int correct) {
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