# Converts a json format cv into a list in a usable format. Updates the custom_indices as it discovers new features if is_training.
def convert_format(cv, custom_indices: dict, is_training):
    # Checks that the CV is in the right format and is not missing any necessary features.
    required_fields = {"Degree Qualification", "Degree Level", "University Attended", "A-Level Qualifications", "Languages Known", "Previous Employment", "Skills", "Hobbies", "Answer Percentage"}
    for field in required_fields:
        if field not in cv:
            raise Exception("Required field: \"{}\" not found in CV: {}".format(field, cv))
    if is_training and "Classification" not in cv:
        raise Exception("Required field: \"Classification\" not found in CV: {}".format(cv))

    # Creates an array of the correct length. If this is during training, then further columns may need to be added.
    formatted_cv = [0] * len(custom_indices)
    # Adds all languages, skills, work experience, and hobbies in the CV to the formatted_cv. Does not add them if it is not training and the feature was not seen in the training data.
    # Sums them so that features not seen in the training data still count for something during predictions as they can be added to the total.
    language_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Languages Known"], "Language", "Expertise")
    other_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Skills"], "Skill", "Expertise")
    experience_total = sum_value(custom_indices, is_training, formatted_cv, cv["Previous Employment"], "Position", "Length of Employment")
    hobby_total = sum_value(custom_indices, is_training, formatted_cv, cv["Hobbies"], "Name", "Interest")

    formatted_cv[custom_indices["Language Skill Total"]] = language_skill_total
    formatted_cv[custom_indices["Other Skill Total"]] = other_skill_total
    formatted_cv[custom_indices["Experience Total"]] = experience_total
    formatted_cv[custom_indices["Hobby Total"]] = hobby_total

    formatted_cv[custom_indices["Answer Percentage"]] = cv["Answer Percentage"]

    return formatted_cv


# Gets the total level for a feature (skills, hobbies etc) and adds missing columns as it goes.
def sum_value(custom_indices: dict, is_training, formatted_cv, feature_list, feature_name, feature_value):
    feature_total = 0

    # Iterates through all known languages or all hobbies etc in the CV.
    for feature in feature_list:
        name = feature[feature_name]
        val = feature[feature_value]
        if not isinstance(val, int):
            raise Exception("\"{}\" must be an integer. Value found for \"{}\" was: {}".format(feature_value, name, val))
        feature_total += val
        # If the feature is already known, then add to it's column for this CV
        if name in custom_indices:
            formatted_cv[custom_indices[name]] += val
        # If the feature has not been seen before, then add it to the model if training. If not, then it will only contribute to the total but not be specifically used by the model.
        else:
            if is_training:
                custom_indices[name] = len(custom_indices)
                formatted_cv.append(val)

    return feature_total
