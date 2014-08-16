import cv2
import requests

vc = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
service_backend = 'http://10.10.89.99:5000/face'


def detect(img):
    rects = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def post_to_service(image):
    files = {'file': image}
    requests.post(service_backend, files=files)


if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    rval, frame = vc.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = detect(gray)
    for face in faces:
        cv2.imwrite('face.jpg', gray)
        post_to_service(open('face.png', 'rb'))


cv2.destroyWindow("preview")
