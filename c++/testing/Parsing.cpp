#include "Parsing.h"
#include <cstdlib>
#include <cstring>

#define __PYTHONIFY__

#ifdef __PYTHONIFY__
#include <boost/python.hpp>
using namespace boost::python;
#endif

/******************** Parser Definitions *********************/
int Parser::append_value(int value, std::string name)
{
	int_map_[name] = value;
	return 0;
}

int Parser::append_value(double value, std::string name)
{
	double_map_[name] = value;
	return 0;
}

int Parser::append_value(unsigned char value, std::string name)
{
	uchar_map_[name] = value;
	return 0;
}

int Parser::init_value(const ParseToken* ptok)
{
	switch(ptok->type)
	{
		case INT:
			int_map_[ptok->name] = 0;
			break;
		case DOUBLE:
			double_map_[ptok->name] = 0.0;
			break;
		case UCHAR:
			uchar_map_[ptok->name] = '\00';
			break;
		case FLOAT:
			float_map_[ptok->name] = 0.0f;
			break;
		case UINT:
			uint_map_[ptok->name] = 0;
			break;
		case SHORT:
			short_map_[ptok->name] = 0;
			break;
		case LONG:
			long_map_[ptok->name] = 0;
			break;
		case USHORT:
			ushort_map_[ptok->name] = 0;
			break;
		case ULONG:
			ulong_map_[ptok->name] = 0;
			break;
		case STRING:
			str_map_[ptok->name] = "";
			break;
		default:
			fprintf(stderr, "Warning: Unknown parse type. The value will not be saved\n.");
			return PARSER_UNKNOWN_TYPE;
			break;
	}

	return PARSER_SUCCESS;
}

double Parser::get_double(std::string name)
{
	std::map<std::string, double>::iterator it = double_map_.find(name);
	if(it == double_map_.end()){
		fprintf(stderr, "Unknown value name %s\n", name.c_str());
	}

	return double_map_[name];
}

int Parser::get_int(std::string name)
{
	std::map<std::string, int>::iterator it = int_map_.find(name);
	if(it == int_map_.end()){
		fprintf(stderr, "Unknown value name %s\n", name.c_str());
	}

	return int_map_[name];

}

unsigned char Parser::get_uchar(std::string name)
{
	std::map<std::string, unsigned char>::iterator it = uchar_map_.find(name);
	if(it == uchar_map_.end()){
		fprintf(stderr, "Unknown value name %s\n", name.c_str());
	}

	return uchar_map_[name];
}	

/******************* AsciiParser Definitions **********************/

/**
 * Add a ParseTokens to the parse token list.  ParseTokens define the structure
 * of the parsed string and drive the parsing process.
 */
int AsciiParser::add_token(int type, std::string name, std::string delimiter)
{
	int err;
	boost::shared_ptr<ParseToken> tok = boost::shared_ptr<ParseToken>(new ParseToken());
	tok->type = type;
	tok->name = name;
	tok->delimiter = delimiter[0]; // for now, only single character delimiters are supported

	err = init_value(tok.get());

	if(err == PARSER_SUCCESS) {
		parse_tokens_.push_back(tok);
		return ASCIIPARSE_SUCCESS;
	}
	else {
		return ASCIIPARSE_UNKNOWN_TYPE;
	}
	
}

int AsciiParser::parse_string(char* str, int slen)
{
	TokenList::iterator it;
	char* tok, *delim;
	char num[64]; // we dont expect any number to be more than 64 digits
	int rlen=slen, count = 0;
	uintptr_t tok_len = 0; // PLATFORM DEPENDENT!! 32bit addressing vs 64bit!
	tok = str;

	// preparse to check integrity
	it = parse_tokens_.begin();
	while( (delim = static_cast<char *>(memchr(tok, (*it)->delimiter, rlen))) != NULL)
	{
		count++;
		if(delim - str == 0)
			return ASCIIPARSE_INCOMPLETE_STRING;

		rlen = slen - (delim - str) - 1;
		tok = delim + 1;
		it++;

		if(it == parse_tokens_.end())
			break;
	}

	// not worth wasting time on a string which is known to be invalid at some point
	if(count != parse_tokens_.size())
		return ASCIIPARSE_INCOMPLETE_STRING;

	// parse the data if we have made it thus far!
	rlen = slen;
	tok = str;
	for(it=parse_tokens_.begin(); it != parse_tokens_.end(); it++)
	{
		delim = static_cast<char *>(memchr(tok, (*it)->delimiter, rlen));
		if(delim == NULL)
			return ASCIIPARSE_INCOMPLETE_STRING;

		tok_len = uintptr_t(delim) - uintptr_t(tok);
		rlen = slen - tok_len - 1;
		memcpy(num, tok, tok_len);
		num[tok_len] = 0; // terminate the string!
		tok = delim + 1;

		// save the value
		switch((*it)->type)
		{
			case DOUBLE:
				Parser::append_value((double)atof(num), (*it)->name);
				break;
			case INT:
				Parser::append_value((int)atoi(num), (*it)->name);
				break;
			case UCHAR:
				Parser::append_value((unsigned char)num[0], (*it)->name);
				break;
		}

	}

	return ASCIIPARSE_SUCCESS;
}

/****************** Expose AsciiParser to Python *******************/
#ifdef __PYTHONIFY__
BOOST_PYTHON_MODULE(Parsing)
{
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
	;
	class_<Parser>("Parser")
		.def("get_double", &Parser::get_double)
		.def("get_int", &Parser::get_int)
		.def("get_uchar", &Parser::get_uchar)
	;
	class_<AsciiParser>("AsciiParser")
		.def("add_token", &AsciiParser::add_token)
		.def("parse_string", &AsciiParser::parse_string)
		.def("get_double", &AsciiParser::get_double)
		.def("get_int", &AsciiParser::get_int)
		.def("get_uchar", &AsciiParser::get_uchar)
	;
}
#endif