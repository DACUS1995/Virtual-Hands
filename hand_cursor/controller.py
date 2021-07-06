from enum import Enum
from typing import Dict, Tuple, List
import cv2
import time

from hand_detector import HandDetector, HandType
from cursor import Cursor, CursorAction
import config


class Controller():
	def __init__(self, hand_detector:HandDetector, cursor:Cursor) -> None:
		self.hand_detector = hand_detector
		self.cursor = cursor
		self.is_running = False
		self.last_action_timestamp = time.time()
		self._last_open_hand_coordinates = None

	def start(self):
		self.is_running = True
		cap = cv2.VideoCapture(0)
		try:
			while cap.isOpened() and self.is_running:
				success, image = cap.read()
				if not success:
					print("Ignoring empty camera frame.")
					continue

				image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

				result = self.hand_detector.detect(image)
				if result is None:
					pass
				else:
					landmarks, type = result
					self._update(landmarks, type)

				if cv2.waitKey(5) & 0xFF == 27:
					self.is_running = False
					break
		finally:
			cap.release()


	def _update(self, landmarks, type:HandType):
		landmark = landmarks.landmark
		
		if type == HandType.OPEN_HAND:
			if self._last_open_hand_coordinates is not None:
				coordinates = (
					self.cursor.screen_size[0] * landmark[config.OPEN_HAND_LANDMARK].x - self._last_open_hand_coordinates[0],
					self.cursor.screen_size[1] * landmark[config.OPEN_HAND_LANDMARK].y - self._last_open_hand_coordinates[1]
				)
				self.cursor.move_rel(coordinates)
		elif type == HandType.LEFT_CLICK_HAND:
			self._perform_cursor_action(CursorAction.LEFT_CLICK_ACTION)
		elif type == HandType.CLOSE_HAND:
			pass
		else:
			raise Exception("Unhandled hand type")

		if type == HandType.OPEN_HAND:
			self._last_open_hand_coordinates = (
				self.cursor.screen_size[0] * landmark[config.OPEN_HAND_LANDMARK].x,
				self.cursor.screen_size[1] * landmark[config.OPEN_HAND_LANDMARK].y
			)
		else:
			self._last_open_hand_coordinates = None


	def _perform_cursor_action(self, action:CursorAction):
		curr_time = time.time()
		if curr_time - self.last_action_timestamp < 1:
			return

		self.last_action_timestamp = curr_time
		self.cursor.perform_action(action)
		
