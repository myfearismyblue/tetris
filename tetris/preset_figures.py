from physics import FigureBuilder, Key

__all__ = ['dash_figure',
           'L_figure',
           'square_figure',
           'Z_figure',
           'S_figure',
           'back_L_figure',
           'T_figure',
           ]

fb = FigureBuilder()

fb.reset(width=4, height=4)  # dash figure
fb.set_state(key=Key(1), state=[[1, 1, 1, 1],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0]])
fb.set_state(key=Key(2), state=[[1, 0, 0, 0],
                                [1, 0, 0, 0],
                                [1, 0, 0, 0],
                                [1, 0, 0, 0]])
fb.set_state(key=Key(3), state=[[1, 1, 1, 1],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0]])
fb.set_state(key=Key(4), state=[[1, 0, 0, 0],
                                [1, 0, 0, 0],
                                [1, 0, 0, 0],
                                [1, 0, 0, 0]])
dash_figure = fb.get_result()


fb.reset(width=3, height=3)  # L figure
fb.set_state(key=Key(1), state=[[1, 1, 1],
                                [1, 0, 0],
                                [0, 0, 0]])
fb.set_state(key=Key(2), state=[[1, 0, 0],
                                [1, 0, 0],
                                [1, 1, 0]])
fb.set_state(key=Key(3), state=[[0, 0, 1],
                                [1, 1, 1],
                                [0, 0, 0]])
fb.set_state(key=Key(4), state=[[1, 1, 0],
                                [0, 1, 0],
                                [0, 1, 0]])
L_figure = fb.get_result()


fb.reset(width=2, height=2)  # square figure
fb.set_state(key=Key(1), state=[[1, 1],
                                [1, 1]])
fb.set_state(key=Key(2), state=[[1, 1],
                                [1, 1]])
fb.set_state(key=Key(3), state=[[1, 1],
                                [1, 1]])
fb.set_state(key=Key(4), state=[[1, 1],
                                [1, 1]])
square_figure = fb.get_result()

fb.reset(width=3, height=3)  # Z figure
fb.set_state(key=Key(1), state=[[1, 1, 0],
                                [0, 1, 1],
                                [0, 0, 0]])
fb.set_state(key=Key(2), state=[[0, 1, 0],
                                [1, 1, 0],
                                [1, 0, 0]])
fb.set_state(key=Key(3), state=[[1, 1, 0],
                                [0, 1, 1],
                                [0, 0, 0]])
fb.set_state(key=Key(4), state=[[0, 1, 0],
                                [1, 1, 0],
                                [1, 0, 0]])
Z_figure = fb.get_result()

fb.reset(width=3, height=3)  # S figure
fb.set_state(key=Key(1), state=[[0, 1, 1],
                                [1, 1, 0],
                                [0, 0, 0]])
fb.set_state(key=Key(2), state=[[1, 0, 0],
                                [1, 1, 0],
                                [0, 1, 0]])
fb.set_state(key=Key(3), state=[[0, 1, 1],
                                [1, 1, 0],
                                [0, 0, 0]])
fb.set_state(key=Key(4), state=[[1, 0, 0],
                                [1, 1, 0],
                                [0, 1, 0]])
S_figure = fb.get_result()

fb.reset(width=3, height=3)  # back angle figure
fb.set_state(key=Key(1), state=[[1, 1, 1],
                                [0, 0, 1],
                                [0, 0, 0]])
fb.set_state(key=Key(2), state=[[1, 1, 0],
                                [1, 0, 0],
                                [1, 0, 0]])
fb.set_state(key=Key(3), state=[[1, 0, 0],
                                [1, 1, 1],
                                [0, 0, 0]])
fb.set_state(key=Key(4), state=[[0, 1, 0],
                                [0, 1, 0],
                                [1, 1, 0]])
back_L_figure = fb.get_result()

fb.reset(width=3, height=3)  # T figure
fb.set_state(key=Key(1), state=[[1, 1, 1],
                                [0, 1, 0],
                                [0, 0, 0]])
fb.set_state(key=Key(2), state=[[1, 0, 0],
                                [1, 1, 0],
                                [1, 0, 0]])
fb.set_state(key=Key(3), state=[[0, 1, 0],
                                [1, 1, 1],
                                [0, 0, 0]])
fb.set_state(key=Key(4), state=[[0, 1, 0],
                                [1, 1, 0],
                                [0, 1, 0]])
T_figure = fb.get_result()


