import pigpio

pi = pigpio.pi()

while True:
    try:
        pin = int(input('Pin (0-31): '))
        pi.set_mode(pin, pigpio.OUTPUT)

        while (pwm := int(input('PWM (0, 500-2500), -1 - next: '))) != -1:
            if 500 <= pwm <= 2500 or pwm == 0:
                pi.set_servo_pulsewidth(pin, pwm)
            else:
                print(f'- PWM must be 0 or 500-2500, not {pwm}!')

        print('+ Next')

    except pigpio.error:
        print('- Wrong pin')

    except KeyboardInterrupt:
        print()
        break

# Turn off all motors
for pin in range(32):
    try:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.set_servo_pulsewidth(pin, 0)

    except pigpio.error:
        pass

pi.stop()
print('Exit...')
