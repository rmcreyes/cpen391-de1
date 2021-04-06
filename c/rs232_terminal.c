#include "rs232.h"
#include <stdio.h>

int main() {
    char input[50];
    char output[50];
    char * i;
    Init_RS232();

    putcharRS232('\r');
    putcharRS232('\n');
    putcharRS232('\r');
    putcharRS232('\n');
    putcharRS232('\r');
    putcharRS232('\n');
    sleep(2);
    RS232Flush();

    while (1) {
        printf("Input: ");
        gets(input);
        for (i = input; *i != 0; i++) {
            putcharRS232(*i);
        }
        putcharRS232('\r');
        putcharRS232('\n');
        i = output;
        *i = getcharRS232();
        while (*i != '\n') {
            i++;
            *i = getcharRS232();
        }
        if(!RS232TestForReceivedData()) {
            i++;
            *i = getcharRS232();
            while (*i != '\n' && *i != '>') {
                i++;
                *i = getcharRS232();
            }
        }
        *i = 0;
        printf("Received: %s", output);
        printf("\n---------------------------\n");
        sleep(1);
        RS232Flush();
    }
    return 0;
}