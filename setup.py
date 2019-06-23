from setuptools import setup

setup(
    name='ahp_midi_controller',
    version='0.0.1',
    description='Use USB Gamepad/Joysticks to control MIDI',
    py_modules=['ahp_midi_controller'],
    package_dir={'': 'src'},
    install_requires=['pygame', 'mido']
)
