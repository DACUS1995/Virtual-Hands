from enum import Enum
from typing import Dict, Tuple, List
import cv2

from hand_detector import HandDetector, HandType
from cursor import Cursor


class Controller():
	def __init__(self, hand_detector:HandDetector, cursor:Cursor) -> None:
		self.hand_detector = hand_detector
		self.cursor = cursor
		self.is_running = False

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
			coordinates = (
				self.cursor.screen_size[0] * landmark[8].x,
				self.cursor.screen_size[1] * landmark[8].y
			)
			self.cursor.set_position(coordinates)

