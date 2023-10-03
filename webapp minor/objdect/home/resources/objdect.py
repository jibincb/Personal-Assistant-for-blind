import numpy as np
import cv2
import concurrent.futures
import pyttsx3
import time

dur = 40
st = time.time()
# image_path = 'IMG_20201126_181055.jpg'
prototxt_path = 'home/resources/models/MobileNetSSD_deploy.prototxt.txt'
model_path = 'home/resources/models/MobileNetSSD_deploy.caffemodel'
# prototxt_path = 'models/MobileNetSSD_deploy.prototxt.txt'
# model_path = 'models/MobileNetSSD_deploy.caffemodel'
min_confidence = 0.2

classes = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor",
           ]

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

cap = cv2.VideoCapture(0)

def objcheck(frame, query):
    height, width = frame.shape[0], frame.shape[1]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007, (300, 300), 130)

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > min_confidence:
            class_id = int(detections[0, 0, i, 1])
            class_name = classes[class_id]
            if class_name == query:
                print(f"Detected object: {class_name}, Confidence: {confidence:.2f}")
                speak(f"{query} is found")
                return True
    print(f"{query} is not found")
    speak(f"{query} is not found")
    return False

def obj_dect(query):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        counter = 0
        while True:
            ret, frame = cap.read()

            if ret:
                if counter % 30 == 0:
                    executor.submit(objcheck, frame.copy(), query)
                # executor.submit(objcheck, frame.copy(), query)
                counter += 1

                process_frame(frame)

            key = cv2.waitKey(1)
            if time.time() - st >= dur:

                break
            if key == ord("q"):
                break
            # cap.release()
    # cv2.destroyAllWindows()
def process_frame(frame):
    cv2.imshow("video", frame)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Start object detection with 'bottle' as the query
# obj_dect('person')

# Release the VideoCapture object and close the
