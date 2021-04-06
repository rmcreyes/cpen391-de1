#ifndef _BT_
#define _BT_
void sendBTLine(char * str);
int confirm_BT(char * plate, char * buf, int bufSize);
int ok_done(char * plate, char * buf, int bufSize);
int ok_leave();
int ok_user(char * plate, char * buf, int bufSize);
#endif