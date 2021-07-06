from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np

from hand_detector import HandType
["fist", "open_hand", "peace_hand", "point_hand", "prosper_hand"]

CLASS_TO_HAND_TYPE = {
	0: HandType.FIST_HAND,
	1: HandType.OPEN_HAND,
	2: HandType.PEACE_HAND,
	3: HandType.LEFT_CLICK_HAND,
	4: HandType.PROSPER_HAND
}

class HandPoseClassifier:
	def __init__(self, model_path, model_type="random_forest_classifier") -> None:
		self.model_type = model_type
		self.model_path = model_path
		self.model = self._load_model()

	def classify(self, landmarks):
		if not isinstance(landmarks, np.ndarray):
			landmarks = self.preprocess(landmarks)

		return self.model.predict(landmarks)

	def preprocess(self, landmarks)->np.ndarray:
		landmarks = list(landmarks.landmark)
		landmark_list = []

		for landmark in landmarks:
			landmark_list.extend([landmark.x, landmark.y, landmark.z])

		return np.array([landmark_list])

	def _load_model(self):
		if self.model_type == "random_forest_classifier":
			return pickle.load(open(self.model_path, "rb"))

		raise Exception("Unhandled model type")

	def class_to_hand_type(self, class_num)->HandType:
		return CLASS_TO_HAND_TYPE[class_num]

if __name__ == "__main__":
	cls = HandPoseClassifier(
		"./trained_models/random_forest_classifier.pkl", 
		"random_forest_classifier"
	)