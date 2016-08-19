"""Template for skip_conditionals

Please treat this as existing code. In short, don't change the API unless
it's required to get the job done.

"""
import csv
from collections import OrderedDict, defaultdict


class SurveyDataSet(object):
    """A single survey's data set.

    Initialized with a single argument, the filename of the CSV data set.

    """
    def __init__(self, dataset_filename):
        # open the data file and create the question objects
        self.questions = []
        with open(dataset_filename) as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)

            question_results = OrderedDict((q_name, []) for q_name in headers)
            # testability could be improved by refactoring this loop to a fn()
            for line in reader:
                column = 0
                for q_name in headers:
                    data_point = line[column].strip()
                    if data_point == "":
                        data_point = None
                    question_results[q_name].append(data_point)
                    column += 1

            for q, res in question_results.items():
                conds = self.get_conditionals(
                    Util.ordered_dict_slice(question_results, q)
                )
                self.questions.append(Question(
                    name=q, data=res, conditionals=conds, parent_dataset=self
                ))

    def get_conditionals(self, question_results):
        """ Return a list of (question, result) tuples which are conditionals.

        Iterate over the given data to determine if None values in the argument
        question results indicate a conditional result.
        """
        last_q_results = question_results.popitem()[1]
        if 0 == last_q_results.count(None):
            return []

        # Do not include RespondentID as a conditional
        question_results.pop("RespondentID", None)

        conditionals = []
        for q, res in question_results.items():
            # copy data into a set and check length to find out if there is
            # more than 1 item in the set - if so, they are not all the same
            if (len(set(res)) <= 1):
                break
            overlay_result = Util.get_conditional_overlay_value(
                res, last_q_results
            )
            if (overlay_result):
                conditionals.append((q, overlay_result))
        return conditionals

    def get_question(self, question_label):
        """Return the question matching the label.

        Raises AttributeError if no matching question exists.

        """
        for question in self.questions:
            if question.name == question_label:
                return question

        raise AttributeError(
            'no question with label "{0}" in data set'.format(question_label)
        )


class Question(object):
    """A single question.

    Initialized with name, list of results, reference to its parent study.

    """
    def __init__(self, name, data, conditionals, parent_dataset):
        self.name = name
        self.data = data
        self.conditionals = conditionals
        self.parent_dataset = parent_dataset

    def __repr__(self):
        return "<{}: {}>".format(type(self).__name__, self.name)

    @property
    def sample_size(self):
        """
        Returns an integer representing the number of results to this
        question
        """
        return len(self.data) - self.data.count(None)

    @property
    def histogram(self):
        """
        returns a dictionary whose keys are strings, the possible results to
        this question and whose values are integers, the count of respondents
        who gave that answer.

        Does not indicate respondents who didn't answer the question.
        """
        histogram = defaultdict(int)
        for data_point in self.data:
            if data_point is None:
                # ignore people who didn't respond
                pass
            else:
                histogram[data_point] += 1
        return histogram

    def get_conditionals(self):
        """
        returns a list of all conditionals which might have been used to
        determine which respondents saw this question.  Each element in the
        list is a dict in the format:
            {
                "determined_by": ..., # instance of question
                "where_result_equals": ..., # result as string
            }

        Example:
            "Do you have a dog?" is only asked to respondents who answered
            "Yes" to "Do you have pets?".  Calling <Question: "Do you have a
            dog?">'s conditionals method yields:
            [
                {
                    "determined_by": <Question: Do you have pets?>,
                    "where_result_equals": "Yes"
                }
            ]

        """
        dict_list = []
        for q, res in self.conditionals:
            dict_list.append(
                {"determined_by": self.parent_dataset.get_question(q),
                 "where_result_equals": res}
            )
        return dict_list


class Util(object):
    """Generic utility functions for data manipulation

    These are inefficient and possibly not very pythonic, but
    they could be safely separated and refactored later as needed.
    """

    @staticmethod
    def ordered_dict_slice(dict, index_stop):
        """ Helper method for slicing an ordered dictionary.

        Accepts string index values
        Does not handle bad data / out of bounds / missing indexes, etc.
        Copying the "slice" is inefficient, but the alternatives I found were
        not simple. Time permitting, I'd revisit. Also put this in a lib"""
        slice = OrderedDict()
        keys = list(dict.keys())
        stop = keys.index(index_stop) + 1
        for i in list(keys[0:stop]):
            slice[i] = dict[i]
        return slice

    @staticmethod
    def get_conditional_overlay_value(list_a, list_b):
        """ Helper method for determing if None values from list_b "overlay"
        a set of unique items in list_a. Returns the complement of the unique
        items from list_a.

        An overlay is defined as a unique value in list_a which
        corresponds 1:1 with None values in list_b in the same list position.
        This function is used to determine "conditionality", meaning the result
        in list_a potentially is one which ended the line of questioning
        in a survey (hence the corresponding None values in list_b).
        """
        # Create the list of overlay candidates
        a_matches = [a for a, b in zip(list_a, list_b) if b is None]
        if not a_matches:
            return None

        # If a_matches contains all of the same values
        if (len(a_matches) != a_matches.count(a_matches[0])):
            return None

        # If >1 result overlays a None value
        if (len(a_matches) != list_a.count(a_matches[0])):
            return None

        # Create a set of all results not corresponding to a None result in b
        all_conds = set(
            [c_val for c_val in list_a if c_val and c_val != a_matches[0]]
        )

        # if > 1 result in the complement of a_matches
        if len(all_conds) != 1:
            # (If we wanted to include all unique results, return all_conds)
            return None

        # All results are the same, pop one off and return it as a scalar
        return all_conds.pop()

if __name__ == '__main__':
    # verify the example output when called via CLI
    dataset = SurveyDataSet("simple_sample.csv")
    dog_q = dataset.get_question("Do you have a dog?")
    print(dog_q.get_conditionals())
