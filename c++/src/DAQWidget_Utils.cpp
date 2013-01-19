#include <boost/python.hpp>

using namespace boost::python;

void calculate_points(list x_data, list y_data, int dlen, list points, list _points,
		double x, double y, double xrange, double yrange, double xmin, double ymin, double width, double height)
{
	double px, py;
	for(int i = 0; i < dlen; i++)
	{	
		px = x + (extract<double>(x_data[i])-xmin)*1.0/xrange*width;
		py = y + (extract<double>(y_data[i])-ymin)*1.0/yrange*height;
		points.append(px);
		points.append(py);
		
	}
}

BOOST_PYTHON_MODULE(DAQWidget_Utils)
{
	def("calculate_points", calculate_points);
}