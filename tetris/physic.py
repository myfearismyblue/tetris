from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Tuple, List, Optional

import tetris.config as cfg


class Key(Enum):
    """List of  keys' names to manage ingame motions and gameplay"""
    LEFTARROW = auto()
    RIGHTARROW = auto()
    UPARROW = auto()


class IFigureState(ABC):
    """Interface for a figure various states"""
    ...


class IFieldState(ABC):
    """
    Interface for game field data structure
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


class IFigure(ABC):
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
    def _current_state(self) -> IFigureState:
        ...

    @property
    @abstractmethod
    def _states(self) -> Dict[Key, IFigureState]:
        """Various possible states have to be provided"""
        ...

    @abstractmethod
    def change_state(self, key: Key):
        pass

    @abstractmethod
    def get_current_state(self):
        pass


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
                super().__init__([[0] * kwargs['width'] for _ in range(kwargs['height'])])
            except KeyError as e:
                raise TypeError(f'If state is not given, width and height kwargs have to be provided') from e
        else:
            super().__init__(state)
