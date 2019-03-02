# Converts a json format cv into a list in a usable format. Updates the custom_indices if is_training
def convert_format(cv, custom_indices: dict, is_training):
    required_fields = {"Degree Qualification", "Degree level", "University Attended", "A-Level Qualifications", "Languages Known", "Previous Employment", "Skills", "Hobbies", "Answer Percentage"}
    for field in required_fields:
        if field not in cv:
            raise Exception("Required field: \"{}\" not found in CV: {}".format(field, cv))
    if is_training and "Classification" not in cv:
        raise Exception("Required field: \"Classification\" not found in CV: {}".format(cv))

    formatted_cv = [0] * len(custom_indices)
    language_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Languages Known"], "Language", "Expertise")
    other_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Skills"], "Skill", "Expertise")
    experience_total = sum_value(custom_indices, is_training, formatted_cv, cv["Previous Employment"], "Position", "Length of Employment")
    hobby_total = sum_value(custom_indices, is_training, formatted_cv, cv["Hobbies"], "Name", "Interest")

    formatted_cv[custom_indices["Language Skill Total"]] = language_skill_total
    formatted_cv[custom_indices["Other Skill Total"]] = other_skill_total
    formatted_cv[custom_indices["Experience Total"]] = experience_total
    formatted_cv[custom_indices["Hobby Total"]] = hobby_total

    if "Answer Percentage" not in cv:
        raise Exception("CV does not contain a value for \"Answer Percentage\"")
    formatted_cv[custom_indices["Answer Percentage"]] = cv["Answer Percentage"]

    return formatted_cv


# Gets the total level for a feature (skills, hobbies etc) and adds missing columns as it goes
def sum_value(custom_indices: dict, is_training, formatted_cv, feature_list, feature_name, feature_value):
    feature_total = 0

    for feature in feature_list:
        name = feature[feature_name]
        val = feature[feature_value]
        if feature_value == "Length of Employment" and not isinstance(val, int):
            raise Exception("Length of employment must be an integer. Value found was: {}".format(val))
        feature_total += val
        if name in custom_indices:
            formatted_cv[custom_indices[name]] = val
        else:
            if is_training:
                custom_indices[name] = len(custom_indices)
                formatted_cv.append(val)

    return feature_total
