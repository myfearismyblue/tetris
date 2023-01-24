import pytest

from tetris.physic import FieldState, FigureState, FigureBuilder, IFigureBuilder, Key


@pytest.mark.parametrize('expected, args, kwargs',
                         [([[]], [[[]]], {}),
                          ([[1, 2, 3], [1, 2, 3]], [[[1, 2, 3], [1, 2, 3]]], {}),  # args[0] == [[1, 2, 3], [1, 2, 3]]
                          ([[0, 0], [0, 0]], [], {'width': 2, 'height': 2}),
                          ([[0, 0], [0, 0]], [], {'state': [[0, 0], [0, 0]]}),
                          ([[]], [], {'width': 0, 'height': 0}),
                          ([[0, 0], [0, 0]], [None], {'width': 2, 'height': 2}),
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


@pytest.mark.parametrize('expected, args, kwargs',
                         [([[1, 2, 3], [1, 2, 3]], [[[1, 2, 3], [1, 2, 3]]], {}),  # args[0] == [[1, 2, 3], [1, 2, 3]]
                          ([[0, 0], [0, 0]], [], {'width': 2, 'height': 2}),
                          ([[0, 0], [0, 0]], [], {'state': [[0, 0], [0, 0]]}),
                          ([[0, 0], [0, 0]], [None], {'width': 2, 'height': 2}),
                          ])
def test_FigureState(expected,  args, kwargs):
    assert FigureState(*args, **kwargs) == expected


@pytest.mark.parametrize('expected_exception, args, kwargs',
                         [(TypeError, [], {}),
                          (TypeError, [[]], {}),        # here args[0] = [] so state is flat []
                          (ValueError, [[[]]], {}),
                          (TypeError, [], {'wrong': 1, 'height': 1}),
                          (TypeError, [], {'width': 1, 'wrong': 1}),
                          (TypeError, [[]], {'width': 1, 'height': 1}),      # here args[0] = [] so state is flat []
                          (ValueError, [], {'width': -1, 'height': -1}),
                          ])
def test_FigureState_exceptions(expected_exception, args, kwargs):
    with pytest.raises(expected_exception):
        FigureState(*args, **kwargs)


def test_FigureBuilder___init__(dummy_figure_builder: IFigureBuilder):
    assert dummy_figure_builder._FigureBuilder__figure.states is None
    assert dummy_figure_builder._FigureBuilder__figure.current_state is None


@pytest.mark.parametrize('expected, width, height',
                         [([1, 1], 1, 1),
                          ([10, 1], 1, 10),
                          ])
def test_FigureBuilder_reset(expected, width, height, dummy_figure_builder: IFigureBuilder):
    fb = dummy_figure_builder
    fb.reset(width=width, height=height)
    for key in Key:
        state = fb._figure[key]
        assert len(state) == expected[0] == state.height
        assert len(state[0]) == expected[1] == state.width
    assert len(fb._figure.states) == len(Key)


def test_FigureBuilder_get_result(preset_figure_builder):
    res = preset_figure_builder.get_result()
    assert res[Key(1)][0][0] == 1
    assert res[Key(1)][0][1] == 1
    assert res[Key(1)][1][0] == 0
    assert res[Key(1)][1][1] == 0


@pytest.mark.parametrize('expected_exception', (ValueError, ))
def test_FigureBuilder_get_result_exception(expected_exception, dummy_figure):
    with pytest.raises(expected_exception):
        FigureBuilder().get_result()