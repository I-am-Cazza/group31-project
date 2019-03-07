# Machine Learning Engine
## Overview
The machine learning implementation we are using is a [random forest][randomforest], handled by the [scikit-learn][scikit] package.\
A [random forest][randomforest] works by taking a random subset of the data, and building a decision tree that determines the classification of any given datum in that subset. Each node in the tree splits in whatever way separates the most data with different classifications, and the leaf nodes are the classification of data with attributes which reach that leaf when processed by the decision tree. It then repeats that tree generation process on different random subsets of the data creating many trees, hence forest.\
To determine the classification of a new piece of data, it is processed by each tree individually, then the predicted classification is obtained by having all the trees vote on a classification.\
Our implementation of this is the one in the [scikit-learn][scikit] package. The input must be formatted as a matrix, in which each row is a CV, and each column in an attribute.

## Interface
All operations of the Machine Learning Engine can be accessed through `mlengine.py`.
### mlengine.train
``` python
mlengine.train(classifier_name: str, training_data: Any) -> None
```

| Parameters    |                                   |
| ------------- | --------------------------------- |
| classifier_name    | The name of the classifier to train    |
| training_data | A JSON containing an array of CVs |

#### Description
Trains a random forest classifier based only on the data given in `training_data`, and saves the new classifier as a file under the name given in `classifier_name`. If [`classifier_name`] is already a saved classifier, then it will overwrite that classifier.\
The training data should be a single JSON object containing an array of CVs. Each CV should contain the following information:

- Degree Qualification --- The type of degree the applicant has, i.e.: Computer Science, BSc

- Degree Level --- The level of degree awarded, i.e.: 1:1, 2:1

- University Attended --- The University the applicant attended

- A-Level Qualifications --- A list of JSON objects consisting of the subject title and the grade earned, i.e.: {"Subject": "Computing", "Grade": "A"}, {"Subject": "Mathematics", "Grade": "B"}, {"Subject": "Physics", "Grade": "C"}

- Languages Known --- A list of programming languages the applicant knows. This is a list of JSON objects, consisting of the language name and skill at that language graded from 0-10, with 1 being little experience and 10 being an expert. i.e.: {"Language": "Java", "Expertise": 6}, {"Language": "Python", "Expertise": 8}, {"Language": "C++", "Expertise": 4}

- Previous Employment --- A list of JSON objects detailing previous employment. This includes their position and the length of time they worked. i.e.:{"Position" : "Software Developer", "Length of Employment": "1 year 6 months"}
  
- Skills --- A list of skills outside of pure programming that the applicant may have, again with their expertise rated from 0-10. i.e.:{"Skill":"Excel","Expertise":4},{"Skill":"Public Speaking", "Expertise":7}
  
- Hobbies --- A list of JSON objects detailing hobbies, includes a name and a level of interest rated from 1-10. 1 being barely interested, 10 being very interested. i.e.:{"Name":"Gaming", "Interest":5}, {"Name":"Reading", "Interest":8}, {"Name":"Fencing", "Interest":3}
  
- Answer Percentage --- The percentage of answers the applicant got right in testing. A float in the range 0-100
  
- Classification --- The classification the MLEngine should give this CV, i.e. interview, reject etc. This is only needed in the training data

This differes from the standard CV format given in three ways. First, there is no name. The second is that the names of the companies in Previous Employment are omitted. These are not used as there is no way to get three different data points into one cell of an array. It is fine for the data to contain these, and any other additional features, but not necessary. The third way is the inclusion of a classification. This is needed in the training data, and will be ignored for predictions.

### mlengine.predict
``` python
mlengine.predict(classifier_name: str, cv: Any) -> str
```

| Parameters |                                                     |
| ---------- | --------------------------------------------------- |
| classifier_name | The name of the classifier that will make the prediction |
| cv         | The CV to assess, in JSON format                    |

| Returns   |                                                                        |
| --------- | ---------------------------------------------------------------------- |
| **str**   | The predicted classification given by the classifier                        |

#### Description
Gives a prediction of what classification the CV should fall under e.g. "interview" or "reject". The available classifications are determined by the classifications given in the training data.

## Dependencies
The Machine Learning Engine requires:
- [Python][python] (>= 2.7 or >= 3.4)
- [NumPy][numpy] (>= 1.8.2)
- [SciPy][scipy] (>= 0.13.3)
- [Scikit-learn][scikit]

The Python packages are most easily installed together as `scikit-learn[alldeps]`, using the command `pip install scikit-learn`

## Implementation
For training data, this matrix will contain many rows, as many CVs are needed to train on. For predictions, there will only be one row, the CV being tested.

### Data Format
The first three columns are `totalSkill`, `totalLanguages`, and `totalHobbies`. Each of these is calculated by summing the proficiencies in their category, e.g. somebody with Java at level 8 and Python at level 5 has `totalLanguages` of 13. The fourth column, `totalALevels` is calculated in a similar way, but the letter scores are converted to numbers first. A* is 6, A is 5, B is 4, C is 3, D is 2, and E is 1. The fifth column, `totalExperience` is the summed number of months they have worked as listed under Previous Employment on their CV.\
 Each skill, language, hobby, and A-Level is programmatically assigned its own column. When a new skill, language, hobby, or A-Level is discovered in the training data, a new column is added to the matrix for it. The value in this column shows the proficiency or numeric A-Level grade that row's CV has for that column's feature. CVs lacking that feature will receive a 0 in that column.

 ### Unknown Features in Non-Training Data
 It is likely that CVs sent to the Machine Learning Engine for predictions will sometimes have features not found in the training data, such as new or obscure languages and skills. These will be added to the `totalSkill`, `totalLanguages` and other total variables, but will not be given their own column. This means that the additional skills will be valued as a general increase in skill, but will not be weighted on their own, so will probably be less favoured than those that were already in the training data.

 #### Example CV
| totalSkill | totalLanguages | totalHobbies | totalALevels | totalExperience | Java | Python | Sailing | Public Speaking | C++ | Software Developer | Machine Learning | Tester |
| ---------- | -------------- | ------------ | ------------ | --------------- | ---- | ------ | ------- | --------------- | --- | ------------------ | ---------------- | ------ |
| 10         | 8              | 4            | 15           | 36              | 5    | 2      | 4       | 10              | 0   | 0                  | 0                | 6      |

Skills, languages, hobbies, A Levels, and Experience columns will not necessarily be together, as you can see from the example. Notice also that the total Languages is 8, but the sum of Java, Python, and C++ is only 7. This implies a proficiency of 1 in another language which was not included in the training data. This person also has a total of 36 months of experience, but the total across Software Developer and Tester is only 6. This implies 30 months of experience in jobs that were not included in the training data.




[python]: https://www.python.org/
[scikit]: https://scikit-learn.org/stable/
[numpy]: http://www.numpy.org/
[scipy]: https://www.scipy.org/
[randomforest]: https://en.wikipedia.org/wiki/Random_forest