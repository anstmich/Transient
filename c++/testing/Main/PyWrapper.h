
#ifndef __PYWRAPPER_H__
#define __PYWRAPPER_H__

extern "C"
{
	void* new_Backend();
	void* new_SerialDevice(const char* port, int baud);
}

#endif
