import copy
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional, Iterable, Dict, List, Union

import config as cfg
from .exceptions import OutOfBorderException, ObjectIntersectionException

__all__ = ['Key',
           'IFieldState',
           'IFigureState',
           'IField',
           'IFigure',
           'FieldState',
           'FigureState',
           'Field',
           'Figure',
           'IFigureBuilder',
           'FigureBuilder']


class Key(Enum):
    """List of  keys' names to manage in-game figure states and gameplay"""
    NORMAL = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()

    def next(self, ascending=True):
        """Returns the next element of enumeration. If index is exceeded returns the first element. """
        step = 1 if ascending else -1
        items = list(self.__class__)
        current = items.index(self)
        nxt = (current + step) % len(items)
        return items[nxt]

    def prev(self):
        return self.next(ascending=False)


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
    def __getitem__(self, item):
        ...

    @abstractmethod
    def __setitem__(self, key, val):
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
            is_container = '__getitem__' in dir(state)
            not_flat = '__getitem__' in dir(state[0])
        except IndexError as flat_list_given:
            raise TypeError(f'{state=} should be Iterable[Iterable] but was given a flat iterable') from flat_list_given
        empty = not len(state[0])
        if empty:
            raise ValueError(f'Given state shouldn\'t be empty. {state=}')

        if is_container and not_flat and not empty:
            return  # Supposed that the iterable[] syntax should be provided


        raise TypeError(f'Validation of {state=} is failed. '
                        f'Should be not empty Iterable[Iterable] but was given {type(state)}')

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


class IFigure(ABC):
    """
    Abstract type of any kind of figure that is falling down
    """

    def __setitem__(self, k, v):
        self.states[k] = v

    def __getitem__(self, k):
        return self.states[k]

    def __contains__(self, item):
        try:
            self.states[item]
            return True
        except KeyError:
            return False

    @property
    @abstractmethod
    def current_key(self) -> Optional[Key]:
        ...

    @property
    @abstractmethod
    def states(self) -> Optional[Dict[Key, IFigureState]]:
        ...


    @property
    @abstractmethod
    def width(self) -> int:
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        ...

    @abstractmethod
    def get_current_state(self) -> IFigureState:
        ...

    @abstractmethod
    def get_current_key(self) -> Key:
        ...

    @abstractmethod
    def change_state_by_key(self, key: Key) -> None:
        """Cahnges figure's current state"""
        ...


class IField(ABC):
    @abstractmethod
    def __getitem__(self, item):
        ...

    @abstractmethod
    def __setitem__(self, key, value):
        ...

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
    def make_row_empty(self, idx):
        ...

    @abstractmethod
    def validate_figure_borders(self, figure: IFigure, coords: Iterable[int]):
        ...

    @abstractmethod
    def validate_figure_field_has_no_itersections(self, figure: IFigure, coords: Iterable[int]):
        ...

    @abstractmethod
    def update_field_state(self, figure: IFigure, coords: Iterable[int]):
        pass




class FieldState(List, IFieldState):
    """Type to store a state of a game field"""

    def __init__(self, state: Optional[Union[IFieldState, Iterable[Iterable]]] = None, **kwargs: int):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """
        _validate_dimensions(state, **kwargs)
        if state is None:
            try:
                super().__init__([[0] * kwargs['width'] for _ in range(kwargs['height'])])
            except KeyError as e:
                raise TypeError(f'If state is not given, width and height kwargs have to be provided') from e
        else:
            super().__init__(state)

    def __getitem__(self, item):    # what the hack? why __getitem isnot inherited
        return list(self).__getitem__(item)
    #
    # def __setitem__(self, key, value):
    #     _storeage = list(self)
    #     _storeage.__setitem__(key, value)
    #     self = FieldState(state=_storeage)
    #     print(f'FieldState is {self}')

    def __str__(self):
        ret = ''
        for row in self:
            ret = ''.join((ret, str(row), '\n'))
        return ret

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

        _validate_dimensions(state, **kwargs)
        if state is None:
            state = [[0] * kwargs['width'] for _ in range(kwargs['height'])]

        super().__init__(state)

    def __getitem__(self, item):    # what the hack? why __getitem is not inherited
        return list(self).__getitem__(item)

    @property
    def width(self) -> int:
        return len(self[0])

    @property
    def height(self) -> int:
        return len(self)


def _validate_dimensions(state: Union[IFigureState, IFieldState, Iterable[Iterable], type(None)], **kwargs):
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


class Field(IField):
    def __eq__(self, other):
        return self.state.__eq__(other)

    def __init__(self, *, width: int = cfg.FIELD_WIDTH, height: int = cfg.FIELD_HEIGHT, state: IFieldState = None):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """
        self.__state = FieldState(width=width, height=height) if state is None else FieldState(state)
        self.__width = self.__state.width
        self.__height = self.__state.height

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, row_idx, value):
        self.state[row_idx] = value

    def __str__(self):
        return self.state.__str__()

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def state(self) -> IFieldState:
        return self.__state

    def validate_figure_borders(self, figure: IFigure, coords: Iterable[int]):
        """Validates if a figure opaque points is not located out of fields borders
        if figure is placed to a given coords. If such point is found raises OutOfBorderException."""
        x, y = coords
        figure_state: IFigureState = figure.get_current_state()
        for row_idx in range(figure_state.height):
            for col_idx in range(figure_state.width):
                # check if any opaque point of the figure located out of the field
                point_opaque = figure_state[row_idx][col_idx]
                if not point_opaque:    # in a case point in figure is transparent no action is needed even it's out of
                                        # the field
                    continue
                if (not 0 <= col_idx + x < self.width or
                    not 0 <= row_idx + y < self.height):
                    assert point_opaque
                    raise OutOfBorderException(f'Figure point is out of field: {col_idx, row_idx, point_opaque}.')

    def validate_figure_field_has_no_itersections(self, figure: IFigure, coords: Iterable[int]):
        """Validates if a given figure with coords and field have intersections.
        First uses figure border validation to be sure figure os not out of field"""
        self.validate_figure_borders(figure, coords)    # OoBException shall be raised if figure is out
        x, y = coords
        figure_state: IFigureState = figure.get_current_state()
        for row_idx in range(figure_state.height):
            for col_idx in range(figure_state.width):
                point_opaque = figure_state[row_idx][col_idx]
                if point_opaque and self.state[row_idx + y][col_idx + x]:
                    raise ObjectIntersectionException(f'Figure and field has intersections: \n'
                                                      f'Figure {row_idx=}, {col_idx=} and '
                                                      f'field row_idx={row_idx + y}, el_idx={row_idx + y}')

    def make_row_empty(self, idx: int):
        """Fills row with the given idx with zeros"""
        if isinstance(idx, int) and 0 <= idx < self.height:
            self.state[idx] = [0] * self.width
            return
        raise ValueError(f'Wrong idx is given: {idx=}')

    def update_field_state(self, figure: IFigure, coords: Iterable[int]) -> None:
        """
        Appends the figure to the field plot.
        Checks if figure could be appended to the game field by validating the absense of intersections of filed
        state and figure current state. If so append to the field state.
        :param figure: A figure with certain current_state
        :param coords: Indexes of a column and a row on the field corresponds to left upper corner of the figure
        """

        x, y = coords
        figure_state: IFigureState = figure.get_current_state()
        for row_idx in range(figure_state.height):
            for col_idx in range(figure_state.width):
                # check if any opaque point of the figure located out of the field
                point_opaque = figure_state[row_idx][col_idx]
                if not point_opaque:    # in a case point in figure is transparent no action is needed even it's out of
                                        # the field
                    continue
                if (not 0 <= col_idx + x < self.width or
                    not 0 <= row_idx + y < self.height):
                    assert point_opaque
                    raise OutOfBorderException(f'Figure point is out of field: {col_idx, row_idx}.')

                elif figure_state[row_idx][col_idx] and self.state[row_idx + y][col_idx + x]:
                    assert point_opaque
                    raise ObjectIntersectionException(f'Figure and field has intersections: \n'
                                                      f'Figure {row_idx=}, {col_idx=} and '
                                                      f'field row_idx={row_idx + y}, el_idx={row_idx + y}')
                else:
                    self.state[row_idx + y][col_idx + x] = figure_state[row_idx][col_idx]


class Figure(IFigure):
    """
    Just the same but concrete representation of interface
    """

    def __init__(self, current_key=None, states=None):
        self.current_key = current_key
        self.states = states

    def __str__(self):
        current_key = self.current_key
        state = self.get_current_state()
        ret = '===Current_state===\n'
        for row in state:
            ret = ''.join((ret, str(row), '\n'))
        ret = ''.join((ret, '===Other_states===\n'))
        for key in Key:
            if key is not current_key:
                state = self.states[key]
                for row in state:
                    ret = ''.join((ret, str(row), '\n'))
        ret = ''.join((ret, '==================\n'))
        return ret

    @property
    def current_key(self) -> Optional[Key]:
        if self.__current_key is None:
            raise ValueError(f'Current state of the figure hasn\'t been set.')
        return self.__current_key

    @current_key.setter
    def current_key(self, key: Optional[Key]):
        if key is None or key.name in Key.__members__:
            self.__current_key = key
            return
        raise ValueError(f'Given state has to defined as Key, but was given: {type(key)}')

    @property
    def states(self) -> Optional[Dict[Key, IFigureState]]:
        # if self.__states is None:
        #     raise ValueError(f'States of the figure haven\'t been set.')
        return self.__states

    @states.setter
    def states(self, val: Dict[Key, IFigureState]):
        if val is None:
            self.__states = val
            return
        if not isinstance(val, dict):
            raise ValueError(f'val should be Dict[Key, IFigureState], Given: {val}')
        for item in val.items():
            if item[0] not in Key or not isinstance(item[1], IFigureState):
                raise ValueError(f'Wrong input is given: {item}. Should be Dict[Key, IFigureState].')
        self.__states = val

    @property
    def width(self):
        current_state = self.get_current_state()
        return current_state.width

    @property
    def height(self):
        current_state = self.get_current_state()
        return current_state.height

    def get_current_state(self) -> IFigureState:
        return self.states[getattr(Key,self.current_key.name)]

    def get_current_key(self) -> Key:
        return self.current_key

    def change_state_by_key(self, key: Key):
        if key is None:  # remaining validation is at the setter
            raise ValueError(f'Changing current state to None is not allowed')
        self.current_key = key


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
        self.__figure = Figure(current_key=None, states=None)

    @property
    def _figure(self) -> IFigure:
        if self.__figure.states is None:
            raise ValueError(f'Builder hasn''t been reset. Use reset() and set_state() to build a figure')
        return self.__figure

    @_figure.setter
    def _figure(self, new_fig: Optional[IFigure]) -> None:
        self.__figure = new_fig

    def reset(self, *, width: int, height: int):
        """Resets all keys with given dimensions"""
        self.__figure.states = {}
        self.__figure.current_key = Key(1)
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
        return copy.deepcopy(self._figure)
