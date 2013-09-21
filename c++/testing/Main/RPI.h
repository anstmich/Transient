#include <thread>
#include <mutex>
#include <condition_variable>

#ifndef __RPI_H__
#define __RPI_H__

class RPI
{

    public:
        RPI();

        void* get_res();
        int get_res_size();
        bool updated();
        void wait_until_updated();
        
        void begin_res_update();
        bool try_res_update();
        void end_res_update();

        void set_res(void* res);
        void set_res_size(int size);

    private:
        void* res_;
        int rsize_;
        bool updated_;

        std::mutex res_mtx_;
        std::mutex update_flag_mtx_;
        std::condition_variable update_cond_;
            
};

#endif
