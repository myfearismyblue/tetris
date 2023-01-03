from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


class Key(Enum):
    """List of  keys' names to manage ingame motions and gameplay"""
    ...


class IFigureState(ABC):
    """Interface for a figure various states"""
    ...


class IFieldState(ABC):
    """Interface for game field data structure"""
    ...


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
    def _state(self) -> IFigureState:
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


