#include "RPI.h"

RPI::RPI()
{
    updated_ = false;
    rsize_ = 0;
    res_ = 0;
}

void* RPI::get_res()
{

    return res_;
}

int RPI::get_res_size()
{
    return rsize_;
}

bool RPI::updated()
{
    if(updated_) {
        res_mtx_.lock();
        updated_ = false;
        res_mtx_.unlock();
        return true;
    }
    else {
        return false;
    }
}

void RPI::wait_until_updated()
{
    boost::unique_lock<boost::mutex> lock(res_mtx_);
    while(!updated_)
        update_cond_.wait(lock);

    updated_ = false;

}

void RPI::set_res(void* res)
{
    res_ = res;
}

void RPI::set_res_size(int size)
{
    rsize_ = size;
}

void RPI::begin_res_update()
{
    res_mtx_.lock();
}

bool RPI::try_res_update()
{
    return res_mtx_.try_lock();
}

void RPI::end_res_update()
{
    updated_ = true;
    res_mtx_.unlock();
    update_cond_.notify_all(); 
}

