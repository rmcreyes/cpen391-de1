#ifndef _WIFI_
#define _WIFI_
int confirm_wifi(char * id, char * plate, char * buf, int bufSize, int correct);
int notify(char * plate, char * buf, int bufSize, int parked);
int initWifi();
#endif