#include "Backend.h"

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

void PostProcLayer::get_doubles(std::string s, boost::python::list l)
{
    transfer<double>(double_buffer_[s], l);
}

void PostProcLayer::get_uchar(std::string s, boost::python::list l)
{
    transfer<unsigned char>(uchar_buffer_[s], l);
}

void PostProcLayer::get_int(std::string s, boost::python::list l)
{
    transfer<int>(int_buffer_[s], l);
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
    hw_layer_.enable();
    hw_thread_ = boost::thread(boost::ref(hw_layer_));
    pp_thread_ = boost::thread(boost::ref(pp_layer_));
}

void Backend::stop()
{
    hw_layer_.disable();
}

void Backend::finish()
{
    hw_thread_.join();
    pp_thread_.join();
}

void Backend::get_doubles(std::string s, boost::python::list l)
{
    pp_layer_.get_doubles(s, l);
}

void Backend::get_uchars(std::string s, boost::python::list l)
{
    pp_layer_.get_uchar(s,l);
}

void Backend::get_ints(std::string s, boost::python::list l)
{
    pp_layer_.get_int(s,l);
}

