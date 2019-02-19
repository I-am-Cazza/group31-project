from sklearn.model_selection import cross_val_score
import trainer
from utilities import Utilities

# The number of cvs to use as testing data instead of training data
n_test_count = 10
util = Utilities()
print("Retrieving data")
training_data, testing_data = util.get_data(n_test_count)

print("Generating actual scores")
assessed_data = list()
for cv in training_data:
    score = util.assess_cv(cv)
    assessed_data.append(score)

print("Training model")
model = trainer.get_model(training_data, assessed_data)

print("Assessing model")
scores = cross_val_score(model, training_data, assessed_data, cv=5)
print(scores.mean())
predictions = model.predict(testing_data)

for i in range(n_test_count):
    print("Predicted value: ", predictions[i], "\nActual value:", util.assess_cv(testing_data[i]))
