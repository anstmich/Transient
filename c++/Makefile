# location of the Python header files

PYTHON = /usr/include/python2.7

# location of the Boost Python include files and library

BOOST_INC = /usr/include
BOOST_LIB = /usr/lib

# compile mesh classes
TARGET = src/DAQWidget_Utils
MODULE_OUTPUT = ../python/Transient/DAQWidget_Utils

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic \
	$(TARGET).o -L$(BOOST_LIB) -lboost_python \
	-L/usr/lib/python2.7/config -lpython2.7 \
	-o $(MODULE_OUTPUT).so

$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON) -Iinclude -I$(BOOST_INC) -c $(TARGET).cpp -o $(TARGET).o -fPIC

clean:
	rm *.o *.so