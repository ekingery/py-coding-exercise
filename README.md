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
the question name, the results for that question, and a reference to the
"parent" SurveyDataSet object.

### Pseudocode ###

    foreach survey_result (line in the csv) | O(n)
      foreach question_result (column in the csv) | *O(m)
        build the ordered dictionary (data) | * ((O(1) lookup + O(1) append))
    foreach question in ordered dictionary (column in the csv) | O(m)
      create a new question and append it to the member data list | O(1) append

This solution has a time complexity of `O(n * m)` assuming ordered dictionary 
and list getters and appends are O(1).
[(Reference)](https://wiki.python.org/moin/TimeComplexity)

* n = # of rows (results) in the csv
* m = # of columns (questions) in the csv

Solution Documentation
----------------------
In order to implement `Question.get_conditionals()`, we want to pre-compute and store
the list of Questions which could be determiners for each Question in the survey.

Once this data is stored as class member data (`self.conditionals`),
`get_conditionals()` can be implemented as a simple getter for that data.

### Solution Pseudocode ###

    foreach survey_result (line in the csv) | O(n)
      foreach question_result (column in the csv) | *O(m)
        build the ordered dictionary (data) | *((O(1) lookup + O(1) append))
    foreach question in ordered dictionary (column in the csv) | O(m)
      get_conditionals(ordered dictionary from first to current element) | *O(m * n)
      create a new question and append it to the member data list | O(1) append

    get_conditionals(list of questions): O(m * n)
      if list of results contains no None(s), return | O(n)
      foreach q in dictionary of questions | O(m)
        return if results in q are all the same | O(n)
        conditional_list.append(complement(q, current_q)) | O(n)
      return conditional_list

    complement(list_a, list_b) O(n)
      a_null_matches = result matches from `a` which correspond with None items in `b` | O(n)
      comp_a_null_matches = the complement of a_null_matches | O(n)
      if an item from comp_a_null_matches corresponds to every non-None result 
        and does not appear in the a_null_matches list, we have a conditional

This solution has a time complexity of `O(m^2 * n)` assuming ordered dictionary 
and list getters and appends are O(1).
[(Reference)](https://wiki.python.org/moin/TimeComplexity)

* n = # of rows (results) in the csv
* m = # of columns (questions) in the csv

### Misc. Notes / TODO Time Permitting ###
  * I spent about 3 hours figuring out the current code and the solution
  * I spent about 6 hours writing python code

#### Technical Notes / Concerns ####
* I would be curious to run this against a larger data set, to spot check for
    correctness and to get a sense for real-world runtime
* For the `self.conditional` member data, check that references to the objects are passed / stored,
  as opposed to copies.
  * It looks like references are stored in parent_dataset. I'm assuming we're good
   here but worth further eval if this were production code / I had time to
   learn more about references in python!

#### Python3 Compatibility ####
The first commit (c7a4ffe) contains the updates I found necessary for python3
compatibility. Ordinarily I would include these changes in a separate PR, but 
in this case given I don't have PR access to the originally forked repo. 
The following are my notes (I would typically include these in a PR):

* Removed `unicode` and `str` magic methods no longer necessary in python3
* Tweaked line length to adhere to [PEP-8](https://www.python.org/dev/peps/pep-0008/)
* Simplified the csv open
  * 'r' is default, 'b' is no longer necessary, [U is deprecated](https://docs.python.org/3/library/functions.html#open)
* `__repr__` as written was causing an infinite recursive loop
  * I wonder why?
  * I made the output format match the original implementation, 
   however it seems that using `__str__()` as opposed to `__repr__()`
   might be preferred because `repr()` is suggested to return a 
   [valid python expression](https://docs.python.org/3/library/functions.html#repr)
  * I found the previous two items worth noting, but not worth spending much time on
