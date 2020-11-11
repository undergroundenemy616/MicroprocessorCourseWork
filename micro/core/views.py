from django.shortcuts import render
import json
from django.http import HttpResponse
from .telegram_api import invoke_telegram
from django.views.decorators.csrf import csrf_exempt
from micro import settings
import cv2
from .tasks import train, video_stream, button_check
from .models import User
from django.core.cache import cache
import os


# Create your views here.

video_stream.delay()
button_check.delay()

def __telegram_callback_query(json_message):
    # logger.info(f'Telegram has callback {json_message}')

    if 'message' not in json_message['callback_query']:
        return HttpResponse('OK')


@csrf_exempt
def telegram_hook(request):
    update = json.loads(request.body)
    # add.delay()

    if 'callback_query' in update:
        return __telegram_callback_query(update)

    if not 'message' in update:
        return HttpResponse('OK')

    message = update['message']

    text = ' '
    if 'text' in message:
        text = message['text'].strip()

    if settings.IS_REGISTRATION:
        if text == ' ':
            invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Нужно ввести Имя')
        else:
            user = User.objects.create(name=text)
            register_command(user.id)
            settings.IS_REGISTRATION = False

    if '/online' == text:
        invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text=f'Трансляция по ссылке: {settings.URL}/index.html')

    if cache.get('IS_FRIEND'):
        if 'Да' or 'да' == text:
            invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Дверь открылась')
            cache.set('IS_FRIEND', False, timeout=None)
        elif 'Нет' or 'не' == text:
            invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Он послан нахуй')
            cache.set('IS_FRIEND', False, timeout=None)
        else:
            invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Я вас не понял, введите Да/Нет')

    if '/start' == text:
        start_command()
        return HttpResponse('OK')

    if '/register' == text:
        settings.IS_REGISTRATION = True
        invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Введите Имя пользователя')

    return HttpResponse('OK')


def start_command():
    welcome_message = 'Сосать + лежать'
    invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text=welcome_message)

def register_command(text):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # For each person, enter one numeric face id
    face_id = text

    invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Идет процесс регистрации, смотрите в камеру')
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    while (True):
        ret, img = cam.read()
        img = cv2.flip(img, -1)  # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30:  # Take 30 face sample and stop video
            break
    invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Регистрация завершена, начинается тренировка нейронной сети, это займет некоторое время.')
    train.delay()
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()