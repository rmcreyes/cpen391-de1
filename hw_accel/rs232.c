#include "mapping.h"
#include <stdio.h>

// #define RS232_ReceiverFifo       (*(volatile unsigned char *)(0xFF210200))
// #define RS232_TransmitterFifo    (*(volatile unsigned char *)(0xFF210200))
// #define RS232_InterruptEnableReg (*(volatile unsigned char *)(0xFF210202))
// #define RS232_InterruptIdentificationReg        (*(volatile unsigned char *)(0xFF210204))
// #define RS232_FifoControlReg                    (*(volatile unsigned char *)(0xFF210204))
// #define RS232_LineControlReg                    (*(volatile unsigned char *)(0xFF210206))
// #define RS232_ModemControlReg                   (*(volatile unsigned char *)(0xFF210208))
// #define RS232_LineStatusReg                     (*(volatile unsigned char *)(0xFF21020A))
// #define RS232_ModemStatusReg                    (*(volatile unsigned char *)(0xFF21020C))
// #define RS232_ScratchReg                        (*(volatile unsigned char *)(0xFF21020E))
// #define RS232_DivisorLatchLSB                   (*(volatile unsigned char *)(0xFF210200))
// #define RS232_DivisorLatchMSB                   (*(volatile unsigned char *)(0xFF210202))

#define IO_Base 0xFF210000
#define RS_Base (0x200)
#define RS_ReceiverBase (RS_Base + 0x0)
#define RS_TransmitterBase (RS_Base + 0x0)
#define RS_InterruptEnable (RS_Base + 0x2)
#define RS_InterruptIDBase (RS_Base + 0x4)
#define RS_FifoBase (RS_Base + 0x4)
#define RS_LineControlBase (RS_Base + 0x6)
#define RS_ModemControlBase (RS_Base + 0x8)
#define RS_LineStatusBase (RS_Base + 0xA)
#define RS_ModemStatusBase (RS_Base + 0xC)
#define RS_ScratchBase (RS_Base + 0xE)
#define RS_DivisorLSBBase (RS_Base + 0x0)
#define RS_DivisorMSBBase (RS_Base + 0x2)

volatile void * RS232;
volatile unsigned char * RS232_ReceiverFifo;
volatile unsigned char * RS232_TransmitterFifo;
volatile unsigned char * RS232_InterruptEnable;
volatile unsigned char * RS232_InterruptIdentificationReg;
volatile unsigned char * RS232_FifoControlReg; 
volatile unsigned char * RS232_LineControlReg; 
volatile unsigned char * RS232_ModemControlReg;
volatile unsigned char * RS232_LineStatusReg;  
volatile unsigned char * RS232_ModemStatusReg; 
volatile unsigned char * RS232_ScratchReg;     
volatile unsigned char * RS232_DivisorLatchLSB;
volatile unsigned char * RS232_DivisorLatchMSB;
int memFd = -1;


void initMap() {
    memFd = open_physical(memFd);
    RS232 = map_physical(memFd, IO_Base, 0x10);
    RS232_ReceiverFifo = RS232 + RS_ReceiverBase;
    RS232_TransmitterFifo = RS232 + RS_TransmitterBase;
    RS232_InterruptEnable = RS232 + RS_InterruptEnable;
    RS232_InterruptIdentificationReg = RS232 + RS_InterruptIDBase;
    RS232_FifoControlReg = RS232 + RS_FifoBase;
    RS232_LineControlReg = RS232 + RS_LineControlBase;
    RS232_ModemControlReg = RS232 + RS_ModemControlBase;
    RS232_LineStatusReg = RS232 + RS_LineStatusBase;
    RS232_ModemStatusReg = RS232 + RS_ModemStatusBase;
    RS232_ScratchReg = RS232 + RS_ScratchBase;
    RS232_DivisorLatchLSB = RS232 + RS_DivisorLSBBase;
    RS232_DivisorLatchMSB = RS232 + RS_DivisorMSBBase;
    close_physical(memFd);
}

void closeRS232(void) {
    unmap_physical(RS232, 0x10);
    close_physical(memFd);
}


void Init_RS232(void) {
    // set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
    // set Divisor latch (LSB and MSB) with correct value for required baud rate
    // set bit 7 of Line control register back to 0 and
    // program other bits in that reg for 8 bit data, 1 stop bit, no parity etc
    // Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
    // Now Clear all bits in the FiFo control registers
    *RS232_LineControlReg = 0x80;
    // 115200 Baud rate. Divisor = 27 = 0x1B
    *RS232_DivisorLatchLSB = 0x1B;
    *RS232_DivisorLatchMSB = 0x0;
    // 00xx0011 = 0x03
    *RS232_LineControlReg = 0x0;
    *RS232_LineControlReg =  0x03;
    *RS232_FifoControlReg = 0x06;
    *RS232_FifoControlReg = 0x0;
}

// the following function polls the UART to determine if any character
// has been received. It doesn't wait for one, or read it, it simply tests
// to see if one is available to read from the FIFO
int RS232TestForReceivedData(void) {
    // if *RS232_LineStatusReg bit 0 is set to 1
    //return TRUE, otherwise return FALSE
    return *RS232_LineStatusReg & 1;
}

int putcharRS232(int c) {
    // wait for Transmitter Holding Register bit (5) of line status register to be '1'
    // indicating we can write to the device
    // write character to Transmitter fifo register
    // return the character we printed
    while(!((*RS232_LineStatusReg >> 5) & 1));
    *RS232_TransmitterFifo = (char) c;
    return c;
}

int getcharRS232(void) {
    // wait for Data Ready bit (0) of line status register to be '1'
    // read new character from ReceiverFiFo register
    // return new character
    while(!RS232TestForReceivedData());
    return *RS232_ReceiverFifo;
}

//
// Remove/flush the UART receiver buffer by removing any unread characters
//
void RS232Flush(void) {
    // while bit 0 of Line Status Register == ‘1’
    // read unwanted char out of fifo receiver buffer
    while(RS232TestForReceivedData()){
        *RS232_ReceiverFifo;
    }
}

int main() {
    char input[50];
    char output[50];
    char * i;
    initMap();
    Init_RS232();

    while (1) {
        printf("Input: ");
        gets(input);
        for (i = input; *i != 0; i++) {
            putcharRS232(*i);
        }
        putcharRS232('\r');
        putcharRS232('\n');
        i = output;
        do {
            *i = getcharRS232();
            i++; 
        } while(RS232TestForReceivedData());
        *i = 0;
        printf("%s\n", output);
        RS232Flush();
    }
    return 0;
}