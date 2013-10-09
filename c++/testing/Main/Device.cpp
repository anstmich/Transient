 /**
 * Defines a simple interface to perform IO with USB devices using libusb.
 *
 * @file USBCom.c 
 * @author Andy Michaels
 * @author Cornell BAJA SAE
 */

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <libusb-1.0/libusb.h>
#include "Device.h"

/******** Empty Device implementations *********/

bool SerialDevice::incoming_;

SerialDevice::SerialDevice()
{
    port_ = "/dev/ttyUSB0";
    baud_ = 9600;
}

SerialDevice::SerialDevice(const char* port, int baud)
{
    port_ = port;
    baud_ = baud;
}

SerialDevice::~SerialDevice()
{
    cleanup();
}

int SerialDevice::setup()
{
    return setup(port_.c_str(), baud_);
}

int SerialDevice::setup(const char* port, int baud)
{
    // set up nonblocking readwrite transfer
    ser_ = open(port, O_RDWR | O_NOCTTY);

    if(ser_ < 0) {
        perror(port);
        exit(DEVERR_FAILED_TO_OPEN);
    }
    
    // save current port settings to be restored upon completion
    tcgetattr(ser_,&oldtio_); 
    bzero(&tio_, sizeof(tio_));

    // set up the new port attributes 
    tio_.c_cflag = get_baud_(baud) | CRTSCTS | CS8 | CLOCAL | CREAD;
    tio_.c_iflag = IGNPAR | ICRNL;
    tio_.c_oflag = 0;
    tio_.c_lflag = ICANON;
    tio_.c_cc[VMIN]=1;
    tio_.c_cc[VTIME]=0;

    tcflush(ser_, TCIFLUSH);
    tcsetattr(ser_,TCSANOW,&tio_);

    return DEV_SUCCESS;
     
}

int SerialDevice::poll(unsigned char* buff)
{
    ssize_t len=0;
    len = read(ser_, buff, MAX_BYTES);
    return len;
}

int SerialDevice::send(const unsigned char* buff, int len)
{
	int err = 0;
	err = write(ser_, buff, len);
	return err;
}

int SerialDevice::cleanup()
{
    tcsetattr(ser_,TCSANOW,&oldtio_);
    return 0;
}

speed_t SerialDevice::get_baud_(int baud)
{
    switch(baud) {
        case 0:
            return B0;
            break;
        case 50:
            return B50;
            break;
        case 75:
            return B75;
            break;
        case 110:
            return B110;
            break;
        case 9600:
            return B9600;
            break;
        case 19200:
            return B19200;
            break;
        case 38400:
            return B38400;
            break;
        case 57600:
            return B57600;
            break;
        case 115200:
            return B115200;
            break;
        case 230400:
            return B230400;
            break;
        default:
            fprintf(stderr, "Error: Unknown baudrate %d\n", baud);
            exit(DEVERR_UNKNOWN_BAUD);
    }

}

void SerialDevice::signal_handler_(int status)
{
    incoming_ = true;
}


/**
 * NOTE: Used internally. Not likely used by client programmer.
 * 
 * Searches for a USB device with a matching vendorID.  If found, the corresponding
 * libusb device is returned.  If not, null is returned.
 *
 * @param vendorID The vendor ID of the device
 */
libusb_device_handle* USBDevice::find_device(int vendorID)
{

    libusb_device** list;
    libusb_device* found = NULL;
    libusb_device* device;
    libusb_device_handle* handle;
    struct libusb_device_descriptor descriptor;
  
    ssize_t count = libusb_get_device_list(NULL, &list);
    ssize_t i = 0;
    int err = 0;

    if(count < 0) 
        return NULL;
  
    for(i = 0; i < count; i++) {
        device = list[i];

        libusb_get_device_descriptor(device, &descriptor);
    
        if(descriptor.idVendor == vendorID) {
            fprintf(stderr, "Device with id %x found.", vendorID);
            found = device;

            break;
        }
            
    }
  
    if(found) {
        err = libusb_open(found, &handle);
        
        if(err)
            return NULL;
    }
    else {
        return NULL;
    }
    
    libusb_free_device_list(list, 1);
    
    return handle;
}


/*int USBDevice::setup(int vendorID)
{
    vendorID_ = vendorID;
    return setup();
}*/


/**
 * Initializes libusb and claims the device from the Operating system.  This function
 * MUST be called before any subsequent actions are performed on the USB device.
 *
 * @todo Implement contexts (allows IO with multiple USB devices)
 * @param dev USBDevice struct that describes the connected device.  Used throughout library.
 * @return 0 on Success
 */
int USBDevice::setup()
{
    int error;
    libusb_init(NULL);
    
    inEndpoint_ = 0x81;
    outEndpoint_ = 0x01;

    device_ = find_device(vendorID_);

    if(device_ == NULL) {
        fprintf(stderr, "*** Error: Device %x not found. Quitting.\n", vendorID_);
        return DEVERR_NOT_FOUND;
    }
    
    if(libusb_kernel_driver_active(device_, 0) == 1)  
        error = libusb_detach_kernel_driver(device_, 0);
    if(libusb_kernel_driver_active(device_, 1) == 1)
    	error = libusb_detach_kernel_driver(device_, 0);
    	 
    //printf("Error code: %d\n", error);
    libusb_claim_interface(device_, 0);
    libusb_set_interface_alt_setting(device_, 0, 0);
    //printf("Error code: %d\n", error);
    
    return error;
    
}

/**
 * Clean up and exit libusb.  Call this function after all IO tasks have finished.
 *
 * @todo Implement contexts
 * @param dev The device descriptor
 * @ return 0 on Success
 */
int USBDevice::cleanup()
{
    int error;
    
    error = libusb_attach_kernel_driver(device_, 0);
    libusb_exit(NULL);
    
    return error;
}

/**
 * Perform a bulk transfer on a USB device.  On success, the buffer is filled 
 * and the number of bytes transferred is returned.  A call to USBCom_setup must precede 
 * this function.
 *
 * @param buffer The buffer to which data is transfered.
 * @param bufferLength The length of the data buffer (number supplied to malloc())
 * @param dev The usb device descriptor
 * @retuen The number of bytes transfered.
 */
int USBDevice::bulk_get(unsigned char * buffer, int bufferLength)
{
    int numBytes = 0, error = 0;

    error = libusb_bulk_transfer(device_, (inEndpoint_ | LIBUSB_ENDPOINT_IN), buffer, bufferLength, &numBytes, 1);
   
    return numBytes;
}


int USBDevice::bulk_send(unsigned char * buffer, int bufferLength)
{
    int numBytes = 0, error=0;
    
    error = libusb_bulk_transfer(device_, (outEndpoint_ | LIBUSB_ENDPOINT_OUT), buffer, bufferLength, &numBytes, 2);
    
    return numBytes;
}

void USBDevice::set_vendor_id(int id)
{
    vendorID_ = id;
}

int USBDevice::poll(unsigned char* str)
{
    return bulk_get(str, INPUT_BUFFER_LEN);
}

int USBDevice::send(const unsigned char* buff, int len)
{
	return 0;
}
