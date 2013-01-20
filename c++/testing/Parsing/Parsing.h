#include <map> 
#include <string>
#include <list>
#include <boost/shared_ptr.hpp>

#ifndef __PARSING_H__
#define __PARSING_H__

// Parse token 
class ParseToken
{
public:
	int type;
	std::string name;
	unsigned char delimiter;
};

enum DataTypes
{
	SHORT, LONG, INT,
	USHORT, ULONG, UINT,
	UCHAR, CHAR, 
	DOUBLE, FLOAT,
	STRING
};

enum PARSER_ERRORS
{
	PARSER_SUCCESS,
	PARSER_UNKNOWN_TYPE
};

enum ASCII_PARSER_ERRORS
{
	ASCIIPARSE_SUCCESS,
	ASCIIPARSE_UNKNOWN_TYPE,
	ASCIIPARSE_INCOMPLETE_STRING
};

class Parser
{
public:
	double get_double(std::string name);
	int get_int(std::string name);
	unsigned char get_uchar(std::string name);

protected:
	int append_value(int value, std::string name);
	int append_value(double value, std::string name);
	int append_value(unsigned char value, std::string name);

	int init_value(const ParseToken* ptok);

private:
	// data containers
	std::map<std::string, short> short_map_;
	std::map<std::string, long> long_map_;
	std::map<std::string, int> int_map_;
	std::map<std::string, unsigned short> ushort_map_;
	std::map<std::string, unsigned long> ulong_map_;
	std::map<std::string, unsigned int> uint_map_;

	std::map<std::string, unsigned char> uchar_map_;
	std::map<std::string, char> char_map_;

	std::map<std::string, double> double_map_;
	std::map<std::string, float> float_map_;

	std::map<std::string, std::string> str_map_;
};

class AsciiParser : public Parser
{
public:
	int add_token(int type, std::string name, std::string delimiter);
	int parse_string(char* str, int slen);

private:
	std::string format;

	typedef std::list<boost::shared_ptr<ParseToken> > TokenList;
	TokenList parse_tokens_;

};

#endif