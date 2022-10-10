from math import cos, sin, pi as PI
from threading import Thread
from time import time

from pigpio import pi

from controller import MyController

from calibrate_parameters import *


def range(old_max, old_min, new_max, new_min, value):
    old_range = old_max - old_min
    new_range = new_max - new_min

    return (((value - old_min) * new_range) / old_range) + new_min


def pwm(pi, pin, pwm):
    if pwm < 500:
        pwm = 500
    elif pwm > 2500:
        pwm = 2500

    pi.set_servo_pulsewidth(pin, pwm)


# SETUP
SPEED_MIN = 8
SPEED_TOP = 10
STEP_X = 200
STEP_Y = 150

# Do not change (predeclaration for later)
walk = False  # True - walk, False - stay still
turn = True  # True - control turn, False - control sideways walk
step_height = 1.0  # min 0.0 -> max 1.0
idle = 0  # time in sec since lats stick (walk) input
speed = SPEED_MIN  # current speed mode
quad = 0    # | Keep walk directions to prevent mid step changes
pair_a = 0  # |
pair_b = 0  # |


# PIGPIO INIT
pi = pi()

for pin, _, max in SRV_ALL:
    pi.set_mode(pin, 1)
    pi.set_servo_pulsewidth(pin, max)


# Init the controller
# 1C:96:5A:D1:76:5D
controller = MyController()
thread = Thread(target=controller.listen, daemon=True)
thread.start()


try:
    while True:
        inputs = controller.get_inputs()

        # Press L1 -> Left stick controls turn around or sidewalk
        if inputs["l1"]:
            turn = not turn

        # Hold R1 -> Boost speed
        if inputs["r1_hold"]:
            speed = SPEED_TOP
        else:
            speed = SPEED_MIN

        # Press up or down arrows -> Raise or lower the body
        if inputs["up"]:
            h = step_height + 0.05
            step_height = h if h < 1 else 1

        if inputs["down"]:
            h = step_height - 0.05
            step_height = h if h > 0 else 0

        # Stop after 3 sec of idle (no directional input)
        if inputs["move_x"] or inputs["move_y"]:
            idle = time()

        # Press X -> Stop or continue to walk
        if inputs["x"] or (walk and time() - idle > 3):
            walk = not walk
            idle = time()

        if not walk:
            for pin, min, max in SRV_ALL:
                height = range(1, 0, max, min, step_height)
                pwm(pi, pin, height)

            continue

        # Walking / turning cycle
        x = time() * speed
        cycle_a = -cos(2 * x) if -sin(x) > 0 else -1
        cycle_b = -cos(2 * x) if sin(x) > 0 else -1
        cycle_x = cos(x)

        # Turn around / walk sideways
        move_y = range(32676, -32676, STEP_Y, -STEP_Y, inputs["move_y"])
        quad = move_y if -0.1 < cycle_x < 0.1 else quad * walk

        for pin, min, max in SRV_UP_FR:
            stride = range(1, -1, max - quad, max + quad, cycle_x)
            pwm_new = range(1, -1, min, stride, cycle_a)
            pwm(pi, pin, pwm_new)

        for pin, min, max in SRV_UP_FL:
            stride = range(1, -1, max + quad, max - quad, cycle_x)
            pwm_new = range(1, -1, min, stride, cycle_a)
            pwm(pi, pin, pwm_new)

        for pin, min, max in SRV_UP_BR:
            cx = -cycle_x if turn else cycle_x
            stride = range(1, -1, max - quad, max + quad, cx)
            pwm_new = range(1, -1, min, stride, cycle_a)
            pwm(pi, pin, pwm_new)

        for pin, min, max in SRV_UP_BL:
            cx = -cycle_x if turn else cycle_x
            stride = range(1, -1, max + quad, max - quad, cx)
            pwm_new = range(1, -1, min, stride, cycle_a)
            pwm(pi, pin, pwm_new)

        # Walk straight
        move_x = range(32676, -32676, STEP_X, -STEP_X, inputs["move_x"])
        pair_a = move_x if cycle_a > 0.9 else pair_a
        pair_b = move_x if cycle_b > 0.9 else pair_b

        for pin, min, max in SRV_FR:
            height = range(1, 0, max, min, step_height)
            stride = range(1, -1, height - pair_a, height + pair_a, cycle_x)
            pwm_new = range(1, -1, min, stride, cycle_b)
            pwm(pi, pin, pwm_new)

        for pin, min, max in SRV_FL:
            height = range(1, 0, max, min, step_height)
            stride = range(1, -1, height - pair_a, height + pair_a, cycle_x)
            pwm_new = range(1, -1, min, stride, cycle_a)
            pwm(pi, pin, pwm_new)

        for pin, min, max in SRV_BL:
            height = range(1, 0, max, min, step_height)
            stride = range(1, -1, height - pair_b, height + pair_b, -cycle_x)
            pwm_new = range(1, -1, min, stride, cycle_a)
            pwm(pi, pin, pwm_new)

        for pin, min, max in SRV_BR:
            height = range(1, 0, max, min, step_height)
            stride = range(1, -1, height - pair_b, height + pair_b, -cycle_x)
            pwm_new = range(1, -1, min, stride, cycle_b)
            pwm(pi, pin, pwm_new)

except KeyboardInterrupt:
    print("\r - ctrl+c is stop - ")

finally:
    for pin, _, _ in SRV_ALL:
        pi.set_servo_pulsewidth(pin, 0)

    pi.stop()
