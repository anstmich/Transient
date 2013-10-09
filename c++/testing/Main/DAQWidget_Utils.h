#include <boost/python.hpp>

#ifndef __DAQWIDGET_UTILS_H__
#define __DAQWIDGET_UTILS_H__

using namespace boost::python;

namespace Transient_UI
{
	void calculate_points(list x_data, list y_data, int dlen, list points, list _points,
		double x, double y, double xrange, double yrange, double xmin, double ymin);
}


#endif