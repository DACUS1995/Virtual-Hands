import argparse
from collections import namedtuple
from typing import List, NamedTuple
import cv2
import pickle

from hand_detector import HandDetector


DEFAULT_NUM_SAMPLES = 1000


Landmark = namedtuple("Landmark", ["x", "y", "z"])


def main(args):
	hand_detector = HandDetector()
	sample_counter = 0
	recordings = []

	cap = cv2.VideoCapture(0)

	try:
		while sample_counter < args.samples and cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				continue

			image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

			result = hand_detector.detect(image)
			sample_counter += 1

			if sample_counter % 100 == 0:
				print(f"Number of samples: {sample_counter}")

			if result is None:
				pass
			else:
				landmarks = result
				landmark = landmarks.landmark
				landmark = normalized_landmark_to_list(landmark)
				recordings.append(landmark)

			if cv2.waitKey(5) & 0xFF == 27:
				break
	finally:
		cap.release()

	save_recordings(recordings, args.pose)

def save_recordings(recordings, pose="open_hand"):
	with open(f"{pose}_landmarks.pkl", "wb") as file:
		pickle.dump(recordings, file)

def normalized_landmark_to_list(landmarks)->List[NamedTuple]:
	landmarks_list = list(landmarks)
	landmarks_list = map(
		lambda landmark: Landmark(landmark.x, landmark.y, landmark.z), 
		landmarks_list
	)

	return list(landmarks_list)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--pose", type=str, default="open_hand")
	parser.add_argument("--samples", type=int, default=DEFAULT_NUM_SAMPLES)
	args = parser.parse_args()
	main(args)