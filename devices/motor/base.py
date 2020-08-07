import numpy as np
from simulation.loader import ScriptLoader

class MotorMixin:

    MAX_FORCE = 10000
    time_wait = -1

    applied_force = 0

    def _updateTime(self, tick):
        if self.time_wait > 0:
            self.time_wait -= 1 / ScriptLoader.instance.GAME_TICK_RATE
            if self.time_wait <= 0:
                self.off()
    
    def _applyMotors(self, object, position, rotation):
        object.apply_force(self.applied_force * np.array([np.cos(rotation), np.sin(rotation)]), pos=position)

    def on(self, speed, **kwargs):
        """
        Turn the motors on indefinitely at a certain speed.
        
        :param float speed: Any number from -100 to 100. Negative values turn the motors the opposite direction.
        """
        assert - 100 <= speed <= 100, "Speed value is out of bounds."
        self.applied_force = speed * self.MAX_FORCE / 100
        # Ensure this overwrites further 
        self.time_wait = -1

    def on_for_seconds(self, speed, seconds, **kwargs):
        """
        Turn the motors on for a certain amount of time. Note that further calls to motors may interrupt this behaviour.

        :param float speed: Any number from -100 to 100. Negative values turn the motors the opposite direction.
        :param float seconds: Any positive number. Seconds the motors will stay this speed for.
        """
        self.on(speed, **kwargs)
        self.time_wait = seconds
    
    def on_for_rotations(self, speed, rotations, **kwargs):
        """
        Turn the motors on for a certain amount of rotations. Note that further calls to motors may interrupt this behaviour.

        :param float speed: Any number from -100 to 100. Negative values turn the motors the opposite direction.
        :param float rotations: Any number, amount of rotations to complete, Negative values will turn the motors the opposite direction. 
        """
        if rotations < 0:
            speed *= -1
            rotations *= -1
        self.on_for_seconds(speed, rotations / self.ROTATIONS_PER_SECOND_AT_MAX * abs(speed) / 100, **kwargs)

    def on_for_degrees(self, speed, degrees, **kwargs):
        """
        Turn the motors on for a certain amount of degrees. Note that further calls to motors may interrupt this behaviour.

        :param float speed: Any number from -100 to 100. Negative values turn the motors the opposite direction.
        :param float degrees: Any number, amount of degrees to rotate, Negative values will turn the motors the opposite direction. 
        """
        self.on_for_rotations(speed, degrees / 360)

    def off(self):
        """
        Turns the motors off indefinitely, until further calls are made.
        """
        self.applied_force = 0
        self.time_wait = -1

    