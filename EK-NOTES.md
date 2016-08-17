Eric K - Notes on Skip Patterns Exercise
========================================

Existing Survey Data Set and Question Object Documentation
----------------------------------------------------------
The SurveyDataSet object takes a CSV in its constructor. __init__() parses every line 
and builds an
[OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict) 
containing the questions as keys to a list of data points (values / answers).

Once the data has been parsed into the ordered dictionary, the dictionary is
iterated on, creating a list of new Question objects. A Question object stores
the question name, the responses for that question, and a reference to the
"parent" SurveyDataSet object.

### Pseudocode ###

    foreach survey_response (line in the csv)
      foreach question_response (column in the csv)
        build the ordered dictionary (data)
    foreach question in ordered dictionary (data)
      self.questions.append(Question(question_name, [res1, res2, res3], self)))

Solution Documentation
----------------------
In order to implement `get_conditionals()`, we want to pre-compute and store
the list of Questions which could be determiners for each Question in the survey.

Once this data is stored as class member data (`self.conditionals`),
`get_conditionals()` can be implemented as a simple getter for that data.

### Solution Pseudocode ###
This solution has a time complexity of `O(n^2)`

    foreach survey_response (line in the csv)
      foreach question_response (column in the csv)
        build the ordered dictionary (data)
    foreach question in ordered dictionary (data)
      determinants = self.get_determinants()
      self.questions.append(
        Question(question_name, [res1, res2, res3], determinants, self)
      )

    def get_determinants(self):
      if list of results contains None(s)
        foreach q in list of questions from 0:current
          if results in q are not all the same
            'overlay' q and current_q
            1. does every None result in current_q correspond to the same response in q?
              - if no, we do not have a determinant
              - if yes, we have a determinant candidate
                2. Is response in q = the response to any non None responses in current_q?
                - if yes, we do not have a determinant
                - if no, we have a determinant
                  returnval.append(q) 
      return returnval

### Misc. Notes ###
* For the `self.conditional` member data, check that references to the objects are passed / stored,
  as opposed to copies.
 * It looks like references are stored in parent_dataset. I"m assuming we're good
   here but worth further eval if this were production code / I had time to
   learn more about references in python!


Python3 Compatibility
---------------------
The first commit (c7a4ffe) contains the updates I found necessary for python3
compatibility. Ordinarily I would include these changes in a separate PR, but 
in this case given I don't have PR access to the originally forked repo. 
Instead I isolated them in the first commit so they can be cherry-picked if you find them 
worthwhile to include in the main [skip patterns repo](https://bitbucket.org/knowledgehound/skip_patterns). 
The following are my notes (I'd include these in the PR):

* Removed `unicode` and `str` magic methods no longer necessary in python3
* Tweaked line length to adhere to [PEP-8](https://www.python.org/dev/peps/pep-0008/)
* Simplified the csv open
 * 'r' is default, 'b' is no longer necessary, [U is deprecated](https://docs.python.org/3/library/functions.html#open)
* `__repr__` as written was causing an infinite recursive loop
 * I'm curious as to the reason for this
 * I made the output format match the original implementation, 
   however it seems that using `__str__()` as opposed to `__repr__()`
   might be preferred because `repr()` is suggested to return a 
   [valid python expression](https://docs.python.org/3/library/functions.html#repr)
 * I found the previous two items worth noting, but not worth spending much time on

