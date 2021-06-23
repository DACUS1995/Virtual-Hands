from enum import Enum

class Cursor():
	def __init__(self, hand_detector, config):
		self.hand_detector = hand_detector
		self.config = config

	def get_position(self):
		pass

	def set_position(self, coordinates):
		pass

	def perform_action(self, action:CursorAction):
		pass


class CursorAction(Enum):
	LEFT_CLICK_ACTION = 1
	RIGHT_CLICK_ACTION = 2

