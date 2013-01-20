/**
 * Defines a simple interface to perform IO with USB devices using libusb.
 *
 * @file USBCom.h 
 * @author Andy Michaels
 * @author Cornell BAJA SAE
 */

#include <libusb-1.0/libusb.h>

#ifndef __USBCOM_H__
#define __USBCOM_H__

enum DeviceErrors
{
	DEV_SUCCESS,
	DEVERR_NOT_FOUND
};	

class Device
{
public:
	virtual int setup() = 0;
	virtual int read_device(unsigned char* str) = 0;
	virtual int cleanup() = 0;
};

class USBDevice : public Device
{
public:
	libusb_device_handle* find_device(int vendorID);
	int setup();
	//int setup(int vendorID);
	int read_device(unsigned char* str);
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
