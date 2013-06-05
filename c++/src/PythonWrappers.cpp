#include "Backend.h"
#include "Parsing.h"
#include "Device.h"
#include <boost/python.hpp>


using namespace boost::python;

BOOST_PYTHON_MODULE(Backend)
{
    class_<Backend,boost::noncopyable>("Backend")
        .def("set_device", &Backend::set_device)
        .def("set_parser", &Backend::set_parser)
        .def("start", &Backend::start)
        .def("stop", &Backend::stop)
        .def("finish", &Backend::finish)
        .def("get_doubles", &Backend::get_doubles)
        .def("get_ints", &Backend::get_ints)
        .def("get_uchars", &Backend::get_uchars)
    ;
    class_<ParseToken>("ParseToken");
	enum_<DataTypes>("DataTypes")
		.value("SHORT", SHORT)
		.value("LONG", LONG)
		.value("INT", INT)
		.value("USHORT", USHORT)
		.value("ULONG", ULONG)
		.value("UINT", UINT)
		.value("UCHAR", UCHAR)
		.value("CHAR", CHAR)
		.value("DOUBLE", DOUBLE)
		.value("FLOAT", FLOAT)
		.value("STRING", STRING)
		.value("NUMBER", NUMBER) // number is a generic type to be determined by the front end
	;

    /************** Parser Exposure **********************/
    class_< Parser , boost::noncopyable>("Parser", no_init);
	class_<AsciiParser, bases<Parser> >("AsciiParser")
		.def("add_token", &AsciiParser::add_token)
		.def("parse", &AsciiParser::parse)
		.def("get_double", &AsciiParser::get_double)
		.def("get_int", &AsciiParser::get_int)
		.def("get_uchar", &AsciiParser::get_uchar)
	;

    /************** Device Exposure *******************/
    enum_<DeviceErrors>("DeviceErrors")
        .value("DEV_SUCCESS", DEV_SUCCESS)
        .value("DEVERR_NOT_FOUND", DEVERR_NOT_FOUND)
    ;
    class_< Device, boost::noncopyable>("Device", no_init);
    class_<SerialDevice, bases<Device> >("SerialDevice")
        .def(init<const char*, int>())
    ;
    class_<USBDevice, bases<Device> >("USBDevice")
        .def("setup", &USBDevice::setup)
        .def("poll", &USBDevice::poll)
        .def("bulk_get", &USBDevice::bulk_get)
        .def("bulk_send", &USBDevice::bulk_send)
        .def("cleanup", &USBDevice::cleanup)
        .def("set_vendor_id", &USBDevice::set_vendor_id)
    ;
}

