# tetris

Implementation of the core domain of the tetris game using DDD principles. Entity objects Field and Figure are aggregated by PhysicalInteractor and MovementManager.
The app layer is implemented by three loop threads - physics, keyboard listener and representator.

Game settings are at config.py.
Figure to play could be built in preset_figures.py. Use reset(), set_state() and get_result() methods of th FigureBuilder cls. Import of new-brand figures is automated.

