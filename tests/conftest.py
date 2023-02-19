import pytest

from tetris.physics import Figure, FigureBuilder, IFigureBuilder, IFigure, Key, IPhysicalInteractor, PhysicalInteractor, \
    IField, Field

_FIGURE_WIDTH = 2
_FIGURE_HEIGHT = 2


def FIGURE_WIDTH():
    return _FIGURE_WIDTH


def FIGURE_HEIGHT():
    return _FIGURE_HEIGHT

@pytest.fixture
def filled_field() -> IField:
    return Field(state=[[1, 1, 1], [1, 1, 1], [1, 1, 1] ])


@pytest.fixture
def dummy_figure(width=FIGURE_WIDTH, height=FIGURE_HEIGHT) -> IFigure:
    return Figure(current_key=None, states=None)


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

@pytest.fixture
def dummy_interactor() -> IPhysicalInteractor:
    return PhysicalInteractor()
