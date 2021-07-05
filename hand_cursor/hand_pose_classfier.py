from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np

class HandPoseClassifier:
	def __init__(self, model_path, model_type="random_forest_classifier") -> None:
		self.model_type = model_type
		self.model_path = model_path
		self.model = self._load_model()

	def classify(self, landmarks):
		if not isinstance(landmarks, np.ndarray):
			landmarks = self.preprocess(landmarks)

	def preprocess(self, landmarks)->np.ndarray:
		pass

	def _load_model(self):
		if self.model_type == "random_forest_classifier":
			return pickle.load(open(self.model_path, "rb"))

		raise Exception("Unhandled model type")


if __name__ == "__main__":
	cls = HandPoseClassifier("./trained_models/random_forest_classifier.pkl", "random_forest_classifier")