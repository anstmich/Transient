#include "Python.h"
#include "Device.h"
#include "RPI.h"
#include "Parsing.h"
#include <map> 
#include <string>
#include <deque>
#include <thread>
#include <mutex>


#ifndef __BACKEND_H__
#define __BACKEND_H__

using namespace std; // you'll see why...

class HardwareLayer
{
    public:
        HardwareLayer();
        HardwareLayer(Device* dev, RPI* res);

        /// Make the class a callable functor -- thread runs this function
        void operator()();

        void enable();
        void disable();

		int send(unsigned char* buff, int len);

    private:
        Device* dev_;
        RPI* rpi_;

        bool active_;
        unsigned char buffer_[1024];
        
        unsigned char* resource_;
};

class PostProcLayer 
{
    public:
        PostProcLayer();
        PostProcLayer(RPI* rpi, Parser* p);
        void operator()();

        void get_doubles(std::string s, PyObject* list);
        void get_uchar(std::string s, PyObject* list);
        void get_int(std::string s, PyObject* list);


    private:
        unsigned char data_[1024];
        int dlen_;

        RPI* rpi_;
        Parser* parser_;

        unsigned char* res_;

        ValueTypeList parse_structure_;

        map<string, deque<double> > double_buffer_;
        map<string, deque<int> > int_buffer_;
        map<string, deque<unsigned char> > uchar_buffer_;

        int qlen_;
};

class Backend
{
    public:
        Backend();
        
        void set_device(Device* dev);
        void set_parser(Parser* p);
        void start();
        void stop();
        void finish();

        void get_doubles(std::string s, PyObject* list);
        void get_uchars(std::string s, PyObject* list);
        void get_ints(std::string s, PyObject* list);

		void send(std::string s);

    private:
        std::thread pp_thread_;
        std::thread hw_thread_;

        PostProcLayer pp_layer_;
        HardwareLayer hw_layer_;

        RPI rpi_;
        unsigned char rpi_buff_[1024];
};

#endif 
