# CLS5830HV
# Dead band:            1μs (1 микросек. = 0.000001 сек.)
# Working frequence:    1520μs / 330hz
# Motor:                Coreless
# Operating Speed 6.0v  0.11 sec/60°
# Operating Speed 8.4v  0.09 sec/60°
# Stall Torque 6.0v     24.7 kg.cm
# Stall Torque 8.4v     30.3 kg.cm

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
