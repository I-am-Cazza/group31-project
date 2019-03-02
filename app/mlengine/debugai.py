from .mlengine import train, predict
import json
import random


# Train the 'model' on the majority of the data in 'dataset', then test with the last 'n_test_count' records. Returns the classification and probability of the last 'n_test_count' records
# test_run("100cvDataset", "demo", 10)
def test_run(dataset: str, model: str, n_test_count: int):
    print("Retrieving data")
    training_data = list()
    testing_data = list()
    f = open(dataset + ".json", "r")
    raw_data = json.loads(f.read())

    # Adds the last n_test_count elements to the testing data, and each other record to training_data in the correct format
    print("Classifying and adding to datasets")
    i = 0
    size = len(raw_data)
    for cv in raw_data:
        if len(cv["Languages Known"]) > 10:
            cv["Classification"] = "Good"
        elif len(cv["Languages Known"]) > 5:
            cv["Classification"] = "Average"
        else:
            cv["Classification"] = "Bad"
        i += 1
        if i > size - n_test_count:
            testing_data.append(cv)
        else:
            training_data.append(cv)

    print("Training model")
    train(model, training_data)

    for i in testing_data:
        predicted_class = predict(model, i)
        print("\nActual class:", i["Classification"], "\nPredicted class:", predicted_class)


# To convert the 100,000 record cvDataset.json to a 100 record 100cvDataset.json, run reduce_dataset(cvDataset, 100)
def reduce_dataset(dataset: str, n_records: int):
    print("Opening file")
    with open(dataset + ".json", "r") as f:
        print("Reading data")
        raw_data = json.loads(f.read())
        for cv in raw_data:
            update_format(cv)
    small_data = raw_data[0:n_records]
    small_file_name = str(n_records) + dataset + ".json"
    with open(small_file_name, "w") as f:
        f.write(json.dumps(small_data))
    print(small_file_name, " created")


def update_format(cv):
    if "Answer Percentage" not in cv:
        cv["Answer Percentage"] = random.uniform(0, 100)
    for employment in cv["Previous Employment"]:
        employment["Length of Employment"] = years_to_months(employment["Length of Employment"])


# Converts the string X years Y months into the number of months (12X+Y)
def years_to_months(time):  # time is in the format "1 year 5 months"
    if isinstance(time, int):
        return time
    breakdown = time.split(' ')  # breakdown is in the format ['1', 'year', '5', 'months']
    if len(breakdown) <= 1:
        if breakdown == ['']:
            return 0
        else:
            return int(breakdown[0])
    total = 0
    if breakdown[1] == "year" or breakdown[1] == "years":
        total += 12*int(breakdown[0])
        if len(breakdown) == 4:
            total += int(breakdown[2])
    else:
        total = int(breakdown[0])
    return total
