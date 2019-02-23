from .formatting import convert_format
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy


# Creates or retrains a model. data is a collection of cvs in json form. model_name is the name of the model to train
def train(model_name: str, data: any) -> None:
    training_data = list()
    assessed_data = list()
    custom_indices = {"Language Skill Total": 0, "Other Skill Total": 1, "Experience Total": 2, "Hobby Total": 3}
    for cv in data:
        training_data.append(convert_format(cv, custom_indices, True))
        assessed_data.append(cv["Classification"])

    training_matrix = numpy.zeros((len(training_data), len(custom_indices)))
    for enu, row in enumerate(training_data):
        training_matrix[enu, :len(row)] += row
    training_matrix.tolist()

    n_features = len(training_matrix[0])
    ai_model = RandomForestClassifier(n_estimators=10, max_features=n_features, max_depth=None, min_samples_split=2, n_jobs=-1)
    ai_model.fit(training_matrix, assessed_data)

    with open("aimodels/" + model_name + ".ai", "wb") as file:
        pickle.dump([ai_model, custom_indices], file, pickle.HIGHEST_PROTOCOL)


# Returns the classification of 'cv' according to 'model_name' and a number 0-1 indicating the certainty of the classification.
def predict(model_name: str, cv: any) -> [str, float]:
    with open("aimodels/" + model_name + ".ai", "rb") as file:
        ai_model, custom_indices = pickle.load(file)
        formatted_cv = [convert_format(cv, custom_indices, False)]
        classification = ai_model.predict(formatted_cv)[0]
        index = ai_model.classes_.tolist().index(classification)
        probability = ai_model.predict_proba(formatted_cv)[0][index]
        return [classification, probability]
