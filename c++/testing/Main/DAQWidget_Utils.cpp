#include "DAQWidget_Utils.h"

void calculate_points(PyObject* x_data, PyObject* y_data, int dlen, PyObject* points, PyObject* _points,
		double x, double y, double xrange, double yrange, double xmin, double ymin, double width, double height)
{
	double px, py, xd, yd;
	for(int i = 0; i < dlen; i++)
	{	
		xd = PyFloat_AS_DOUBLE(PyList_GetItem(x_data, i));
		yd = PyFloat_AS_DOUBLE(PyList_GetItem(y_data, i));
		px = x + (xd-xmin)*1.0/xrange*width;
		py = y + (yd-ymin)*1.0/yrange*height;
		PyList_Append(points, PyFloat_FromDouble(px));
		PyList_Append(points, PyFloat_FromDouble(py));
	}
}
