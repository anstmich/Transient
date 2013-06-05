#include <cstdio>
#include <iostream>
#include "Backend.h"

int main()
{
    unsigned char buffer[1024];
    RPI res;
    res.set_res(buffer);
    SerialDevice sd("/dev/pts/3", 115200);
    AsciiParser parse;

    parse.add_token(DOUBLE, "time", ",");
    parse.add_token(DOUBLE, "long", ",");
    parse.add_token(UCHAR, "longdir", ",");
    parse.add_token(DOUBLE, "lat", ",");
    parse.add_token(UCHAR, "latdir", ",");
    parse.add_token(DOUBLE, "hdop", ",");
    parse.add_token(UCHAR, "status", ",");
    parse.add_token(DOUBLE, "speed", ",");
    parse.add_token(DOUBLE, "heading", ",");
    parse.add_token(INT, "erpm", ",");
    parse.add_token(INT, "wrpm", ",");
    parse.add_token(INT, "b1", ",");
    parse.add_token(INT, "b2", ",");
    parse.add_token(INT, "b3", "\n");
    
   
    Backend b;
    b.set_device(&sd);
    b.set_parser(&parse);
    b.start();
    b.finish();

    return 0;
}
