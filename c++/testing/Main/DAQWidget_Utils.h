#include "Python.h"

#ifndef __DAQWIDGET_UTILS_H__
#define __DAQWIDGET_UTILS_H__


namespace Transient_UI
{
	extern "C" {
	void calculate_points(PyObject* x_data, PyObject* y_data, int dlen, PyObject* points, PyObject* _points,
		double x, double y, double xrange, double yrange, double xmin, double ymin);

	}
}


#endif
