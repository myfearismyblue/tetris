import pytest

from tetris.physic import Figure, FigureBuilder, IFigureBuilder, IFigure, Key


_FIGURE_WIDTH = 2
_FIGURE_HEIGHT = 2


def FIGURE_WIDTH():
    return _FIGURE_WIDTH


def FIGURE_HEIGHT():
    return _FIGURE_HEIGHT


@pytest.fixture
def dummy_figure(width=FIGURE_WIDTH, height=FIGURE_HEIGHT) -> IFigure:
    return Figure(width=width, height=height, states=None)


@pytest.fixture
def dummy_figure_builder() -> IFigureBuilder:
    return FigureBuilder()


@pytest.fixture
def empty_figure_builder() -> IFigureBuilder:
    return FigureBuilder().reset(width=FIGURE_WIDTH, height=FIGURE_HEIGHT)


@pytest.fixture
def preset_figure_builder() -> IFigureBuilder:
    state = [[1, 1], [0, 0]]
    key = Key(1)
    fb = FigureBuilder()
    fb.reset(width=FIGURE_WIDTH(), height=FIGURE_HEIGHT())
    fb.set_state(key=key, state=state)
    return fb