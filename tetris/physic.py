from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import random
from typing import Dict, Tuple, List, Optional, Iterable, Union

import tetris.config as cfg


class DomainException(Exception):
    """
    Exception class for business domain
    """


class PhysicException(DomainException):
    """
    Common exception class for in-game physic
    """


class ObjectIntersectionException(PhysicException):
    """
    Raises when two object somehow have mutual intersection in a game field
    """


class Key(Enum):
    """List of  keys' names to manage ingame motions and gameplay"""
    LEFTARROW = auto()
    RIGHTARROW = auto()
    UPARROW = auto()


class IFigureState(ABC):
    """
    Interface for a figure various states.
    Supposed to be nested iterable
    """
    def __new__(cls, *args: Optional[Iterable[Iterable]], **kwargs: Optional[int]):
        """Force check to prove iterable[iterable]"""
        given_state = args[0] if len(args) else None or kwargs.get('state')
        cls._validate_nested_iterable(given_state)
        self = super().__new__(cls)
        return self

    @abstractmethod
    def __getitem__(self):
        ...

    @abstractmethod
    def __setitem__(self):
        ...

    @staticmethod
    def _validate_nested_iterable(state) -> None:
        """
        Throws an exception if a given state is not None neither iterable of iterables
        :param state: List[List]-like array or None
        :return: None
        """
        if state is None:
            return
        try:
            if '__getitem__' in dir(state) and '__getitem__' in dir(state[0]):
                return  # Supposed that the iterable[] syntax should be provided
        except IndexError as flat_list_given:
            raise TypeError(f'{state=} should be Iterable[Iterable] but was given a flat iterable') from flat_list_given

        raise TypeError(f'Validation of {state=} is failed. Should be Iterable[Iterable] but was given {type(state)}')

    @property
    @abstractmethod
    def width(self):
        ...

    @property
    @abstractmethod
    def height(self):
        ...


class IFieldState(IFigureState, ABC):
    """
    Interface for game field data structure
    Supposed to be nested iterable
    """


@dataclass
class IFigure(ABC):
    """
    Abstract type of any kind of figure that is falling down
    """
    current_state: Optional[Key]
    states: Optional[Dict[Key, IFigureState]]

    def __setitem__(self, k, v):
        self.states[k] = v

    def __getitem__(self, k):
        return self.states[k]

    @property
    @abstractmethod
    def width(self):
        ...

    @property
    @abstractmethod
    def height(self):
        ...


    @abstractmethod
    def get_current_state(self):
        ...


class IField(ABC):
    @property
    @abstractmethod
    def width(self) -> int:
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        ...

    @property
    @abstractmethod
    def state(self) -> IFieldState:
        ...

    @abstractmethod
    def update_field_state(self, figure: IFigure, coords: Iterable[int, int]):
        pass

    @abstractmethod
    def validate_figure_coords(self, figure: IFigure, coords: Iterable[int, int]) -> None:
        ...


class FieldState(IFieldState, List):
    """Type to store a state of a game field"""

    def __init__(self, state: Optional[Union[IFieldState, Iterable[Iterable]]] = None, **kwargs: int):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """
        if state is None:
            try:
                super().__init__([[0] * kwargs['width'] for _ in range(kwargs['height'])])
            except KeyError as e:
                raise TypeError(f'If state is not given, width and height kwargs have to be provided') from e
        else:
            super().__init__(state)


    @property
    def width(self) -> int:
        return len(self[0])

    @property
    def height(self) -> int:
        return len(self)


class FigureState(IFigureState, List):
    """Type to store a state of a figure"""

    def __init__(self, state: Union[IFigureState, Iterable[Iterable], type(None)] = None, **kwargs: int):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """

        self. _validate_dimensions(state, **kwargs)
        if state is None:
            state = [[0] * kwargs['width'] for _ in range(kwargs['height'])]

        super().__init__(state)

    def __getitem__(self, item):    # what the hack? why __getitem isnot inherited
        return list(self).__getitem__(item)

    @staticmethod
    def _validate_dimensions(state: Union[IFigureState, Iterable[Iterable], type(None)], **kwargs):
        """
        Validates state to be Iterable[Iterable] and to have non zero  length. If state is not given, then width
        and height have to be provided in kwargs. Raises exceptions if validation is failed.
        :param state:  Iterable of iterable with not zero length
        :param kwargs: width and height should be provided if state hasn't been
        :return None:
        """
        if state is None:
            try:
                _w = kwargs['width']
                _h = kwargs['height']
                if not isinstance(_w, int) or not isinstance(_h, int) or _w <= 0 or _h <= 0:
                    raise ValueError('Dimensions have to be positive integers')
            except KeyError as e:
                raise TypeError(f'If state is not given, width and height kwargs have to be provided') from e
        else:
            try:
                state[0][0]
            except IndexError as empty_list_given:
                raise ValueError(f'State shouldn\'t be empty') from empty_list_given

    @property
    def width(self) -> int:
        return len(self[0])

    @property
    def height(self) -> int:
        return len(self)


class Field(IField):

    def __init__(self, *, width: int = cfg.FIELD_WIDTH, height: int = cfg.FIELD_HEIGHT, state: IFieldState = None):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """
        self.__state = FieldState(width=width, height=height) if state is None else FieldState(state)
        self.__width = len(self.__state[0])
        self.__height = len(self.__state)

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def _width(self, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Width can not be set with {val}')
        self.__width = val

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def _height(self, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Height can not be set with {val}')
        self.__height = val

    @property
    def state(self) -> IFieldState:
        return self.__state

    @state.setter
    def _state(self, val: IFieldState):
        self.__state = val

    def validate_figure_coords(self, figure: IFigure, coords: Iterable[int, int]) -> None:
        """
        Validates if a given figure dimensions are inside the field
        """

        if len(coords) != 2 or not all([isinstance(coords[0], int), isinstance(coords[1], int), ]):
            raise TypeError(f'Wrong figure coords type. Has to be Itetrable[int, int],'
                            f'but was given: {coords}.')
        current_state: IFigureState = figure.get_current_state()
        x, y = coords
        figure_right_and_bottom_edge_in = (0 <= current_state.width - 1 + x < self.width and
                                           0 <= current_state.height - 1 + y < self.height)
        figure_left_and_upper_edge_in = 0 <= x < self.width and 0 <= y < self.height
        if figure_right_and_bottom_edge_in and figure_left_and_upper_edge_in:
            return

        raise ValueError(f'Current state of the figure is out of the field borders. '
                         f'Figure position: {x=}, {y=}. Figure dims: {current_state.width} x {current_state.height}'
                         f'Field dims: {self.width} x {self.height}.')

    def update_field_state(self, figure: IFigure, coords: Iterable[int, int]) -> None:
        """
        Appends the figure to the field plot.
        :param figure: A figure with certain current_state
        :param coords: Indexes of a column and a row on the field corresponds to left upper corner of the figure
        """

        def check_intersection_and_append() -> None:
            """
            Checks if figure could be appended to the game field by validating the absense of intersections of filed
            state and figure current state. If so append to the field state.
            """
            x, y = coords
            figure_state: IFigureState = figure.get_current_state()
            for row_idx in range(figure_state.height):
                for el_idx in range(figure_state.width):
                    if figure_state[row_idx][el_idx] and self.state[row_idx + y][el_idx + x]:
                        raise ObjectIntersectionException(f'Figure and field has intersections: \n'
                                                          f'Figure {row_idx=}, {el_idx=} and '
                                                          f'field row_idx={row_idx + y}, el_idx={row_idx + y}')
                    else:
                        self.state[row_idx + y][el_idx + x] = figure_state[row_idx][el_idx]
        self.validate_figure_coords(figure, coords)
        check_intersection_and_append()


class Figure(IFigure):
    """
    Just the same but concrete representation of interface
    """

    @property
    def width(self):
        return self.get_current_state().width

    @property
    def height(self):
        return self.get_current_state().height


    def get_current_state(self):
        return self.states[self.current_state]


class IFigureBuilder(ABC):
    """
    Abstract builder to create Figures
    """

    @property
    @abstractmethod
    def _figure(self) -> IFigure:
        ...

    @abstractmethod
    def reset(self, *, width, height):
        ...

    @abstractmethod
    def set_state(self, *, key: Key, state: IFigureState):
        ...

    @abstractmethod
    def set_current_state(self, key: Key):
        ...

    @abstractmethod
    def get_result(self) -> IFigure:
        ...


class FigureBuilder(IFigureBuilder):
    def __init__(self):
        self.__figure = Figure(current_state=None, states=None)

    @property
    def _figure(self) -> IFigure:
        if self.__figure.states is None:
            raise ValueError(f'Builder hasn''t been reset. Use reset() and set_state() to build a figure')
        return self.__figure

    @_figure.setter
    def _figure(self, new_fig: Optional[IFigure]) -> None:
        self.__figure = new_fig

    def reset(self, *, width: int, height: int):
        self.__figure.states = {}
        self.__figure.current_state = Key(1)
        for key in Key:
            empty = FigureState(width=width, height=height)
            self.__figure[key] = empty

    def set_state(self, *, key: Key, state: Union[IFigureState, Iterable[Iterable]]) -> None:
        """
        Sets state to the key
        :param key: A key enlisted in Key to which the state stands to
        :param state: Not empty iterable of iterables
        :return: None
        """
        state = FigureState(state)
        self._figure[key] = state

    def set_current_state(self, key: Key):
        """Sets the given key as a figure current state key"""
        assert key in Key
        self._figure.current_state = key

    def get_result(self) -> IFigure:
        return self._figure


class IPhysic(ABC):
    """Interface for game physics managing"""

    @property
    @abstractmethod
    def _field(self) -> IFieldState:
        ...

    @property
    @abstractmethod
    def _available_figures(self) -> Iterable[IFigure]:
        ...

    @property
    @abstractmethod
    def _current_figure(self) -> IFigure:
        ...

    @property
    @abstractmethod
    def _figure_position(self) -> Iterable(int, int):
        ...

    @property
    @abstractmethod
    def input_event(self):
        """Common attr to manage input events, like keyboard pressed etc."""
        ...

    @abstractmethod
    def _collision_check(self):
        ...

    @abstractmethod
    def _move_figure(self, figure: IFigure, coords: Iterable[int, int]):
        ...

    def _rotate_figure(self, figure: IFigure, key: Key):
        ...

    @abstractmethod
    def start_game(self):
        ...

    @abstractmethod
    def stop_game(self):
        ...

    @abstractmethod
    def get_current_field_state(self):
        ...

    @abstractmethod
    def get_current_figure_state(self):
        ...


class Physic(IPhysic):

    def stop_game(self):
        pass

    def __init__(self, *, initial_field: IFieldState, available_figures: Iterable[IFigure], initial_score: int = 0):
        self._field = initial_field     # validation in setter while instancing Field cls
        self._available_figures = available_figures
        self._current_figure = self._random_current_figure()
        self._figure_position = self._random_current_position()
        self._lines_scored: int = initial_score

    @property
    def _field(self) -> IField:
        return self.__field

    @_field.setter
    def _field(self, val: IFieldState):
        self.__field = Field(state=val)

    @property
    def _available_figures(self) -> Iterable[IFigure]:
        return self.__available_figures

    @_available_figures.setter
    def _available_figures(self, val: Iterable[IFigure]):
        if not len(val):
            self.__available_figures = []
            return

        for figure in val:
            break  # FIXME: validate each
            raise ValueError

        self.__available_figures = list(val)

    @property
    def _current_figure(self):
        return self.__current_figure

    @_current_figure.setter
    def _current_figure(self, val: IFigure):
        self.__current_figure = val  # FIXME: validation has to be maintained in Figure entity

    @property
    def _figure_position(self):
        return self.__figure_position

    @_figure_position.setter
    def _figure_position(self, coords: Iterable[int, int]):
        """
        Validates coords input with field.validate_figure_coords.
        Checks if figure and field don't intersect. Sets coords to self.__figure_position.
        """

        self._field.validate_figure_coords(self._current_figure, coords)
        self._check_figure_field_collision()
        self.__figure_position = coords

    @property
    def input_event(self):
        raise NotImplementedError(f'Input events managing hasn''t been implemented yet')

    @input_event.setter
    def input_event(self, event):
        raise NotImplementedError(f'Input events managing hasn''t been implemented yet')

    def _random_current_figure(self):
        return random.choice(self._available_figures)

    def _random_current_position(self) -> Iterable[int, int]:
        figure_width = self._current_figure.width
        field_width = self._field.width
        random_x = random.choice(range(0, field_width - figure_width + 1))
        return random_x, 0

    @staticmethod
    def _collision_check(obj1_coords: Iterable[int, int] = (0, 0), object1: Iterable[Iterable] = None,
                         obj2_coords: Iterable[int, int] = (0, 0), object2: Iterable[Iterable] = None):
        """
        Checks if two 2-dimensional objects has intersections.
        Each object has it's own coords relatively to upper-left corner
        Raises ObjectIntersectionException if intersection is found
        """
        assert object1 and object1[0]
        object1_height = len(object1)
        object1_width = len(object1[0])
        for row_idx in range(object1_height):
            for el_idx in range(object1_width):
                if object1[row_idx + obj2_coords[1]][el_idx + obj2_coords[0]] and object2[row_idx + obj1_coords[1]][el_idx + obj1_coords[0]]:
                    raise ObjectIntersectionException(f'Objects intersect. \n'
                                                      f'Object1 row_idx={row_idx + obj2_coords[1]}, '
                                                      f'el_idx={row_idx + obj2_coords[0]} and '
                                                      f'object2 row_idx={row_idx + obj1_coords[1]}, '
                                                      f'el_idx={row_idx + obj1_coords[0]}')

    def _check_figure_field_collision(self):
        object1 = self._current_figure.get_current_state()
        object2 = self._field.state
        try:
            self._collision_check(obj1_coords=self._figure_position, object1=object1, object2 = object2)
        except ObjectIntersectionException as OIE:
            raise ObjectIntersectionException from OIE  # FIXME: here is another domain type of exceptions is needed

    def _move_figure(self, figure: IFigure,  coords: Iterable[int, int]):
        pass

    def start_game(self):
        pass

    def get_current_field_state(self):
        pass

    def get_current_figure_state(self):
        pass
# fb = FigureBuilder()
# fb.reset(width=2, height=2)
# state = fb._figure[Key.LEFTARROW]
# a = [_ for _ in state]
#
# print((state[0]))
