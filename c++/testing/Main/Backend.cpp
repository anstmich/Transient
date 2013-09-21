#include "Backend.h"
#include <cstdlib>
#include <cstring>
#include <cstdio>

HardwareLayer::HardwareLayer()
{

}

HardwareLayer::HardwareLayer(Device* dev, RPI* res)
{
    dev_ = dev;
    rpi_ = res;
    resource_ = static_cast<unsigned char *>(rpi_->get_res());
}

void HardwareLayer::operator()()
{
    int len=0;
    while(true) {
        if(active_) {
            
            while(len == 0)
                len = dev_->poll(buffer_);

            while(buffer_[len-1] != '\n') {
                len += dev_->poll(buffer_+len);
            }
            
            if(len > 0) {   
                rpi_->begin_res_update();
                buffer_[len++] = 0;
                memcpy(resource_, buffer_, len); 
                rpi_->set_res_size(len);
                rpi_->end_res_update();
            }
            
            len = 0; 
        }

        //sleep 1 us to avoid 100% cpu -- TODO: Find better alternative
        usleep(1);
    }
}

void HardwareLayer::enable()
{
    active_ = true;
    dev_->setup();
}

void HardwareLayer::disable()
{
    active_ = false;
    dev_->cleanup();
    
}

int HardwareLayer::send(unsigned char* buff, int len)
{
	dev_->send(buff, len);
}

/********* Post Processing Layer ********************/
PostProcLayer::PostProcLayer()
{

}

PostProcLayer::PostProcLayer(RPI* rpi, Parser* p)
{
    rpi_ = rpi;
    res_ = static_cast<unsigned char*>(rpi_->get_res());
    parser_ = p;

    parse_structure_ = p->expose_structure();
    qlen_ = 0;
}

void PostProcLayer::operator()()
{
    int status;

    while(true) {
        rpi_->wait_until_updated();
        dlen_ = rpi_->get_res_size();
        memcpy(data_, res_, dlen_);
        data_[dlen_++] = 0;
        
        status = parser_->parse(data_, dlen_);

        // buffer the parsed values
        if(status == PARSER_SUCCESS) {
            ValueTypeList::iterator it;
            for(it = parse_structure_.begin(); it != parse_structure_.end(); it++) {
                switch(it->second) {
                    case DOUBLE:
                        double_buffer_[it->first].push_back(parser_->get_double(it->first));
                        break;
                    case INT:
                        int_buffer_[it->first].push_back(parser_->get_int(it->first));
                        break;
                    case UCHAR:
                        uchar_buffer_[it->first].push_back(parser_->get_uchar(it->first));
                        break;
                }
            }

            qlen_++;
        }
    }  
}

void PostProcLayer::get_doubles(std::string s, PyObject* list)
{
	int size = double_buffer_.size();

	for(int i = 0; i < size; i++) {
		PyList_Append(list, PyFloat_FromDouble(double_buffer_[s].front()));
		double_buffer_[s].pop_front();
	}
}

void PostProcLayer::get_uchar(std::string s, PyObject* list)
{
	int size = uchar_buffer_.size();

	for(int i = 0; i < size; i++) {
		PyList_Append(list, PyInt_FromLong((long)uchar_buffer_[s].front()));
		uchar_buffer_[s].pop_front();
	}
}

void PostProcLayer::get_int(std::string s, PyObject* list)
{
	int size = int_buffer_.size();

	for(int i = 0; i < size; i++) {
		PyList_Append(list, PyInt_FromLong((long)int_buffer_[s].front()));
		int_buffer_[s].pop_front();
	}
}


/*********************** Backend Class *****************************/


Backend::Backend()
{
    rpi_.set_res(rpi_buff_);
}

void Backend::set_device(Device* dev)
{
    hw_layer_ = HardwareLayer(dev, &rpi_);
    
}
void Backend::set_parser(Parser* p)
{
    pp_layer_ = PostProcLayer(&rpi_, p);
}

void Backend::start()
{
	printf("Starting\n");
    hw_layer_.enable();
    hw_thread_ = std::thread(std::ref(hw_layer_));
    pp_thread_ = std::thread(std::ref(pp_layer_));
}

void Backend::stop()
{
    hw_layer_.disable();
}

void Backend::finish()
{
	printf("finishing\n");
    hw_thread_.join();
    pp_thread_.join();
}

void Backend::get_doubles(std::string s, PyObject* list)
{
    pp_layer_.get_doubles(s, list);
}

void Backend::get_uchars(std::string s, PyObject* list)
{
    pp_layer_.get_uchar(s,list);
}

void Backend::get_ints(std::string s, PyObject* list)
{
    pp_layer_.get_int(s,list);
}

void Backend::send(std::string s)
{
	unsigned char* buff = (unsigned char*)&s.c_str()[0];
	hw_layer_.send(buff, s.size());
	
}
