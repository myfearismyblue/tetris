from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Tuple, List, Optional, Iterable, Union

import tetris.config as cfg


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
    current_state: Key
    states: Optional[Dict[Key, IFigureState]]

    def __setitem__(self, k, v):
        self.states[k] = v


class IField(ABC):
    @property
    @abstractmethod
    def _width(self) -> int:
        ...

    @property
    @abstractmethod
    def _height(self) -> int:
        ...

    @property
    @abstractmethod
    def _state(self) -> IFieldState:
        ...

    @abstractmethod
    def _update_field_state(self, figure: IFigure):
        pass


class IPhysic(ABC):
    """Interface for game physics managing"""
    @property
    @abstractmethod
    def _field(self) -> IField:
        ...

    @property
    @abstractmethod
    def _figure(self) -> IFigure:
        ...

    @abstractmethod
    def _collision_check(self):
        ...

    @abstractmethod
    def move(self, key: Key):
        ...

    @abstractmethod
    def spawn_figure(self):
        ...

    @abstractmethod
    def get_current_state(self):
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
                # should maintain the consistence of [[]] if height is 0
                kwargs['height'] = 1 if kwargs['height'] == 0 else kwargs['height']
                super().__init__([[0] * kwargs['width'] for _ in range(kwargs['height'])])
            except KeyError as e:
                raise TypeError(f'If state is not given, width and height kwargs have to be provided') from e
        else:
            super().__init__(state)


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
    def _width(self) -> int:
        return self.__width

    @_width.setter
    def _width(self, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Width can not be set with {val}')
        self.__width = val

    @property
    def _height(self) -> int:
        return self.__height

    @_height.setter
    def _height(self, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Height can not be set with {val}')
        self.__height = val

    @property
    def _state(self) -> IFieldState:
        return self.__state

    @_state.setter
    def _state(self, val: IFieldState):
        self.__state = val

    def _update_field_state(self, figure: IFigure):
        """Appends the figure to the field plot"""
        pass


class Figure(IFigure):
    """
    Just the same but concrete representation of interface
    """
    ...


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
        self._figure.states = {}
        self._figure.current_state = Key.__members__[0]
        for key in Key.__members__:
            empty = FigureState(width=width, height=height)
            self.__figure[Key[key]] = empty


    def set_state(self, *, key: Key, state: Union[IFigureState, Iterable[Iterable]]):
        state = FigureState(state)
        self._figure[key] = state
        return

    def set_current_state(self, key: Key):
        assert key in Key
        self._figure.current_state = key

    def get_result(self) -> IFigure:
        return self._figure



