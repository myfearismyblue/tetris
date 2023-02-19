from physics import IMovementManager, IEvent
from services.keyboard_events import KeyEventMapper, Event


class KeyboardHandlers:
    """Handlers for pynput. Pointer to MovementManager should be provided in order to write in events"""

    def __init__(self, movement_manager: IMovementManager,
                 key_event_mapper: KeyEventMapper = KeyEventMapper(events_cls=Event)):
        self.movement_manager = movement_manager
        self.key_event_mapper = key_event_mapper

    def on_press(self, key):
        e: IEvent = self.key_event_mapper.get_event_by_key_or_neutral(key)
        self.movement_manager.push_event(e)

    def on_release(self, key):
        return
        raise NotImplementedError