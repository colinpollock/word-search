"""Word Search solver for Factual code test.

TODO
----
* handle wrap

"""



class Grid(object):

    def __init__(self, grid):
        self._grid = grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0]) if grid else 0

    @staticmethod
    def empty(num_rows, num_cols):
        return Grid([[None for m in xrange(num_cols)] 
                           for n in xrange(num_rows)])



    def __getitem__(self, (m, n)):
        """Return the letter at the mth row and nth column."""
        return self._grid[m][n]


    def letters_at_indices(self, indices):
        """Return the list of chars at these indices."""
        return [self[idx] for idx in indices]


    def word_at_indices(self, indices):
        """Return the word (a str) at these indices."""
        return ''.join(self.letters_at_indices(indices))


    def positions_that_have_letter(self, letter):
        """Return a generator of (m, n) pairs where self[(m, n)] is the letter.
        """
        return ((m, n) for ((m, n), let) in self.index_letter_pairs
                       if let == letter)


    def spans(self, start_index, length, wrap):
        """Return a list of lists of indices of `length` items beginning at 
        `start_index`.
        """
        #TODO


    def __iter__(self):
        """Return a generator of each letter in the grid."""
        for row in self._grid:
            for item in row:
                yield item

    @property
    def index_letter_pairs(self):
        """Return a generator of ((m, n), letter) pairs.""" 
        for m, row in enumerate(self._grid):
            for n, this_letter in enumerate(row):
                if letter == this_letter:
                    yield (m, n)

    def __repr__(self):
        pass #TODO

    def find_words(self, words):
        """For each word return a list of (m, n) indices where it's found or 
        None if it isn't in the grid.
        """
        return [find_word(w) for w in words]
        

    def find_word(self, word):
        if not word:
            return None

        for m, n in self.positions_that_have_letter(word[0]):
            for span in self.spans((m, n), len(word)):
                if self.word_at_indices(span) == word:
                    return span

        return None





def load_from_str_input(input_str):
    pass #TODO


def test_one():
    grid = Grid(

def main(args):
    test_one()
    pass #TODO: 


if __name__ == '__main__':
    main(sys.argv[1:])
