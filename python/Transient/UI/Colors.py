

class UIColors:

	MAIN_BG = [0.064, 0.068, 0.068, 1.0]
	DARK_BG = [0.13, 0.135, 0.135, 1.0]
	HEADER_BG = [0.16, 0.165, 0.165, 1.0]
	AXES_BG = [0.1, 0.105, 0.105, 1]
	OUTLINE = [0.175,0.175,0.175,1.0]
	SHADOW = [0, 0, 0, 0.7]
	TICK_LINE = [0.275,0.275,0.275,1.0]

	RED = (0.84, 0.156, 0.164, 1)
	GREEN = (0.576, 0.894, 48, 1)
	BLUE = (0.329, 0.125, 0.933, 1)
	SKY = (0.207, 0.894, 0.894, 1)
	LIGHT_ORANGE = (0.933, 0.655, 0.125, 1)
	LAVENDER = (0.71, 0.141, 0.933, 1)
	ORANGE = (0.933, 0.478, 0.125, 1)
	NEON_RED = (1, 0, 0.164, 1)
	NEON_BLUE = (0.071, 0.031, 0.91, 1)
	NEON_GREEN = (0.047, 0, 0.678, 1)

class ColorQueue:

	def __init__(self):
		self.queue = []
		self.pos = 0

		self.queue.append(UIColors.RED)
		self.queue.append(UIColors.GREEN)
		self.queue.append(UIColors.BLUE)
		self.queue.append(UIColors.SKY)
		self.queue.append(UIColors.LIGHT_ORANGE)
		self.queue.append(UIColors.LAVENDER)
		self.queue.append(UIColors.ORANGE)
		self.queue.append(UIColors.NEON_RED)
		self.queue.append(UIColors.NEON_BLUE)
		self.queue.append(UIColors.NEON_GREEN)

		self.len = len(self.queue)

	def next_color(self):
		color = self.queue[self.pos]
		self.pos += 1
		if(self.pos >= self.len):
			self.pos = 0

		return color

	def to_beginning(self):
		self.pos = 0

