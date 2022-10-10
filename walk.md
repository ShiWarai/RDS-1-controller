# Алгоритм ходьбы робота

За передвижение отвечает основная программа (main.py). В этой программе параллельно осуществляется считывание команд с контроллера и управление сервомоторами робота.

В начале мы импортируем библиотеки и настройки калибровки (`import calibrate_parameters`).

> main.py (строки 1-9)

``` python
from math import cos, sin, pi as PI
from threading import Thread
from time import time

from pigpio import pi

from controller import MyController

import calibrate_parameters
```

После этого определяем вспомогательные функции перевода значения из одного диапазона в другой (`def range`) и установки ШИМ сигнала для сервомотора (`def pwm`).

> main.py (строки 12-25)

``` python
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
```

Определяем настройки для алгоритма ходьбы.

> main.py (строки 28-42)

``` python
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
```

Инициируем библиотеки.

> main.py (строки 45-57)

``` python
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
```

Далее начинается основной цикл. Для безопасного завершения программы он обернут в блок try-except-finaly.

> main.py (строки 60-167, исключая 62-158)

``` python
try:
    while True:
		# --- ОСНОВНОЙ ЦИКЛ ---

except KeyboardInterrupt:
    print("\r - ctrl+c is stop - ")

finally:
    for pin, _, _ in SRV_ALL:
        pi.set_servo_pulsewidth(pin, 0)

    pi.stop()
```

В начале цикла мы считываем команды контроллера и обрабатываем их.

> main.py (строки 62-97, внутри основного цикла)

``` python
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
```

В основе алгоритма лежит идея о том, что передвижение это цикличный процесс. Мы можем использовать математическую функцию синуса от текущего времени в качестве основы этой цикличности. Это позволит нам не беспокоится о скорости выполнения программы. 

> main.py (строки 99-103)

``` python
# Walking / turning cycle
x = time() * speed
cycle_a = -cos(2 * x) if -sin(x) > 0 else -1
cycle_b = -cos(2 * x) if sin(x) > 0 else -1
cycle_x = cos(x)
```

Для начала мы рассчитываем поворот на месте (или шаг в сторону).

> main.py (строки 105-129)

``` python
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
```

Далее мы рассчитываем движение вперед (либо назад).

> main.py (строки 131-158)

``` python
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
```
