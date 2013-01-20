#include "Parsing.h"
#include <cstring>

int main()
{
	AsciiParser ap;

	ap.add_token(INT, "A", ",");
	ap.add_token(DOUBLE, "B", ":");
	ap.add_token(UCHAR, "C", "?");

	char test[] = "10,22.3:D?";
	int err = ap.parse_string(test, strlen(test));

	printf("Errors? %d\nResult: %d, %f, %c\n", err, ap.get_int("A"), ap.get_double("B"), ap.get_uchar("C"));

	return 0;
}