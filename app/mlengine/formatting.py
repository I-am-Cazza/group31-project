from .encodings import Encodings


# Converts a json format cv into a list in a usable format. Updates the custom_indices as it discovers new features if is_training.
def convert_format(cv: any, encodings, is_training: bool):
    custom_indices = encodings.custom_indices
    uni_encodings = encodings.uni_encodings
    degree_encodings = encodings.degree_encodings
    # Checks that the CV is in the right format and is not missing any necessary features.
    required_fields = {"Degree Qualification", "Degree Level", "University Attended", "A-Level Qualifications", "Languages Known", "Previous Employment", "Skills", "Hobbies", "Answer Percentage"}
    for field in required_fields:
        if field not in cv:
            raise Exception("Required field: \"{}\" not found in CV: {}".format(field, cv))
    if is_training and "Classification" not in cv:
        raise Exception("Required field: \"Classification\" not found in CV: {}".format(cv))

    # Creates an array of the correct length. If this is during training, then further columns may need to be added.
    formatted_cv = [0] * len(custom_indices)
    degree_to_int = {"1st": 5, "2:1": 4, "2:2": 3, "3rd": 2, "Pass": 1}
    formatted_cv[custom_indices["Degree Level"]] = degree_to_int[cv["Degree Level"]]
    formatted_cv[custom_indices["Answer Percentage"]] = cv["Answer Percentage"]
    # Adds all languages, skills, work experience, and hobbies in the CV to the formatted_cv. Does not add them if it is not training and the feature was not seen in the training data.
    # Sums them so that features not seen in the training data still count for something during predictions as they can be added to the total.
    language_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Languages Known"], "Language", "Expertise")
    other_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Skills"], "Skill", "Expertise")
    experience_total = sum_value(custom_indices, is_training, formatted_cv, cv["Previous Employment"], "Position", "Length of Employment")
    hobby_total = sum_value(custom_indices, is_training, formatted_cv, cv["Hobbies"], "Name", "Interest")
    a_level_total = sum_value(custom_indices, is_training, formatted_cv, cv["A-Level Qualifications"], "Subject", "Grade")

    formatted_cv[custom_indices["Language Skill Total"]] = language_skill_total
    formatted_cv[custom_indices["Other Skill Total"]] = other_skill_total
    formatted_cv[custom_indices["Experience Total"]] = experience_total
    formatted_cv[custom_indices["Hobby Total"]] = hobby_total
    formatted_cv[custom_indices["A Levels Total"]] = a_level_total

    degree = cv["Degree Qualification"]
    if degree in degree_encodings:
        formatted_cv[custom_indices["Degree Qualification"]] = degree_encodings[degree]
    elif is_training:
        degree_encodings[degree] = len(degree_encodings)
        formatted_cv[custom_indices["Degree Qualification"]] = degree_encodings[degree]
    else:
        formatted_cv[custom_indices["Degree Qualification"]] = 0

    uni = cv["University Attended"]
    if uni in uni_encodings:
        formatted_cv[custom_indices["University Attended"]] = uni_encodings[uni]
    elif is_training:
        uni_encodings[uni] = len(uni_encodings)
        formatted_cv[custom_indices["University Attended"]] = uni_encodings[uni]
    else:
        formatted_cv[custom_indices["University Attended"]] = 0

    return formatted_cv


# Gets the total level for a feature (skills, hobbies etc) and adds missing columns as it goes.
def sum_value(custom_indices: dict, is_training, formatted_cv, feature_list, feature_name, feature_value):
    grade_to_int = {"A*": 6, "A": 5, "B": 4, "C": 3, "D": 2, "E": 1}
    feature_total = 0

    # Iterates through all known languages or all hobbies etc in the CV.
    for feature in feature_list:
        name = feature[feature_name]
        val = feature[feature_value]
        if feature_value == "Grade":
            if isinstance(val, str):
                val = grade_to_int[val]
        if not isinstance(val, int):
            raise Exception("\"{}\" must be an integer. Value found for \"{}\" was: {}".format(feature_value, name, val))
        feature_total += val
        # If the feature is already known, then add to it's column for this CV.
        if name in custom_indices:
            formatted_cv[custom_indices[name]] += val
        # If the feature has not been seen before, then add it to the classifier if training. If not, then it will only contribute to the total but not be specifically used by the classifier.
        else:
            if is_training:
                custom_indices[name] = len(custom_indices)
                formatted_cv.append(val)

    return feature_total
