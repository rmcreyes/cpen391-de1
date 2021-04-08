#include "rfs.h"
#include "bt.h"
#include <string.h>

#define BT_BUF_SIZE 128

const char * confirm_str = "CONFIRM,";
const char * ok_done_str = "OK,DONE,";
const char * ok_leave_str = "OK,LEAVE";
const char * ok_user_str = "OK,USER,";
const char * ok_not_user_str = "OK,NOTUSER,";

char bt_send_buf[BT_BUF_SIZE];

void sendBTLine(char * str) {
    char * c;
    for(c = str; *c != 0; c++){
        putcharBT(*c);
    }
    putcharBT('\r');
    putcharBT('\n');
    memset(bt_send_buf, 0, BT_BUF_SIZE);
}

int receiveBTLine(char * buf, int bufSize) {
    char * c = buf;
    int i = 0;
    do {
        *c = getcharBT();
        if (*c == '\r')
            break;
        c++;
    } while(1);
    *c = 0;
    BTFlush();
    return i;
}

int confirm_BT(char * plate, char * buf, int bufSize) {
    strcat(bt_send_buf, confirm_str);
    strcat(bt_send_buf, plate);
    sendBTLine(bt_send_buf);
    return receiveBTLine(buf,bufSize);
}

int ok_done(char * plate, char * buf, int bufSize) {
    strcat(bt_send_buf, ok_done_str);
    strcat(bt_send_buf, plate);
    sendBTLine(bt_send_buf);
    return 0;
}

int ok_user(char * plate, char * buf, int bufSize, int isUser){
    if(isUser)
        strcat(bt_send_buf, ok_user_str);
    else
        strcat(bt_send_buf, ok_not_user_str);
    strcat(bt_send_buf, plate);
    sendBTLine(bt_send_buf);
    if(isUser)
        return 0;
    return receiveBTLine(buf,bufSize);
}

int ok_leave() {
    strcat(bt_send_buf, ok_leave_str);
    sendBTLine(bt_send_buf);
    return 0;
}