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
        with open(dataset_filename, 'rbU') as csv_file:
            reader = csv.reader(csv_file)
            variable_names = reader.next()

            data = OrderedDict((name, []) for name in variable_names)
            for line in reader:
                column = 0
                for name in variable_names:
                    data_point = line[column].strip()
                    if data_point == "":
                        data_point = None
                    data[name].append(data_point)
                    column += 1

            for variable in data:
                self.questions.append(
                    Question(name=variable, data=data[variable], parent_dataset=self)
                )

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

    Initialized with name, a list of responses, and a reference to its parent study.

    """
    def __init__(self, name, data, parent_dataset):
        self.name = name
        self.data = data
        self.parent_dataset = parent_dataset

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Question: {name}".format(name=self.name)

    def __repr__(self):
        return "<{}>".format(self)

    @property
    def sample_size(self):
        """
        Returns an integer representing the number of responses to this
        question
        """
        return len(self.data) - self.data.count(None)

    @property
    def histogram(self):
        """
        returns a dictionary whose keys are strings, the possible responses to
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
                "where_response_equals": ..., # response as string
            }

        Example:
            "Do you have a dog?" is only asked to respondents who answered
            "Yes" to "Do you have pets?".  Calling <Question: "Do you have a
            dog?">'s conditionals method yeilds:
            [
                {
                    "determined_by": <Question: Do you have pets?>
                    "where_response_equals": "Yes"
                }
            ]
        """
        # Make this work!
        raise NotImplementedError('Implement me!')
