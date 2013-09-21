/**
 * Defines a simple interface to perform IO with USB devices using libusb.
 *
 * @file USBCom.h 
 * @author Andy Michaels
 * @author Cornell BAJA SAE
 */

#include <libusb-1.0/libusb.h>
#include <termios.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string>

#ifndef __DEVICE_H__
#define __DEVICE_H__

enum DeviceErrors
{
	DEV_SUCCESS,
    DEVERR_UNKNOWN_BAUD,
    DEVERR_FAILED_TO_OPEN,
	DEVERR_NOT_FOUND
};	

class Device
{
public:
	virtual int setup() = 0;
	virtual int poll(unsigned char* str) = 0;
	virtual int send(const unsigned char* buff, int len) = 0;
	virtual int send_async(const unsigned char* buff, int len, int timeout);
	virtual int cleanup() = 0;
};

class SerialDevice : public Device 
{
    public:
        SerialDevice();
        SerialDevice(const char* port, int baud);
        ~SerialDevice();
        virtual int setup();
        int setup(const char* port, int baud);
        virtual int poll(unsigned char* buff);
		virtual int send(const unsigned char* buff, int len);
        virtual int cleanup();

        const static int MAX_BYTES = 1024;

    private:
        static void signal_handler_(int status);
        speed_t get_baud_(int baud);

    private:
        std::string port_;
        int baud_;
        int ser_;
        struct termios tio_, oldtio_;
        struct sigaction saio_;

        static bool incoming_;
          
};

class USBDevice : public Device
{
public:
	libusb_device_handle* find_device(int vendorID);
	int setup();
	//int setup(int vendorID);
	int poll(unsigned char* str);
	virtual int send(const unsigned char* buff, int len);
	int bulk_get(unsigned char * buffer, int bufferLength);
	int bulk_send(unsigned char * buffer, int bufferLength);
	int cleanup();

	void set_vendor_id(int id);

private:
	int inEndpoint_;
	int outEndpoint_;
	int vendorID_;
	int productID_;
	
	libusb_device_handle* device_;
	libusb_context** context_;

	const static int INPUT_BUFFER_LEN = 512;
};

#endif 
