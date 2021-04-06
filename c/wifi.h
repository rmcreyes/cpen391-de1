#ifndef _WIFI_
#define _WIFI_
int confirm_wifi(char * id, char * plate, char * buf, int bufSize, int correct);
int notify(char * plate, char * buf, int bufSize, int parked);
int initWifi();
int reset_meter(char * buf, int bufSize);
int send_payment(char * parking_id, char * card_num, char * exp, char * cvv, char * buf, int bufSize);
#endif