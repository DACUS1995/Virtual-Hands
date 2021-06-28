import cv2
import mediapipe as mp
from mediapipe.python.solutions.hands import HandLandmark
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

		fingers_pose = self._detect_fingers_pose(landmarks)

		if (fingers_pose["index_finger_open"] and 
			not any({key:fingers_pose[key] for key in fingers_pose if key != "index_finger_open"}.values())):
			return HandType.LEFT_CLICK_HAND

		if not all(fingers_pose.values()):
			return HandType.CLOSE_HAND
		
		# if (landmarks[HandLandmark.INDEX_FINGER_MCP].x - landmarks[HandLandmark.INDEX_FINGER_TIP].x < config.LANDMARK_DISTANCE_THRESHOLD and
		# 	landmarks[HandLandmark.INDEX_FINGER_MCP].y - landmarks[HandLandmark.INDEX_FINGER_TIP].y < config.LANDMARK_DISTANCE_THRESHOLD):
		# 	print(landmarks[9].x - landmarks[8].x)
		# 	print(landmarks[9].y - landmarks[8].y)

		return HandType.OPEN_HAND

	def _detect_fingers_pose(self, landmarks):

		index_finger_open = True
		middle_finger_open = True
		ring_finger_open = True
		pinky_finger_open = True

		# INDEX FINGER
		if (landmarks[HandLandmark.INDEX_FINGER_MCP].x - landmarks[HandLandmark.INDEX_FINGER_TIP].x < config.LANDMARK_DISTANCE_THRESHOLD and
			landmarks[HandLandmark.INDEX_FINGER_MCP].y - landmarks[HandLandmark.INDEX_FINGER_TIP].y < config.LANDMARK_DISTANCE_THRESHOLD):
			index_finger_open = False

		# MIDDLE FINGER
		if (landmarks[HandLandmark.MIDDLE_FINGER_MCP].x - landmarks[HandLandmark.MIDDLE_FINGER_TIP].x < config.LANDMARK_DISTANCE_THRESHOLD and
			landmarks[HandLandmark.MIDDLE_FINGER_MCP].y - landmarks[HandLandmark.MIDDLE_FINGER_TIP].y < config.LANDMARK_DISTANCE_THRESHOLD):
			middle_finger_open = False

		# RING FINGER
		if (landmarks[HandLandmark.RING_FINGER_MCP].x - landmarks[HandLandmark.RING_FINGER_TIP].x < config.LANDMARK_DISTANCE_THRESHOLD and
			landmarks[HandLandmark.RING_FINGER_MCP].y - landmarks[HandLandmark.RING_FINGER_TIP].y < config.LANDMARK_DISTANCE_THRESHOLD):
			ring_finger_open = False

		# PINKY FINGER
		if (landmarks[HandLandmark.PINKY_MCP].x - landmarks[HandLandmark.PINKY_TIP].x < config.LANDMARK_DISTANCE_THRESHOLD and
			landmarks[HandLandmark.PINKY_MCP].y - landmarks[HandLandmark.PINKY_TIP].y < config.LANDMARK_DISTANCE_THRESHOLD):
			pinky_finger_open = False

		return {
			"index_finger_open": index_finger_open,
			"middle_finger_open": middle_finger_open,
			"ring_finger_open": ring_finger_open,
			"pinky_finger_open": pinky_finger_open,
		} 

if __name__ == "__main__":
	detector = HandDetector()
	detector.detect()