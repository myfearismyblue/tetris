from enum import Enum, auto
from typing import Dict, Callable, Type

from physics import IEvent, IActionEventMapper, IMovementManager


class _MetaDummy(type(IEvent), type(Enum)):
    """Dummy to resolve metaclass conflict while mixin in Event"""
    ...


class Event(IEvent, Enum, metaclass=_MetaDummy):
    """
    Class for all kinds of gameplay user actions which are to be corresponded to a keyboard keys and movement methods
    """
    NO_PENDING_EVENT = 0
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SPEED_UP = auto()
    ROTATE_FIGURE = auto()
    PAUSE_GAME = auto()
    UNPAUSE_GAME = auto()

    @classmethod
    def get_neutral_event(cls) -> IEvent:
        return cls.NO_PENDING_EVENT


class KeyEventMapper:
    """Maps keyboard keys onto events declared in event_cls"""
    def __init__(self, events_cls: Type[IEvent]):
        self._events_cls = events_cls
        self._storage: Dict[str, IEvent] = {'a': events_cls(1),
                                            'd': events_cls(2),
                                            's': events_cls(3),
                                            'w': events_cls(4),
                                            'x': events_cls(5),
                                            'z': events_cls(6),
                                            }
        assert len(self._storage) == len(self._events_cls) - 1   # neutral element doesn't need a key

    def _get_event_by_str(self, name_or_char: str):
        return self._storage[name_or_char]

    def get_event_by_key_or_neutral(self, key):
        """Gets pynput key and tries to fetch char or name.
        Finds char or name in inner _storage and returns corresponding event or neutral if key is not found"""
        try:
            if hasattr(key, 'char'):
                return self._get_event_by_str(name_or_char=key.char)
            elif hasattr(key, 'name'):
                return self._get_event_by_str(name_or_char=key.name)
        except KeyError:
            return self._events_cls.get_neutral_event()


class ActionEventMapper(IActionEventMapper):
    """Maps events declared in events_cls onto movement manager methods.
    To get corresponding to event method use get_action_by_event(event)"""

    def __init__(self, movement_manager: IMovementManager, events_cls: Type[IEvent]):
        self._movement_manager = movement_manager
        self._events_cls = events_cls
        self._storage = {events_cls.get_neutral_event(): lambda: None,
                         events_cls(1): movement_manager._move_left,
                         events_cls(2): movement_manager._move_right,
                         events_cls(3): movement_manager._accelerate,
                         events_cls(4): movement_manager._rotate_figure,
                         events_cls(5): lambda: None,
                         events_cls(6): lambda: None,
                        }

    @property
    def _movement_manager(self) -> IMovementManager:
        return self.__movement_manager

    @_movement_manager.setter
    def _movement_manager(self, val: IMovementManager):
        # TODO: validation here
        self.__movement_manager = val

    @property
    def _events_cls(self) -> Type[IEvent]:
        return self.__events_cls

    @_events_cls.setter
    def _events_cls(self, val: Type[IEvent]):
        # TODO: validation here
        self.__events_cls = val

    def get_action_by_event(self, event: IEvent) -> Callable:
        return self._storage[event]
