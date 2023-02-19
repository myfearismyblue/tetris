# container to fabricate objects

import config as cfg
from physics import MovementManager
from services.keyboard_events import Event, ActionEventMapper, KeyEventMapper
from services.keyboard_handlers import KeyboardHandlers

events_cls = Event
events_mapper_cls = ActionEventMapper

movement_manager = MovementManager(events_cls=events_cls, events_mapper_cls=events_mapper_cls, speed=cfg.DEFAULT_SPEED)
keyboard_handlers = KeyboardHandlers(movement_manager=movement_manager)
