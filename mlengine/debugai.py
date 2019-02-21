import mlengine
import json
from formatting import convert_format


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
    mlengine.train(model, training_data)

    for i in testing_data:
        predicted_class, probability = mlengine.predict(model, i)
        print("\nActual class:", i["Classification"], "\nPredicted class:", predicted_class, "\nCertainty;", probability)


# To convert the 100,000 record cvDataset.json to a 100 record 100cvDataset.json, run reduce_dataset(cvDataset, 100)
def reduce_dataset(dataset: str, n_records: int):
    print("Opening file")
    with open(dataset + ".json", "r") as f:
        print("Reading data")
        raw_data = json.loads(f.read())
    small_data = raw_data[0:n_records]
    small_file_name = str(n_records) + dataset + ".json"
    with open(small_file_name, "w") as f:
        f.write(json.dumps(small_data))
    print(small_file_name, " created")
