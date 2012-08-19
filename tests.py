"""TODO"""


from wordsearch import Grid

class TestGridOperations(object):
    def setup(self):
        data = [['C', 'A', 'T'],
                ['N', 'T', 'A']]
        self.grid = Grid(data)

    def test_num_row_and_cols(self):
        assert self.grid.num_rows == 2
        assert self.grid.num_cols == 3

    def test_getitem(self):
        assert self.grid[0, 1] == 'A'


    def test_letters_at_indices(self):
        found = list(self.grid.letters_at_indices([(0, 1), (0, 2)]))
        assert found == ['A', 'T']

    def test_word_at_indices(self):
        found = self.grid.word_at_indices([(0, 1), (0, 2)])
        print found
        assert found == 'AT'


    def test_positions_that_have_letter(self):  
        found = list(self.grid.positions_that_have_letter('T'))
        print found
        assert found == [(0, 2), (1, 1)]

    def test_iter(self):
        found = list(iter(self.grid))
        assert found == ['C', 'A', 'T', 'N', 'T', 'A']

    def test_index_letter_pairs(self):
        found = list(self.grid.index_letter_pairs)
        print found
        assert found == [((0, 0), 'C'), ((0, 1), 'A'), ((0, 2), 'T'),
                         ((1, 0), 'N'), ((1, 1), 'T'), ((1, 2), 'A')]


    ############################################################################
    # TESTING Spans
    def test_right_span_nowrap(self):
        found = list(self.grid.right_span((1, 0), 3, False))
        assert found == [(1, 0), (1, 1), (1, 2)]

    def test_right_span_nowrap_nospace(self):
        """Should return None b/c there's not enough space for a span."""
        found = self.grid.right_span((1, 1), 3, False)
        assert found == None

    def test_right_span_wrap(self):
        found = list(self.grid.right_span((0, 2), 3, True))
        assert found == [(0, 2), (0, 0), (0, 1)]

    def test_right_span_nowrap_nospace(self):
        """Should return None b/c there's not enough space for a span."""
        found = list(self.grid.right_span((1, 1), 3, False))
        assert found == None

    def test_spans(self):
        found = list(self.grid.spans((0, 0), 2, False))
        assert len(filter(None, found)) == 2


def test_empty_setup():
    """There should be the right number of rows and columns, all None."""
    grid = Grid.empty(4, 3)
    assert grid.num_rows == 4
    assert grid.num_cols == 3
    assert all(item is None for item in iter(grid))
