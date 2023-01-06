import pytest

from tetris.physic import FieldState


@pytest.mark.parametrize('expected, args, kwargs',
                         [([[]], [[[]]], {}),
                          ([[1, 2, 3], [1, 2, 3]], [[[1, 2, 3], [1, 2, 3]]], {}),  # args[0] == [[1, 2, 3], [1, 2, 3]]
                          ([[0, 0], [0, 0]], [], {'width': 2, 'height': 2}),
                          ([[0, 0], [0, 0]], [], {'state': [[0, 0], [0, 0]]}),
                          ])
def test_FieldState(expected,  args, kwargs):
    assert FieldState(*args, **kwargs) == expected


@pytest.mark.parametrize('expected_exception, args, kwargs',
                         [(TypeError, [], {}),
                          (TypeError, [[]], {}),        # here args[0] = [] so state is flat []
                          (TypeError, [], {'wrong': 1, 'height': 1}),
                          (TypeError, [], {'width': 1, 'wrong': 1}),
                          (TypeError, [[]], {'width': 1, 'height': 1})      # here args[0] = [] so state is flat []
                          ])
def test_FieldState_exceptions(expected_exception, args, kwargs):
    with pytest.raises(expected_exception):
        FieldState(*args, **kwargs)
