import argparse
import time

from cursor import Cursor
from hand_detector import HandDetector
from controller import Controller
from hand_pose_classfier import HandPoseClassifier

def main(args):
	cursor = Cursor()
	hand_detector = HandDetector(
		hand_pose_classifier = HandPoseClassifier(
			model_path="trained_models/random_forest_classifier.pkl"
		)
	)
	controller = Controller(hand_detector, cursor)
	controller.start()

	# while True:
	# 	time.sleep(1)
	# 	cursor.move_rel((1,  0))
	# 	print(cursor.get_position())

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	args = parser.parse_args()
	main(args)