"""TODO"""




from nose.tools import nottest

from wordsearch import Grid, load_from_str_input



class TestFindWords(object):
    def setup(self):
        self.grid = Grid([['A', 'B', 'C'],
                          ['D', 'E', 'F'],
                          ['G', 'H', 'I']])

        self.words = ['FED', 'CAB', 'GAD', 'BID', 'HIGH']

    @nottest
    def test_no_wrap(self):
        indices = self.grid.find_words(self.words, False)
        assert indices == [[(1, 2), (1, 0)],
                           None,
                           None,
                           None,
                           None]

    @nottest
    def test_wrap(self):
        indices = self.grid.find_words(self.words, True)
        assert indices == [[(1, 2), (1, 0)],
                           [(0, 2), (0, 1)],
                           [(2, 0), (1, 0)],
                           [(0, 1), (1, 0)],
                           None]


two_by_three = [['C', 'A', 'T'],
                ['N', 'T', 'A']]

class TestFindWord(object):
    def setup(self):
        self.grid = Grid(two_by_three)


    def find(self, word, wrap):
        found = self.grid.find_word(word, wrap)
        return None if found is None else list(found)

    def test_missing(self):
        assert self.find('XYZ', False) is None

    def test_too_long(self):
        assert self.find('CATC', True) is None

    def test_found(self):
        found = self.find('CAT', False)
        print found
        assert found == [(0, 0), (0, 2)]

    def test_found_wrapped(self):
        found = self.find('ANT', True)
        print found
        assert found == [(1, 2), (1, 1)]

    def test_single_letter(self):
        assert self.find('A', True) == [(0, 1), (0, 1)]

    def test_left(self):
        found = self.find('TAC', False) 
        print found
        assert found == [(0, 2), (0, 0)]

    def test_left_wrapped(self):
        assert self.find('NAT', True) == [(1, 0), (1, 1)]


    @nottest
    def test_right_down(self):
        assert self.find('CT', True) == [(0, 0), (1, 1)]

    @nottest
    def test_right_down_wrap(self):
        assert self.find('TC', True) == [(1, 1), (0, 0)]



class TestGridOperations(object):
    def setup(self):
        self.grid = Grid(two_by_three)

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


class TestSpanFinding(object):
    def setup(self):
        self.grid = Grid(two_by_three)

    def test_right_nowrap(self):
        found = list(self.grid.right_span((1, 0), 3, False))
        assert found == [(1, 0), (1, 1), (1, 2)]

    def test_right_wrap(self):
        found = list(self.grid.right_span((0, 2), 3, True))
        assert found == [(0, 2), (0, 0), (0, 1)]

    def test_right_nowrap_nospace(self):
        """Should return None b/c there's not enough space for a span."""
        found = self.grid.right_span((1, 1), 3, False)
        assert found == None

    def test_left(self):
        found = self.grid.left_span((0, 2), 3, False)
        print found
        assert found == [(0, 2), (0, 1), (0, 0)]

    def test_left_wrap(self):
        found = self.grid.left_span((1, 0), 3, True)
        print found
        assert found == [(1, 0), (1, 2), (1, 1)]

    def test_up(self):
        found = self.grid.up_span((1, 0), 2, False)
        print found
        assert found == [(1, 0), (0, 0)]

    def test_up_wrap(self):
        found = self.grid.up_span((0, 0), 2, True)
        assert found == [(0, 0), (1, 0)]

    def test_up_too_long(self):
        assert self.grid.up_span((0, 0), 2, False) is None

    def test_down(self):
        found = self.grid.down_span((0, 0), 2, False)
        assert found == [(0, 0), (1, 0)]

    def test_down_wrap(self):
        found = self.grid.down_span((1, 0), 2, True)
        assert found == [(1, 0), (0, 0)]

    def test_down_too_long(self):
        assert self.grid.down_span((0, 0), 3, False) is None

    def test_down_too_long_with_wrap(self):
        assert self.grid.down_span((0, 0), 3, True) is None

    def test_down_over_end(self):
        assert self.grid.down_span((1, 0), 2, False) is None

    @nottest
    def test_wrap(self):
        found = [list(ob) for ob in (self.grid.spans((0, 0), 2, False))]
        assert len([ob for ob in found if ob is not None]) == 6

    @nottest
    def test_no_wrap(self):
        found = [list(ob) for ob in (self.grid.spans((0, 0), 2, True))]
        assert len([ob for ob in found if ob is not None]) == 3

    def test_right_wrap(self):
        """Should find a span that wraps around the right side."""
        found = list(self.grid.right_span((1, 1), 3, True))
        print found
        assert found == [(1, 1), (1, 2), (1, 0)]

    def test_right_wrap_with_no_space(self):
        """Should return None because a square can't be used twice."""
        found = self.grid.right_span((1, 1), 4, True)
        assert found == None

    def test_str(self):
        assert str(self.grid) == 'CAT\nNTA'


def test_empty_setup():
    """There should be the right number of rows and columns, all None."""
    grid = Grid.empty(4, 3)
    assert grid.num_rows == 4
    assert grid.num_cols == 3
    assert all(item is None for item in grid)


def test_load_from_str_input():
    s = """3 3


ABC


DEF


GHI


WRAP


5


FED


CAB


GAD


BID


HIGH
"""
    grid, words, wrap = load_from_str_input(s)
    assert grid.num_rows == 3
    assert grid.num_cols == 3
    assert words == ['FED', 'CAB', 'GAD', 'BID', 'HIGH']
    assert wrap == True
