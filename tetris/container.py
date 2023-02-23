# container to fabricate objects
from inspect import getmembers

import config as cfg
from physics import MovementManager, IFigure
import preset_figures
from services.keyboard_events import Event, ActionEventMapper, KeyEventMapper
from services.keyboard_handlers import KeyboardHandlers


def _partial_IFigure_isinstance(obj):
    """To be used while extracting figure objects from preset_figures with inspect.getmembers"""
    return isinstance(obj, IFigure)


events_cls = Event
events_mapper_cls = ActionEventMapper
movement_manager = MovementManager(events_cls=events_cls, events_mapper_cls=events_mapper_cls, speed=cfg.DEFAULT_SPEED)
inspected_preset_figures = getmembers(preset_figures, _partial_IFigure_isinstance)
figures = [_[1] for _ in inspected_preset_figures]
movement_manager.set_available_figures(figures)
keyboard_handlers = KeyboardHandlers(movement_manager=movement_manager)
