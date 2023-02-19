import copy
import random
from abc import ABC, abstractmethod
from time import sleep
from typing import Iterable, Optional, Type, Callable, List

import config as cfg
from .exceptions import ObjectIntersectionException, FigureIsToBeAppended, OutOfBorderException
from .entities import IFieldState, IField, IFigure, Key, Field

__all__ = ['IPhysicalInteractor',
           'IMovementManager',
           'PhysicalInteractor',
           'MovementManager',
           'IEvent',
           'IActionEventMapper'
           ]


class IPhysicalInteractor(ABC):
    """Interface for game objects interaction."""
    @property
    @abstractmethod
    def _field(self) -> IFieldState:
        ...

    @property
    @abstractmethod
    def _current_figure(self) -> IFigure:
        ...

    @property
    @abstractmethod
    def _figure_position(self) -> Iterable[int]:
        ...

    @property
    @abstractmethod
    def lines_scored(self):
        ...

    @abstractmethod
    def place_figure(self, figure: IFigure, coords: Iterable[int]):
        ...

    @abstractmethod
    def change_figure_state(self, key: Key):
        ...

    @abstractmethod
    def update_field_state(self):
        """Updates current field with current figure"""
        ...

    @abstractmethod
    def get_current_field_state(self):
        ...

    @abstractmethod
    def get_current_figure(self):
        ...

    @abstractmethod
    def get_current_figure_pos(self) -> Iterable[int]:
        ...

    @abstractmethod
    def map_figure_to_field(self):
        ...

    @abstractmethod
    def count_and_clear_lines(self):
        ...


class PhysicalInteractor(IPhysicalInteractor):
    """
    Game objects interaction.
    Contains field, figure and it's position attributes
    Can place a figure in certain coords.
    If interaction is occurred rises exceptions
    """

    def __init__(self, *, initial_field: IFieldState = Field(),
                 initial_scored_lines: Iterable[int] = None):
        self._field = initial_field     # validation in setter while instancing Field cls
        self._current_figure = None
        self._figure_position = None
        self.lines_scored: Iterable[int] = [] if initial_scored_lines is None else initial_scored_lines

    @property
    def _field(self) -> IField:
        return self.__field

    @_field.setter
    def _field(self, val: IFieldState):
        self.__field = Field(state=val)

    @property
    def _current_figure(self) -> IFigure:
        if self.__current_figure is None:
            raise ValueError(f'Figure is not set')
        return self.__current_figure

    @_current_figure.setter
    def _current_figure(self, val: Optional[IFigure]):
        if val is None:
            pass
        self.__current_figure = val  # FIXME: validation has to be maintained in Figure entity

    @property
    def _figure_position(self) -> Iterable[int]:
        if self.__figure_position is None:
            raise ValueError('Figure position is not set')
        return self.__figure_position

    @_figure_position.setter
    def _figure_position(self, coords: Optional[Iterable[int]]):
        """
        Validates coords input with field.validate_figure_coords.
        Checks if figure and field don't intersect. Sets coords to self.__figure_position.
        """
        if coords is not None:
            self._field.validate_figure_borders(self._current_figure, coords)
            self._field.validate_figure_field_has_no_itersections(self._current_figure, coords)
        self.__figure_position = coords

    @property
    def lines_scored(self) -> List[List[int]]:
        assert self.__lines_scored is not None
        return self.__lines_scored

    @lines_scored.setter
    def lines_scored(self, val: List[List[int]]):
        if not isinstance(val, List):
            raise ValueError(f'Initial score hasn\'t been set correctly: {val}')
        if len(val) and len(val[0]) and not all([isinstance(item, int) for item in val[0]]):
            raise ValueError(f'Initial scores has to be integers: {val}')
        self.__lines_scored = val

    def count_and_clear_lines(self) -> Iterable[int]:
        """
        Finds all filled rows at a current field state. Removes those rows, offsets remaining part of the field
        and return iterable of lines separately removed, for example: [1, 1, 2] means that was found two single
        separated lines and two glued lines
        """
        rows_found = []  # store here idx of rows found
        sequence_found = []

        def count_lines():
            nonlocal sequence_found
            sequence_counter = 0
            for row_idx, row in enumerate(self._field):
                if all(row):
                    sequence_counter += 1
                    rows_found.append(row_idx)
                else:
                    sequence_found.append(sequence_counter) if sequence_counter else None
                    sequence_counter = 0
            sequence_found.append(sequence_counter) if sequence_counter else None

        def clear_lines():
            nonlocal rows_found
            for current_row_idx in rows_found:
                for row_idx in range(current_row_idx - 1, -1, -1):
                    self._field[row_idx + 1] = self._field[row_idx]
                self._field.make_row_empty(idx=0)

        count_lines()
        self.lines_scored.append(sequence_found) if sequence_found else None
        clear_lines()
        return sequence_found

    def place_figure(self, figure: IFigure,  coords: Iterable[int]):
        """Sets current_figure to the given figure as well as the current position to be given coords"""
        self._current_figure = figure
        self._figure_position = coords

    def change_figure_state(self, key: Key):
        """
        Changes current figures state according to the given key, revalidates position.
        After placing figure _field would raise an exception if interaction with its state or borders is occurred
        """
        self._current_figure.change_state_by_key(key)
        coords = copy.deepcopy(self._figure_position)   # revalidate coords after changing figure state
        assert isinstance(coords, Iterable)
        self._figure_position = coords

    def map_figure_to_field(self):
        """Mapping of the current figure at the current field state"""
        x, y = self.get_current_figure_pos()
        figure = self.get_current_figure()
        ret = copy.deepcopy(self._field)
        for row_idx in range(figure.height):
            for col_idx in range(figure.width):
                point = figure.get_current_state()[row_idx][col_idx]
                point_opauqe = bool(point)
                if point_opauqe:
                    ret[row_idx + y][col_idx + x] = point
        return ret

    def update_field_state(self):
        """Updates current field with current figure"""
        self._field.update_field_state(figure=self._current_figure, coords=self._figure_position)

    def get_current_field_state(self) -> IField:
        return self._field

    def get_current_figure(self) -> IFigure:
        return self._current_figure

    def get_current_figure_pos(self) -> Iterable[int]:
        return self._figure_position


class IEvent(ABC):
    """Abstract for various domain events"""
    @abstractmethod
    def __contains__(self, item):
        ...

    @abstractmethod
    def __getitem__(self, item):
        ...

    @abstractmethod
    def __len__(self):
        ...

    @abstractmethod
    def __setitem__(self, key, value):
        ...

    @abstractmethod
    def get_neutral_event(self):
        """Returns event when nothing to do is needed"""
        ...


class IActionEventMapper(ABC):
    """Interface for mapper, which maps events onto movement manager methods"""
    @abstractmethod
    def __init__(self, movement_manager, events_cls):
        ...

    @property
    @abstractmethod
    def _movement_manager(self):
        ...

    @abstractmethod
    def get_action_by_event(self, event: IEvent) -> Callable:
        ...


class IMovementManager(ABC):
    """Responsable for game objects movements and gameplay. Interacts with IIngameInteraction"""

    @property
    @abstractmethod
    def _physical_interactor(self) -> IPhysicalInteractor:
        """An instance of the interactor"""
        ...

    @property
    @abstractmethod
    def _available_figures(self) -> Iterable[IFigure]:
        ...

    @property
    @abstractmethod
    def _event_register(self) -> IEvent:
        ...

    @property
    @abstractmethod
    def game_is_alive(self) -> bool:
        ...

    @property
    @abstractmethod
    def lines_scored(self) -> List[int]:
        ...

    @abstractmethod
    def push_event(self, event: IEvent):
        ...

    @abstractmethod
    def start_game(self):
        ...

    @abstractmethod
    def tick_game(self):
        ...

    @abstractmethod
    def stop_game(self):
        ...

    @abstractmethod
    def pop_scored_lines(self):
        ...

    @abstractmethod
    def get_current_field_state(self):
        ...

    @abstractmethod
    def set_available_figures(self, figures: List[IFigure]):
        ...


class MovementManager(IMovementManager):
    def __init__(self, speed: int, events_cls: Type[IEvent], events_mapper_cls: Type[IActionEventMapper]):
        """Speed of falling figures in lines per second"""
        self.__physical_interactor: IPhysicalInteractor = PhysicalInteractor()
        self.falling_speed_in_lines_per_sec: int = speed    # lines/sec
        self._events_cls: Type[IEvent] = events_cls
        self._events_mapper: IActionEventMapper = events_mapper_cls(movement_manager=self,
                                                                    events_cls = self._events_cls)
        self._event_register: IEvent = self._events_cls.get_neutral_event()
        self._frames_per_falling_move_counter: int = 0   # for tick purposes. How many frames is needed to make one line
                                                         # step down
        self.game_is_alive = True

    def __str__(self):
        """FIXME: Consider further appearance"""
        return str(self._physical_interactor.map_figure_to_field())

    @property
    def _physical_interactor(self) -> IPhysicalInteractor:
        return self.__physical_interactor

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
    def _event_register(self) -> IEvent:
        return self.__event_register

    @_event_register.setter
    def _event_register(self, event: IEvent):
        # if event not in Event:
        #     raise ValueError(f'Wrong event is given: {event}')
        self.__event_register = event

    @property
    def falling_speed_in_lines_per_sec(self) -> int:
        """In lines per second"""
        return self.__falling_speed_in_lines_per_sec

    @falling_speed_in_lines_per_sec.setter
    def falling_speed_in_lines_per_sec(self, speed: int):
        if not isinstance(speed, int) or speed < 0:
            raise ValueError(f'Wrong falling speed is given: {speed}')
        self.__falling_speed_in_lines_per_sec = speed

    @property
    def game_is_alive(self) -> bool:
        return self.__game_is_alive

    @game_is_alive.setter
    def game_is_alive(self, val: bool):
        self.__game_is_alive = bool(val)

    @property
    def lines_scored(self) -> List[List[int]]:
        return self._physical_interactor.lines_scored

    def _count_and_clear_lines(self):
        """Counts score for filled lines and changes field state by removing counted lines out of field"""
        self._physical_interactor.count_and_clear_lines()

    def _random_figure(self) -> IFigure:
        rand_state: Key = Key(2)   # +1 because Enum.auto() FIXME
        rand_figure: IFigure = random.choice(self._available_figures)
        rand_figure.change_state_by_key(key=rand_state)
        return rand_figure

    def _random_current_position(self, figure: IFigure = None) -> Iterable[int]:
        """Chooses random coord at the top line of the field acceptable for chosen figure"""
        if figure is None:
            figure =  self._physical_interactor.get_current_figure()
        figure_width = figure.width
        field = self._physical_interactor.get_current_field_state()
        field_width = field.width
        try:
            random_x = random.choice(range(0, field_width - figure_width + 1))
            return random_x, 0
        except IndexError:
            return 0, 0

    def _move_down(self, *, lines: int = 1):
        current_figure: IFigure = self._physical_interactor.get_current_figure()
        current_pos: Iterable[int] = self._physical_interactor.get_current_figure_pos()
        offset = (0, lines)
        position_to_move: Iterable[int] = [sum(_) for _ in zip(current_pos, offset)]
        try:
            self._physical_interactor.place_figure(current_figure, position_to_move)

        except ObjectIntersectionException as OIE:
            raise FigureIsToBeAppended from OIE
        except OutOfBorderException as OoBE:    # this exception in move_down method means, bottom edge is approached
            raise FigureIsToBeAppended from OoBE

    def _move_right(self, *, lines: int = 1):
        current_figure: IFigure = self._physical_interactor.get_current_figure()
        current_pos: Iterable[int] = self._physical_interactor.get_current_figure_pos()
        offset = (lines, 0)
        position_to_move: Iterable[int] = [sum(_) for _ in zip(current_pos, offset)]
        try:
            self._physical_interactor.place_figure(current_figure, position_to_move)

        except ObjectIntersectionException as OIE:
            # this exception in move right method means, that there is no way to move righter so nothing to do
            pass
        except OutOfBorderException as OoBE:
            # this exception in move right method means, that right edge is approached so nothing to do
            pass

    def _move_left(self, *, lines: int = 1):
        current_figure: IFigure = self._physical_interactor.get_current_figure()
        current_pos: Iterable[int] = self._physical_interactor.get_current_figure_pos()
        offset = (-lines, 0)
        position_to_move: Iterable[int] = [sum(_) for _ in zip(current_pos, offset)]
        try:
            self._physical_interactor.place_figure(current_figure, position_to_move)

        except ObjectIntersectionException as OIE:
            # this exception in move left method means, that there is no way to move lefter so nothing to do
            pass
        except OutOfBorderException as OoBE:
            # this exception in move left method means, that left edge is approached so nothing to do
            pass

    def _accelerate(self):
        while True:
            self._move_down()

    def _rotate_figure(self):
        """Changes states of the current figure by cycle"""
        current_figure = self._physical_interactor.get_current_figure()
        current_figure_key = current_figure.get_current_key()
        next = current_figure_key.next()
        try:
            self._physical_interactor.change_figure_state(key=next)
        except OutOfBorderException as OoBE:  # if the figure appears to be interacting the field then do nothing
            self._physical_interactor.change_figure_state(key=current_figure_key)   # just revert to allowed state
        except ObjectIntersectionException as OIE:  # same here
            self._physical_interactor.change_figure_state(key=current_figure_key)

    def _spawn_figure(self):
        """Tries to put random figure to the first line at a random position.
        If excepts ObjectIntersectionException then raises GameOverException"""
        assert self._physical_interactor.get_current_field_state()
        assert self._available_figures
        rand_figure = self._random_figure()
        rand_pos = self._random_current_position(figure=rand_figure)
        try:
            self._physical_interactor.place_figure(rand_figure, rand_pos)
        except ObjectIntersectionException as OIE:
            self.game_is_alive = False

    def push_event(self, event: IEvent):
        self._event_register = event

    def start_game(self):
        self._spawn_figure()

    def tick_game(self):
        """Tries to move down the figure specified in _ingame_interactions.
        If FigureIsToBeAppended is caught then appends figure to the field state and clear filled lines """
        sleep(1 / cfg.PHYSICS_FRAME_RATE)   # this lines define physical frame period
        try:
            # make move down each cfg.FRAME_RATE // self._falling_speed_in_lines_per_sec frame and listen for events
            self._frames_per_falling_move_counter += 1
            e = self._event_register
            action = self._events_mapper.get_action_by_event(e)
            self._event_register = self._events_cls.get_neutral_event()
            action()
            if self._frames_per_falling_move_counter == cfg.PHYSICS_FRAME_RATE // self.falling_speed_in_lines_per_sec:
                                            # this line defines falling period
                self._frames_per_falling_move_counter = 0
                self._move_down()
        except FigureIsToBeAppended:
            self._physical_interactor.update_field_state()
            self._count_and_clear_lines()
            self._spawn_figure()

    def stop_game(self):
        pass

    def pop_scored_lines(self) -> List[List[int]]:
        """Flushes scored lines in interactor and returns """
        ret = copy.copy(self.lines_scored)
        self._physical_interactor.lines_scored = []
        return ret

    def get_current_field_state(self) -> IField:
        return self._physical_interactor.get_current_field_state()

    def set_available_figures(self, val: Optional[Iterable[IFigure]]):
        self._available_figures = val
