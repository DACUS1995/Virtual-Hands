import cv2
import mediapipe as mp
from enum import Enum
from typing import Dict, Tuple, List

import config

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class HandType(Enum):
	OPEN_HAND = 1
	CLOSE_HAND = 2
	LEFT_CLICK_HAND = 3

class HandDetector():
	def __init__(self, mode:str = "mediapipe", show:bool =True):
		self.mode = mode
		self.show = show 

	def detect(self, image):

		with mp_hands.Hands(
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5) as hands:
				image.flags.writeable = False
				results = hands.process(image)
				# Draw the hand annotations on the image.
				image.flags.writeable = True
				image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				if results.multi_hand_landmarks:
					for hand_landmarks in results.multi_hand_landmarks:
						mp_drawing.draw_landmarks(
							image, 
							hand_landmarks,
							mp_hands.HAND_CONNECTIONS
						)

					if self.show:
						cv2.imshow("Hands", image)

					hand_type = self._classify_hand_pose(results.multi_hand_landmarks[0])
					return results.multi_hand_landmarks[0], hand_type
				else:
					return None

	def _classify_hand_pose(self, hand_landmarks):
		landmarks = hand_landmarks.landmark
		if (landmarks[9].x - landmarks[8].x < config.CLICK_DISTANCE_THRESHOLD and
			landmarks[9].y - landmarks[8].y < config.CLICK_DISTANCE_THRESHOLD):
			print(landmarks[9].x - landmarks[8].x)
			print(landmarks[9].y - landmarks[8].y)
			return HandType.LEFT_CLICK_HAND

		return HandType.OPEN_HAND


if __name__ == "__main__":
	detector = HandDetector()
	detector.detect()