# location of the Python header files

PYTHON = /usr/include/python2.7

# location of the Boost Python include files and library

BOOST_INC = /usr/include
BOOST_LIB = /usr/lib

# compile mesh classes
TARGET = Device
MODULE_OUTPUT = DeviceBackend#../../python/Transient/Parsing

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic \
	$(TARGET).o -L$(BOOST_LIB) -lboost_python -lusb-1.0 \
	-L/usr/lib/python2.7/config -lpython2.7 \
	-o $(MODULE_OUTPUT).so

$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON) -Iinclude -I$(BOOST_INC) -c $(TARGET).cpp -o $(TARGET).o -fPIC

clean:
	rm *.o *.so

test:
	g++ -c Device.cpp -Wall -g -o Device.o -std=c++0x
