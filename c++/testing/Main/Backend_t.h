#include "Device.h"
#include "RPI.h"
#include "Parsing.h"
#include <map> 
#include <string>
#include <deque>
#include <boost/python.hpp>

#ifndef __BACKEND_H__
#define __BACKEND_H__

using namespace std; // you'll see why...


class Backend
{
        
    private:
        //boost::thread pp_thread_;
        //boost::thread hw_thread_;

        //PostProcLayer pp_layer_;
        //HardwareLayer hw_layer_;

        RPI rpi_;
        unsigned char rpi_buff_[1024];
};

#endif 
