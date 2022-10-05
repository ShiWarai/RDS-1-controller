import pigpio

pi = pigpio.pi()

while True:
    try:
        pin = int(input("Pin (0-31): "))
        pi.set_mode(pin, pigpio.OUTPUT)

        while (pwm := int(input("PWM (0, 500-2500): "))) != 0:
            if 500 <= pwm <= 2500:
                pi.set_servo_pulsewidth(pin, pwm)
            else:
                print(f"- PWM must be 0 or 500-2500, not {pwm}!")

        pi.set_servo_pulsewidth(pin, pwm)
        print("+ Done")

    except pigpio.error:
        print("- Wrong pin")

    except KeyboardInterrupt:
        print()
        break

pi.stop()
print("Exit...")
