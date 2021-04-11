#ifndef _RS232_
#define _RS232_
void closeRS232(void);
int Init_RS232(void);
int RS232TestForReceivedData(void);
int putcharRS232(int c);
int getcharRS232(void);
void RS232Flush(void);

#endif