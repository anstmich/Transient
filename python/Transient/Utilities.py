
def place_value(val):

	tmp = val
	place = 0

	if(tmp > 1):
		while(int(tmp/10) > 0):
			place += 1
			tmp = int(tmp/10)

		return place
	else:
		place = 1
		while(int(tmp*10) < 1):
			place += 1
			tmp = tmp*10

		return -1*place

def num_to_str(num, digits, trunc=False, sci=False):

	val = 0

	# if the number cannot fit in the specified number of digits
	if(abs(num) >= 10**(digits+1)):
		place = place_value(num)
		if(trunc):
			val = int(num / (10**place))
			return ''.join([str(val), 'e', str(place)])
		else: 
			figs = digits - 2
			val = num/(10.0**place)
			text = str(val)

			if(num < 0):
				return ''.join([text[0:figs+2], 'e', str(place)])
			else:
				return ''.join([text[0:figs+1], 'e', str(place)])
	elif(abs(num) <= 10**(-1*digits)):
		return str(num)
	else:
		text = str(num)
		
		if(num < 0):
			if(len(text) <= digits+2):
				return text
			else:
				return text[0:digits+2]
		else:
			if(len(text) <= digits+1):
				return text
			else:
				return text[0:digits+1]

def set_pos(obj, x, y):
	obj.pos = [int(x), int(y)]

def set_size(obj, width, height):
	obj.size = [int(width), int(height)]

def raise_to_top(layout, obj):
	layout.remove_widget(obj)
	layout.add_widget(obj)
