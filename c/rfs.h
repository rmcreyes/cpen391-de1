#ifndef _RFS
#define _RFS_
void Close_RFS(void);
int Init_RFS(void);

int RS232TestForReceivedData(void);
int putcharRS232(int c);
int getcharRS232(void);
void RS232Flush(void);

int BTTestForReceivedData(void);
int putcharBT(int c);
int getcharBT(void);
void BTFlush(void);

#endif