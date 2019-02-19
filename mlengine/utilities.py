import json


class Utilities:

    def __init__(self):
        self.nextIndex = 4
        self.customIndices = dict()

    # Returns a formatted list of i cvs in cvDataset.json as testing_data, and the rest as training_data in the format (training_data, testing_data)
    def get_data(self, n_testing):
        training_data = list()
        testing_data = list()
        f = open("cvDataset.json", "r")
        raw_data = json.loads(f.read())

        # Adds the first i elements to the testing data, then each other record to training_data in the correct format
        i = 0
        size = len(raw_data)
        for cv in raw_data:
            i += 1
            if i > size - n_testing:
                testing_data.append(self.convert_format(cv, False))
            else:
                training_data.append(self.convert_format(cv, True))
        return training_data, testing_data

    # Converts a json format cv into an array
    def convert_format(self, x, is_training):
        formatted_cv = [0] * self.nextIndex
        language_skill_total = self.sum_value(is_training, formatted_cv, x["Languages Known"], "Language", "Expertise")
        other_skill_total = self.sum_value(is_training, formatted_cv, x["Skills"], "Skill", "Expertise")
        experience_total = self.sum_value(is_training, formatted_cv, x["Previous Employment"], "Position", "Length of Employment")
        hobby_total = self.sum_value(is_training, formatted_cv, x["Hobbies"], "Name", "Interest")

        formatted_cv[0] = language_skill_total
        formatted_cv[1] = other_skill_total
        formatted_cv[2] = experience_total
        formatted_cv[3] = hobby_total

        return formatted_cv

    def sum_value(self, is_training, formatted_cv, feature_list, feature_name, feature_value):
        feature_total = 0
        for feature in feature_list[feature_name]:
            name = feature[feature_name]
            val = feature[feature_value]
            if feature_value == "Length of Employment":
                val = self.years_to_months(val)
            feature_total += val
            if name in self.customIndices:
                formatted_cv[self.customIndices[name]] = val
            else:
                if is_training:
                    self.customIndices[name] = self.nextIndex
                    self.nextIndex += 1
                    formatted_cv.append(val)
        return feature_total

    # Gets the sum of all expertise across all languages and skills
    def assess_cv(self, cv: list):
        return sum(cv[0:4])

    def years_to_months(self, time: str):  # time is in the format "1 year 5 months"
        breakdown = time.split(' ')  # breakdown is in the format ['1', 'year', '5', 'months']
        if len(breakdown) == 0:
            return 0
        
        total = 0
        if breakdown[1] == "year" or breakdown[1] == "years":
            total += 12*int(breakdown[0])
            if len(breakdown) == 4:
                total += int(breakdown[2])
        else:
            total = int(breakdown[0])

        return total