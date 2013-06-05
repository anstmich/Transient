#include "Backend_t.h"


/*********************** Backend Class *****************************/


/********** Expose the Backend to python ***********/

using namespace boost::python;

BOOST_PYTHON_MODULE(Backend)
{
    class_<Backend,boost::noncopyable>("Backend")
        
    ;
}
