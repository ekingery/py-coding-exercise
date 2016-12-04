import unittest
import survey
from collections import OrderedDict


class TestSurvey(unittest.TestCase):
    """Test the SurveyDataSet and Question classes"""

    sample_dataset = survey.SurveyDataSet("simple_sample.csv")
    D = OrderedDict()
    D["Gender"] = ["M", "F", "F", "M", "F", "F"]
    D["What is your favorite color?"] = [
        "Red", "Blue", "Yellow", "Red", "Blue", "Red"
    ]
    D["Do you have pets?"] = ["Yes", "No", "Yes", "Yes", "No", "Yes"]
    D["Do you have free will?"] = ["No", "No", "No", "No", "No", "No"]
    D["What kinds of pets do you have?"] = [
        ["Dog", "Cat"], None, ["Dog"], ["Fish"], None, ["Dog", "Fish"]
    ]
    D["Where do you shop for pet food?"] = [
        "Petco", None, "PetSmart", "PetSmart", None, "Petco"
    ]
    D["Do you visit dog parks?"] = ["Yes", None, "No", None, None, "Yes"]
    D["Where do you shop for groceries?"] = [
        "Jewel", "Jewel", "Marianos", "Whole Foods", "Jewel", "Marianos"
    ]

    def test_ordered_dict_slice(self):
        # hack / shortcut to constructing inline
        expected_test_result = OrderedDict()
        expected_test_result["Gender"] = ["M", "F", "F", "M", "F", "F"]
        expected_test_result["What is your favorite color?"] = [
            "Red", "Blue", "Yellow", "Red", "Blue", "Red"
        ]
        self.assertDictEqual(
            survey.Util.ordered_dict_slice(
                TestSurvey.D, "What is your favorite color?"),
            expected_test_result
        )

    def test_get_conditional_complements(self):
        kinds_of_pets = [
            ["Dog", "Cat"], None, ["Dog"], ["Fish"], None, ["Dog", "Fish"]
        ]
        gender = ["M", "F", "F", "M", "F", "F"]
        have_pets = ["Yes", "No", "Yes", "Yes", "No", "Yes"]
        self.assertEqual([], survey.Util.get_conditional_complements(
            gender, kinds_of_pets
        ))
        self.assertEqual(["Yes"], survey.Util.get_conditional_complements(
            have_pets, kinds_of_pets
        ))

    def test_survey_data_get_conditionals(self):
        sd = TestSurvey.sample_dataset
        sample_data_slice1 = survey.Util.ordered_dict_slice(
            TestSurvey.D, "What is your favorite color?"
        )
        sample_data_slice2 = survey.Util.ordered_dict_slice(
            TestSurvey.D, "What kinds of pets do you have?"
        )
        # test case where current set of data contains no Nones
        self.assertEqual(
            [], sd.get_conditionals(sample_data_slice1)
        )
        # test case where there is a conditional match
        self.assertEqual(
            [("Do you have pets?", ["Yes"])],
            sd.get_conditionals(sample_data_slice2)
        )

    def test_question_get_conditionals(self):
        dog_q = TestSurvey.sample_dataset.get_question("Do you have a dog?")
        c_answer = TestSurvey.sample_dataset.get_question("Do you have pets?")
        self.assertEqual(
            [{"determined_by": c_answer, "where_result_equals": "Yes"}],
            (dog_q.get_conditionals())
        )
        self.assertEqual([], c_answer.get_conditionals())

    def test_skip_patterns_interview_data(self):
        dataset = survey.SurveyDataSet("skip_patterns_interview_sample.csv")
        pets_q = dataset.get_question("Do you have pets?")
        pet_kinds_q = dataset.get_question("What kinds of pets do you have?")
        pet_food_q = dataset.get_question("Where do you shop for pet food?")
        dog_parks_q = dataset.get_question("Do you visit dog parks?")
        grocery_q = dataset.get_question("Where do you shop for groceries?")

        self.assertEqual([], pets_q.get_conditionals())
        self.assertEqual(
            [{'determined_by': pet_kinds_q, 'where_result_equals': 'Dog'}],
            dog_parks_q.get_conditionals()
        )
        self.assertEqual([], grocery_q.get_conditionals())
        self.assertEqual(
            [{"determined_by": pets_q, "where_result_equals": "Yes"}],
            (pet_kinds_q.get_conditionals())
        )
        self.assertEqual(
            [{"determined_by": pets_q, "where_result_equals": "Yes"}],
            (pet_food_q.get_conditionals())
        )


if __name__ == '__main__':
    unittest.main()
