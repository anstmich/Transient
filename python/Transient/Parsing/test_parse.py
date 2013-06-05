from Parsing import AsciiFormat

tp = AsciiFormat('<START=$><erpm=NUMBER>,<crpm=NUMBER>,<torque=NUMBER><END=\n>')
s = '1.234,5.643,324.2'
tp.parser.parse(s, len(s)+1)
print tp.parser.get_double('erpm'), tp.parser.get_double('crpm')
