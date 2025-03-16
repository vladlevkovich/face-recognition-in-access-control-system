from gpiozero import LED
from time import sleep

led = LED(17)   # визначте контакт світлодіода відповідно до нумерації BCM

def loop():
    while True:
        led.on()
        print('Led turned >>>>')
        sleep(1)
        led.off()
        print('Led turned of >>>>')
        sleep(1)

if __name__ == '__main__':
    print('Program is starting ... \n')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("Ending program")
