import time
import cv2
import os
from deepface import DeepFace
from gpiozero import LED, Button
from time import sleep
from gpiostepper import Stepper
from service import cup_image

motor_pins = (18, 23, 24, 25)   # підключення пінів до мотора
step_motor = Stepper(motor_pins)
step_motor.set_speed(600)

led_green = LED(17)     # Підключення зеленого світлодіода
led_red = LED(27)       # Підключення червоного світлодіода

button = Button(22)


def save_face(frame, x, y, w, h):
    face = frame[y:y+h, x:x+w]      # виділяємо область під обличчя
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    face_filename = f'detected_faces/face_{timestamp}.jpg'
    cv2.imwrite(face_filename, face)
    return face


def compare_faces(face1_path: str, face2_path: str):
    # рівнюємо обличчя
    result = DeepFace.verify(img1_path=face1_path, img2_path=face2_path, enforce_detection=False)
    return result['verified']   # якшо true то обличчя співпадають якшо false то не співпадають


def load_stored_faces():
    stored_faces = []
    faces_dir = 'faces'
    for person_dir in os.listdir(faces_dir):
        person_path = os.path.join(faces_dir, person_dir)
        if os.path.isdir(person_path):
            for face_file in os.listdir(person_path):
                if face_file.startswith('cropped') and face_file.endswith('.jpg'):
                    stored_faces.append(os.path.join(person_path, face_file))
    return stored_faces


def verify_face(detected_face_path, stored_faces):
    for stored_face in stored_faces:
        result = compare_faces(detected_face_path, stored_face)
        if result is True:
            led_green.on()
            step_motor.step(32 * 64)
            sleep(1)
            led_green.off()
            return True
        else:
            led_red.on()
            sleep(1)
            led_red.off()
            return False


def face_check():
    cascade_path = 'filters/haarcascade_frontalface_default.xml'
    clf = cv2.CascadeClassifier(cascade_path)
    camera = cv2.VideoCapture(0)
    last_capture_time = time.time()     # час збереження останнього фото
    capture_interval = 5   # інтервал збереження
    stored_faces = load_stored_faces()

    while True:
        # зчитуємо дані з камери
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # знаходимло обличчя
        faces = clf.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
        )
        current_time = time.time()
        if current_time - last_capture_time >= capture_interval:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                face_path = save_face(frame=frame, x=x, y=y, w=w, h=h)
                if verify_face(face_path, stored_faces):
                    print('Доступ надано')
                    break
                else:
                    print('У доступі відмовлено')
            last_capture_time = current_time
        cv2.imshow('Faces', frame)
        if cv2.waitKey(1) == 'q':
            break
    camera.release()
    cv2.destroyAllWindows()

def button_face_processed():
    face_check()

# def button_face_save():
#     cup_image('faces')

if __name__ == '__main__':
    button.when_pressed = button_face_processed
    # button.when_pressed = button_face_save
