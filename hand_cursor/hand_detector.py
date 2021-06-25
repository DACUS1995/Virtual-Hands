import cv2
import mediapipe as mp
from enum import Enum
from typing import Dict, Tuple, List

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class HandType(Enum):
    OPEN_HAND = 1
    CLOSE_HAND = 2

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

					return results.multi_hand_landmarks[0], HandType.OPEN_HAND
				else:
					return None

if __name__ == "__main__":
	detector = HandDetector()
	detector.detect()