import unittest

import survey


class TestSurvey(unittest.TestCase):
    def test_get_conditionals(self):
        testq = survey.Question("testq1", None, None)
        self.assertRaises(NotImplementedError, testq.get_conditionals)


if __name__ == '__main__':
    unittest.main()
