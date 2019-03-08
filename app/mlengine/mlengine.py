from .formatting import convert_format
from .encodings import Encodings
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy


# Creates or retrains a classifier. data is a collection of cvs in json form. classifier_name is the name of the classifier to train.
def train(classifier_name: str, data: any) -> None:
    training_data = list()
    assessed_data = list()
    # custom_indices is a dictionary where keys are the name of the feature, and the values are the column number that will contain the data for that feature.
    # It is added to every time a new feature is discovered in the data such as a new programming language or skill.
    encodings = Encodings()
    encodings.custom_indices = {"Other Skill Total": 0, "Language Skill Total": 1, "Hobby Total": 2, "A Levels Total": 3, "Experience Total": 4, "Answer Percentage": 5, "Degree Qualification": 6, "Degree Level": 7, "University Attended": 8}
    for cv in data:
        training_data.append(convert_format(cv, encodings, True))
        assessed_data.append(cv["Classification"])

    # Creates a rectangular matrix in which every row is a CV, and every column is a feature of the data as described by custom_indices.
    # Features not found in a given CV will have a value of 0 i.e. a CV with no Java skills will have a 0 in the column designated for Java.
    training_matrix = numpy.zeros((len(training_data), len(encodings.custom_indices)))
    for enu, row in enumerate(training_data):
        training_matrix[enu, :len(row)] += row

    n_features = len(training_matrix[0])
    classifier = RandomForestClassifier(
        n_estimators=10,  # The Random Forest classifier contains 10 decision trees.
        max_features=n_features,  # It considers all features of the data.
        max_depth=None,  # Calculates decision trees to their maximum size so they are maximally effective. There is an acceptable compromise to speed.
        min_samples_split=2,  # Splits a node only if doing so will allow the classifier to differentiate between at least 2 CVs. This is the minimum and most thorough approach, again with an acceptable compromise to speed.
        n_jobs=-1  # Multi-threading will run as many threads as there are cores in the machine it runs on.
    )
    # Trains the classifier.
    classifier.fit(training_matrix, assessed_data)

    # Save the classifier to file in binary. Also saves custom_indices so that CVs can be put in the correct format to run through the classifier with the right features.
    with open("./app/mlengine/classifiers/" + classifier_name + ".ai", "wb") as file:
        pickle.dump([classifier, encodings], file, pickle.HIGHEST_PROTOCOL)


# Returns the classification of 'cv' according to the model 'classifier_name'.
def predict(classifier_name: str, cv: any) -> str:
    with open("./app/mlengine/classifiers/" + classifier_name + ".ai", "rb") as file:
        classifier, encodings = pickle.load(file)
        # Predictions take an array of inputs, and give a corresponding array of outputs.
        # As this is only making a prediction for 1 CV, it is given as an array of one CV and the one output is taken from the output array.
        formatted_cv = [convert_format(cv, encodings, False)]
        return classifier.predict(formatted_cv)[0]
