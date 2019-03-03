from .formatting import convert_format
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy


# Creates or retrains a model. data is a collection of cvs in json form. model_name is the name of the model to train.
def train(model_name: str, data: any) -> None:
    training_data = list()
    assessed_data = list()
    # custom_indices is a dictionary where keys are the name of the feature, and the values are the column number that will contain the deta for that feature.
    # It is added to every time a new feature is discovered in the data such as a new programming language or skill.
    custom_indices = {"Language Skill Total": 0, "Other Skill Total": 1, "Experience Total": 2, "Hobby Total": 3, "Answer Percentage": 4}
    for cv in data:
        training_data.append(convert_format(cv, custom_indices, True))
        assessed_data.append(cv["Classification"])

    # Creates a rectangular matrix in which every row is a CV, and every column is a feature of the data as described by custom_indices.
    # Features not found in a given CV will have a value of 0 i.e. a CV with no Java skills will have a 0 in the column designated for Java.
    training_matrix = numpy.zeros((len(training_data), len(custom_indices)))
    for enu, row in enumerate(training_data):
        training_matrix[enu, :len(row)] += row

    n_features = len(training_matrix[0])
    ai_model = RandomForestClassifier(
        n_estimators=10,  # The Random Forest model contains 10 decision trees.
        max_features=n_features,  # It considers all features of the data.
        max_depth=None,  # Calculates decision trees to their maximum size so they are maximally effective. There is an acceptable compromise to speed.
        min_samples_split=2,  # Splits a node only if doing so will allow the model to differentiate between at least 2 CVs. This is the minimum and most thorough approach, again with an acceptable compromise to speed.
        n_jobs=-1  # Multi-threading will run as many threads as there are cores in the machine it runs on.
    )
    # Trains the model.
    ai_model.fit(training_matrix, assessed_data)

    # Save the model to file in binary. Also saves custom_indices so that CVs can be put in the correct format to run through the model with the right features.
    with open("./app/mlengine/aimodels/" + model_name + ".ai", "wb") as file:
        pickle.dump([ai_model, custom_indices], file, pickle.HIGHEST_PROTOCOL)


# Returns the classification of 'cv' according to 'model_name'.
def predict(model_name: str, cv: any) -> str:
    with open("./app/mlengine/aimodels/" + model_name + ".ai", "rb") as file:
        ai_model, custom_indices = pickle.load(file)
        # Predictions take an array of inputs, and gice a corresponding array of outputs.
        # As this is only making a prediction for 1 CV, it is given as an array of one CV and the one output is taken from the output array.
        formatted_cv = [convert_format(cv, custom_indices, False)]
        return ai_model.predict(formatted_cv)[0]
