import cv2
import sys


def cup_image(cropped_photo_path):
    """Шукаємо обличчя на фото, зробленому камерою"""
    try:
        cascade_path = 'filters/haarcascade_frontalface_default.xml'

        # Ініціалізація камери
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Не вдалося відкрити камеру.")
            return 'Помилка камери'

        print("Зачекайте, знімається фото...")

        while True:
            ret, frame = cap.read()
            print(ret)
            if not ret:
                print("Не вдалося отримати кадр з камери.")
                break

            # Показуємо кадр на екрані
            cv2.imshow('Capture Image', frame)

            # Шукаємо обличчя на кожному кадрі
            face_cascade = cv2.CascadeClassifier(cascade_path)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) != 0:
                for (x, y, w, h) in faces:
                    face = frame[y:y + h, x:x + w]
                    cv2.imwrite(cropped_photo_path, face)  # Зберігаємо фото
                    print(f"Обличчя знайдено та збережено в {cropped_photo_path}.")
                    cap.release()  # Закриваємо камеру
                    cv2.destroyAllWindows()  # Закриваємо всі вікна
                    sys.exit()  # Завершуємо програму
                break
            else:
                print("Обличчя не знайдено, пробуємо ще раз...")

        cap.release()  # Закриваємо камеру
        cv2.destroyAllWindows()  # Закриваємо всі вікна
        return 'Обличчя не знайдено'

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    cup_image('faces/cropped_face1.jpg')
