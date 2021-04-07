#include "mapping.h"
#include "rfs.h"
#include <stdio.h>
#include <unistd.h>

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


#define BT_Base (0x220)
#define BT_ReceiverBase (BT_Base + 0x0)
#define BT_TransmitterBase (BT_Base + 0x0)
#define BT_InterruptEnableReg (BT_Base + 0x2)
#define BT_InterruptIDBase (BT_Base + 0x4)
#define BT_FifoBase (BT_Base + 0x4)
#define BT_LineControlBase (BT_Base + 0x6)
#define BT_ModemControlBase (BT_Base + 0x8)
#define BT_LineStatusBase (BT_Base + 0xA)
#define BT_ModemStatusBase (BT_Base + 0xC)
#define BT_ScratchBase (BT_Base + 0xE)
#define BT_DivisorLSBBase (BT_Base + 0x0)
#define BT_DivisorMSBBase (BT_Base + 0x2)

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

volatile unsigned char * BT_ReceiverFifo;
volatile unsigned char * BT_TransmitterFifo;
volatile unsigned char * BT_InterruptEnable;
volatile unsigned char * BT_InterruptIdentificationReg;
volatile unsigned char * BT_FifoControlReg; 
volatile unsigned char * BT_LineControlReg; 
volatile unsigned char * BT_ModemControlReg;
volatile unsigned char * BT_LineStatusReg;  
volatile unsigned char * BT_ModemStatusReg; 
volatile unsigned char * BT_ScratchReg;     
volatile unsigned char * BT_DivisorLatchLSB;
volatile unsigned char * BT_DivisorLatchMSB;


int initMap() {
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


    BT_ReceiverFifo = RS232 + BT_ReceiverBase;
    BT_TransmitterFifo = RS232 + BT_TransmitterBase;
    BT_InterruptEnable = RS232 + BT_InterruptEnableReg;
    BT_InterruptIdentificationReg = RS232 + BT_InterruptIDBase;
    BT_FifoControlReg = RS232 + BT_FifoBase;
    BT_LineControlReg = RS232 + BT_LineControlBase;
    BT_ModemControlReg = RS232 + BT_ModemControlBase;
    BT_LineStatusReg = RS232 + BT_LineStatusBase;
    BT_ModemStatusReg = RS232 + BT_ModemStatusBase;
    BT_ScratchReg = RS232 + BT_ScratchBase;
    BT_DivisorLatchLSB = RS232 + BT_DivisorLSBBase;
    BT_DivisorLatchMSB = RS232 + BT_DivisorMSBBase;
    return 0;
}

void Close_RFS(void) {
    unmap_physical(RS232, 0x500);
}


int Init_RFS(void) {
    // set bit 7 of Line Control Register to 1, to gain access to the baud rate registers
    // set Divisor latch (LSB and MSB) with correct value for required baud rate
    // set bit 7 of Line control register back to 0 and
    // program other bits in that reg for 8 bit data, 1 stop bit, no parity etc
    // Reset the Fifo’s in the FiFo Control Reg by setting bits 1 & 2
    // Now Clear all bits in the FiFo control registers
    memFd = open_physical(memFd);
    if (memFd < 0)
        return memFd;
    RS232 = map_physical(memFd, IO_Base, 0x500);
    if (!RS232)
        return -1;

    int err = initMap();
    if(err)
        return err;
    *RS232_LineControlReg = 0x80;
    // 115200 Baud rate. Divisor = 27 = 0x1B
    *RS232_DivisorLatchLSB = 0x1B;
    *RS232_DivisorLatchMSB = 0x00;
    // 00xx0011 = 0x03
    *RS232_LineControlReg = 0x0;
    *RS232_LineControlReg =  0x03;
    *RS232_FifoControlReg = 0x06;
    *RS232_FifoControlReg = 0x0;

    *BT_LineControlReg = 0x80;
    // 115200 Baud rate. Divisor = 27 = 0x1B
    *BT_DivisorLatchLSB = 0x1B;
    *BT_DivisorLatchMSB = 0x00;
    // 00xx0011 = 0x03
    *BT_LineControlReg = 0x0;
    *BT_LineControlReg =  0x03;
    *BT_FifoControlReg = 0x06;
    *BT_FifoControlReg = 0x0;
    close_physical(memFd);
    return 0;
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
    char c;
    while(RS232TestForReceivedData()){
        c = *RS232_ReceiverFifo;
    }
}


// the following function polls the UART to determine if any character
// has been received. It doesn't wait for one, or read it, it simply tests
// to see if one is available to read from the FIFO
int BTTestForReceivedData(void) {
    // if *BT_LineStatusReg bit 0 is set to 1
    //return TRUE, otherwise return FALSE
    return *BT_LineStatusReg & 1;
}

int putcharBT(int c) {
    // wait for Transmitter Holding Register bit (5) of line status register to be '1'
    // indicating we can write to the device
    // write character to Transmitter fifo register
    // return the character we printed
    while(!((*BT_LineStatusReg >> 5) & 1));
    *BT_TransmitterFifo = (char) c;
    return c;
}

int getcharBT(void) {
    // wait for Data Ready bit (0) of line status register to be '1'
    // read new character from ReceiverFiFo register
    // return new character
    while(!BTTestForReceivedData());
    return *BT_ReceiverFifo;
}

//
// Remove/flush the UART receiver buffer by removing any unread characters
//
void BTFlush(void) {
    // while bit 0 of Line Status Register == ‘1’
    // read unwanted char out of fifo receiver buffer
    char c;
    while(BTTestForReceivedData()){
        c = *BT_ReceiverFifo;
    }
}