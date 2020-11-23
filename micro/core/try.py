import cv2
import os

def register_command(text):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    print('1')
    face_detector = cv2.CascadeClassifier('/home/pi/python/recognition/haarcascade_frontalface_default2.xml')
    print(face_detector)
    
    # For each person, enter one numeric face id
    face_id = input()
    #invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Идет процесс регистрации, смотрите в камеру')
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    while (True):
        ret, img = cam.read()
        #img = cv2.flip(img, -1)  # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print('fuck')
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        print(type(faces))
        print('-------')
        print('-------')
      
        
        
        for (x, y, w, h) in faces:
            print('wtf')
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
    #invoke_telegram('sendMessage', chat_id=settings.CHAT_ID, text='Регистрация завершена, начинается тренировка нейронной сети, это займет некоторое время.')
    #train.delay()
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    
register_command('ds')