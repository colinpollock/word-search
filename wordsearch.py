"""Word Search solver

TODO
----
* handle wrap

"""

import itertools
import sys


class Grid(object):

    def __init__(self, grid):
        self.rows = grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0]) if grid else 0

    @staticmethod
    def empty(num_rows, num_cols):
        return Grid([[None for m in xrange(num_cols)] 
                           for n in xrange(num_rows)])

    def __getitem__(self, (m, n)):
        """Return the letter at the mth row and nth column."""
        return self.rows[m][n]

    def letters_at_indices(self, indices):
        """Return the list of chars at these indices."""
        return (self[idx] for idx in indices)


    def word_at_indices(self, indices):
        """Return the word (a str) at these indices."""
        return ''.join(self.letters_at_indices(indices)) #TODO: char by char


    def positions_that_have_letter(self, letter):
        """Return a generator of (m, n) pairs where self[(m, n)] is the letter.
        """
        return ((m, n) for ((m, n), let) in self.index_letter_pairs
                       if let == letter)


    def spans(self, start_index, length, wrap):
        """Return a list of lists of indices of `length` items beginning at 
        `start_index`.
        """
        return itertools.ifilter(None, 
            (self.up_span(start_index, length, wrap),
            self.down_span(start_index, length, wrap),
            self.right_span(start_index, length, wrap),
            self.left_span(start_index, length, wrap),
            self.left_down_span(start_index, length, wrap),
            self.left_up_span(start_index, length, wrap),
            self.right_down_span(start_index, length, wrap),
            self.right_up_span(start_index, length, wrap)))

    def up_span(self, (m, n), length, wrap):
        """Return a generator of length indices starting at (m, n) or None.

        The indices go from bottom to top and can wrap around the grid if wrap
        is True. 
        """

        if length > self.num_rows or (not wrap and m - length + 1 < 0):
            return None

        span = []
        for m_offset in xrange(length):
            m_pos = m - m_offset
            if m_pos < 0:
                m_pos += self.num_rows
            span.append((m_pos, n))
        return span


    def down_span(self, (m, n), length, wrap):
        """Return a generator of length indices starting at (m, n) or None.

        The indices go from top to bottom and can wrap around the grid if wrap
        is True. 
        """

        if length > self.num_rows or (not wrap and m + length > self.num_rows):
            return None

        span = []
        for m_offset in xrange(length):
            m_pos = m + m_offset
            if m_pos >= self.num_rows:
                m_pos -= self.num_rows
            span.append((m_pos, n))
        return span




    def right_span(self, (m, n), length, wrap):
        """Return a generator of length indices starting at (m, n) or None.

        The indices go from left to right and can wrap around the grid if wrap
        is True. 
        """
        if length > self.num_cols or (not wrap and n + length > self.num_cols):
            return None

        span = []
        for n_offset in xrange(length):
            n_pos = n + n_offset
            if n_pos >= self.num_cols:
                n_pos -= self.num_cols
            span.append((m, n_pos))
        return span

    def left_span(self, (m, n), length, wrap):
        """Return a generator of length indices starting at (m, n) or None.

        The indices go from right to left and can wrap around the grid if wrap
        is True.
        """

        if length > self.num_cols or (not wrap and n + length > self.num_cols):
            return None

        span = []
        for n_offset in xrange(length):
            n_pos = n - n_offset
            if n_pos < 0:
                n_pos += self.num_cols
            span.append((m, n_pos))
        return span


    def left_down_span(self, start_index, length, wrap):
        return None #TODO

    def left_up_span(self, start_index, length, wrap):
        return None #TODO
 
    def right_up_span(self, start_index, length, wrap):
        return None #TODO

    def right_down_span(self, start_index, length, wrap):
        return None #TODO

    def __len__(self):
        """Return the number of letter slots in the grid."""
        return self.num_rows * self.num_cols

    def __iter__(self):
        """Return a generator of each letter in the grid."""
        for row in self.rows:
            for item in row:
                yield item

    @property
    def index_letter_pairs(self):
        """Return a generator of ((m, n), letter) pairs.""" 
        for m, row in enumerate(self.rows):
            for n, letter in enumerate(row):
                yield ((m, n), letter)

    def __str__(self):
        return '\n'.join(''.join('*' if item is None else item for item in row) 
                         for row in self.rows)


    def find_words(self, words, wrap):
        """Attempt to find all the input words in the grid.

        For each word, return a pair of positions representing the start and end
        positions of the word. None represents that the word is not in the grid.

        If wrap is True then a word can get to the end of a line and wrap back 
        around.
        """
        return [self.find_word(w, wrap) for w in words]
        

    def find_word(self, word, wrap):
        """Find `word` in the grid.

        Args:
          word: the word to look for
          wrap: bool indicating whether a word can wrap around the grid
        Returns:
          two tuples indicating the start and end position 
        """

        if not word:
            return None

        for m, n in self.positions_that_have_letter(word[0]):
            for span in self.spans((m, n), len(word), wrap):
                if self.word_at_indices(span) == word:
                    return span[0], span[-1]
        return None


class InputParseError(Exception):
    """Raised for malformed input."""

def load_from_str_input(input_str):
    """Load a grid, word list, and +/- wrap from an input string."""
    pat = re.compile(r"""
        \s*
        (?P<rows>\d+)
        [ ]
        (?P<cols>\d+)
        (?P<grid>.*?)
        (?P<wrap>WRAP|NO_WRAP)
        \s+
        (?P<num_words>\d+)
        \s
        (?P<words>.*)
    """, re.VERBOSE|re.DOTALL)

    m = pat.match(input_str)
    if m is None:
        raise InputParseError('Failed to parse input string')

    data = m.groupdict()

    grid = Grid([list(row.strip()) for row in data['grid'].split('\n')
                                   if row.strip()])

    if int(data['rows']) != grid.num_rows or int(data['cols']) != grid.num_cols:
        raise InputParseError("Number of rows or colums doesn't match data")

    words = [line.strip() for line in data['words'].split('\n') if line.strip()]
    if len(words) != int(data['num_words']):
        raise InputParseError("Number of words doesn't match data")

    if data['wrap'] == 'WRAP':
        wrap = True
    elif data['wrap'] == 'NO_WRAP':
        wrap = False
    else:
        raise InputParseError('Wrap instruction must be "WRAP" OR "NO_WRAP"')


    return grid, words, wrap


def main(args):
    test_one()
    pass #TODO: 


if __name__ == '__main__':
    main(sys.argv[1:])
