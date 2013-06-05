#include <libusb-1.0/libusb.h>
#include <termios.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>
#include <stdlib.h>
#include "Device.h"

int main()
{
    unsigned char buff[512];
    int len = 0;
    SerialDevice sd("/dev/pts/5", 115200);
    
    while(true) {

        len = sd.poll(buff);

        if(len > 0)
        {
            buff[len] = 0;
            printf("Got: %s\n", buff);
        }   

    } 

    return 0;
}
