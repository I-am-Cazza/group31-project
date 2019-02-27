# Converts a json format cv into a list in a usable format. Updates the custom_indices if is_training
def convert_format(cv, custom_indices: dict, is_training):
    formatted_cv = [0] * len(custom_indices)
    language_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Languages Known"], "Language", "Expertise")
    other_skill_total = sum_value(custom_indices, is_training, formatted_cv, cv["Skills"], "Skill", "Expertise")
    experience_total = sum_value(custom_indices, is_training, formatted_cv, cv["Previous Employment"], "Position", "Length of Employment")
    hobby_total = sum_value(custom_indices, is_training, formatted_cv, cv["Hobbies"], "Name", "Interest")

    formatted_cv[custom_indices["Language Skill Total"]] = language_skill_total
    formatted_cv[custom_indices["Other Skill Total"]] = other_skill_total
    formatted_cv[custom_indices["Experience Total"]] = experience_total
    formatted_cv[custom_indices["Hobby Total"]] = hobby_total

    return formatted_cv


# Gets the total level for a feature (skills, hobbies etc) and adds missing columns as it goes
def sum_value(custom_indices: dict, is_training, formatted_cv, feature_list, feature_name, feature_value):
    feature_total = 0

    for feature in feature_list:
        name = feature[feature_name]
        val = feature[feature_value]
        if feature_value == "Length of Employment":
            val = years_to_months(val)
        feature_total += val
        if name in custom_indices:
            formatted_cv[custom_indices[name]] = val
        else:
            if is_training:
                custom_indices[name] = len(custom_indices)
                formatted_cv.append(val)

    return feature_total


# Gets the sum of all expertise, interest, and experience across all languages, skills, hobbies, and previous jobs
def assess_cv(cv: list):
    return sum(cv[0:4])


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
