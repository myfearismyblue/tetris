import pytest

from tetris.physic import FieldState, FigureState, FigureBuilder, IFigureBuilder


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
                          ([[]], [], {'width': 0, 'height': 0}),
                          ([[0, 0], [0, 0]], [None], {'width': 2, 'height': 2}),
                          ])
def test_FigureState(expected,  args, kwargs):
    assert FigureState(*args, **kwargs) == expected


@pytest.mark.parametrize('expected_exception, args, kwargs',
                         [(TypeError, [], {}),
                          (TypeError, [[]], {}),        # here args[0] = [] so state is flat []
                          (TypeError, [], {'wrong': 1, 'height': 1}),
                          (TypeError, [], {'width': 1, 'wrong': 1}),
                          (TypeError, [[]], {'width': 1, 'height': 1}),      # here args[0] = [] so state is flat []
                          ])
def test_FigureState_exceptions(expected_exception, args, kwargs):
    with pytest.raises(expected_exception):
        FigureState(*args, **kwargs)


def test_FigureBuilder___init__(dummy_figure_builder: IFigureBuilder):
    assert dummy_figure_builder._FigureBuilder__figure.states is None
    assert dummy_figure_builder._FigureBuilder__figure.width == 0
    assert dummy_figure_builder._FigureBuilder__figure.height == 0


@pytest.mark.parametrize('width, height',
                         [(0, 0),
                          (1, 10),
                          ])
def test_FigureBuilder_reset(width, height, empty_figure_builder: IFigureBuilder):
    assert False


@pytest.mark.parametrize('expected_exception,width, height',
                         [(ValueError, -1, 0),
                          (ValueError, 0, -1),
                          (ValueError, '1', '1'),
                          (ValueError, None, None)
                          ])
def test_FigureBuilder_reset_exceptions(expected_exception, width, height, dummy_figure_builder: IFigureBuilder):
    with pytest.raises(expected_exception):
        dummy_figure_builder.reset(width=width, height=height)


@pytest.mark.parametrize('expected_exception', (ValueError, ))
def test_FigureBuilder_get_result_exception(expected_exception, dummy_figure):
    with pytest.raises(expected_exception):
        FigureBuilder().get_result()