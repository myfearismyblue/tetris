from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Tuple, List, Optional, Iterable

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
    def __new__(cls, *args, **kwargs):
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
    width: int
    height: int
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

    def __init__(self, state: Optional[IFieldState] = None, **kwargs: int):
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

    def __init__(self, state: Optional[IFigureState] = None, **kwargs: int):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """
        # FIXME: just temporary aggregating of the FieldState behaviour
        if state is None:
            try:
                # should maintain the consistence of [[]] if height is 0
                kwargs['height'] = 1 if kwargs['height'] == 0 else kwargs['height']
                super().__init__([[0] * kwargs['width'] for _ in range(kwargs['height'])])
            except KeyError as e:
                raise TypeError(f'If state is not given, width and height kwargs have to be provided') from e
        else:
            super().__init__(state)


class Field(IField):

    def __init__(self, *, width: int = cfg.FIELD_WIDTH, height: int = cfg.FIELD_HEIGHT, state: IFieldState = None):
        """
        Creates an empty List[List[int]]-like with 'width' and 'height' parameters specified in kwargs,
        or validates a given state
        """
        self.__state = FieldState(state, width=width, height=height)
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






