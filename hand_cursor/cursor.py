import pyautogui as pui

from enum import Enum
from typing import Dict, Tuple, List


class CursorAction(Enum):
	LEFT_CLICK_ACTION = 1
	RIGHT_CLICK_ACTION = 2


class Cursor():
	def __init__(self, config:Dict = {})->None:
		self.config = config
		self.screen_size = pui.size()
		self.duration = config.get("duration", 0)
		print(self.screen_size)

	def move_rel(self, coordinates):
		pui.moveRel(coordinates[0], coordinates[1], self.duration)

	def get_position(self)->Tuple:
		return pui.position(0)

	def set_position(self, coordinates)->None:
		if coordinates[0] > self.screen_size[0] \
			or coordinates[1] > self.screen_size[1]:
			raise Exception(f"New position coordinates {coordinates} out of bounds.")


	def perform_action(self, action:CursorAction):
		if action == CursorAction.LEFT_CLICK_ACTION:
			pui.leftClick()


