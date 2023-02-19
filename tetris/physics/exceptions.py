__all__ = ['PhysicException',
           'OutOfBorderException',
           'ObjectIntersectionException',
           'FigureIsToBeAppended',
           'GameOverException',
           ]


class PhysicException(Exception):
    """
    Common exception class for in-game physics
    """


class ObjectIntersectionException(PhysicException):
    """
    Raises when two object somehow have mutual intersection in a game field
    """


class OutOfBorderException(PhysicException):
    """Raises when figure gets out of field borders"""


class PhysicEvent(Exception):
    """Class for physical ingame events for IGameInteractor"""


class FigureIsToBeAppended(PhysicEvent):
    """Raises if a figure places on the top of field and intersection is to be occurred next tick"""


class GameOverException(PhysicEvent):
    """Raises then there is no way to place chosen figure at the chosen coordinates"""
