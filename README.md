Word Search
===========

This is a word search solver that finds words in a two dimensional grid. Words
can be in any of these directions:

* left to right
* right to left
* up to down
* down to up
* top left to bottom right
* top right to bottom left
* bottom left to top right
* bottom right to top left

If the wrap flag is True then words can hit an edge of the grid and continue on
the other end.


Approach
---------
The program searches for the words one at a time. In order to find a word the
program finds all the positions in the grid that contain the first letter of the
word. The program then finds all the spans of positions that are the same
length as the word.


The word found at each span is checked against the input word and if they match
then the first and last positions of the span are returned. None is returned if
the word is not found.

Because generators are used throughout the search for each word ends as soon as
it's found. For example, a search for the word 'CAT' that has three separate
"C"s to start at, each of which has 8 spans to check, will only search the first
"C" and that "C"'s first span if the span contains the word.


Running
-------
The first and only argument to wordsearch.py is the path to a file containing 
a grid of letters and a list of words to be searched for.
```python wordsearch.py input_file.txt```


Input File
----------
```
2 2  # The number of rows and columns

AB   # The first row of letters
CD   # The second row of letters

WRAP # "WRAP" or "NO_WRAP"

2    # The number of words

BA   # The words
AD
```


Running Tests
-------------
Use nose to run the tests.

```nosetests tests.py```


Issues
------
* If the grid isn't square it's possible to have a span longer than the number
  of rows or columns but I don't allow that.
