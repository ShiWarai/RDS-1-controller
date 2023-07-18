import pigpio
import curses

#                1     2           1     2
SRV_UP = ((2,  1450, 1450), (14, 1650, 1650),
          (18, 1500, 1500), (23, 1500, 1500))

# Stand low
# SRV_FR = ((3,  1680, 1470), (4,  1390, 1570))
# SRV_FL = ((15, 1750, 2000), (17, 1570, 1390))
# SRV_BR = ((22, 1250, 1520), (27, 1730, 1560))
# SRV_BL = ((25, 1820, 1580), (24, 950,  1110))

SRV_FR = ((3,  1680, 1340), (4,  1390, 1630))
SRV_FL = ((15, 1750, 2050), (17, 1570, 1300))
SRV_BR = ((22, 1250, 1570), (27, 1730, 1400))
SRV_BL = ((25, 1820, 1450), (24, 950,  1200))

SRV_ALL = SRV_UP + SRV_FR + SRV_FL + SRV_BR + SRV_BL

is_up = True  # 2 if is_up else 1

pi = pigpio.pi()
pwm = pi.set_servo_pulsewidth

for pin, _, _ in SRV_ALL:
    pi.set_mode(pin, pigpio.OUTPUT)
    pwm(pin, 0)

for pin, mx, mn in SRV_ALL:
    x = mn if is_up else mx
    pwm(pin, x)

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

try:
    pose = 2 if is_up else 1
    n = 0  # 0-7
    servos = [
        [3, SRV_FR[0][pose]],
        [4, SRV_FR[1][pose]],
        [15, SRV_FL[0][pose]],
        [17, SRV_FL[1][pose]],
        [22, SRV_BR[1][pose]],
        [27, SRV_BR[0][pose]],
        [25, SRV_BL[1][pose]],
        [24, SRV_BL[0][pose]],
    ]

    while True:
        char = stdscr.getch()

        if char == curses.KEY_UP:
            pulse = servos[n][1]
            pulse = pulse + 10 if pulse + 10 < 2500 else pulse
            servos[n][1] = pulse

        elif char == curses.KEY_DOWN:
            pulse = servos[n][1]
            pulse = pulse - 10 if pulse - 10 > 500 else pulse
            servos[n][1] = pulse

        elif char == curses.KEY_LEFT:
            n = 7 if n == 0 else n - 1

        elif char == curses.KEY_RIGHT:
            n = 0 if n == 7 else n + 1

        else:
            continue

        pin = servos[n][0]
        pulse = servos[n][1]

        print(f'\rpin = {pin} pwm = {pulse}   ', end='')
        pwm(pin, pulse)

except KeyboardInterrupt:
    print()

finally:
    for pin, _, _ in SRV_ALL:
        pwm(pin, 0)
    pi.stop()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    print(servos)
