import cv2
from deepface import DeepFace
import os
from deepface.basemodels import VGGFace
import concurrent.futures
import time
from collections import Counter


def most_frequent(arr):
    counter = Counter(arr)
    most_common = counter.most_common(1)
    return most_common[0][0]


avg_face = []
# url = "http://192.168.180.118:8080/video"
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def FindFace(frame):
    model = VGGFace.loadModel()

    try:
        df = DeepFace.find(frame, db_path='faces', model_name='VGGFace', model=model, distance_metric='cosine')
        print(df)

        if not df.empty:
            image_name = os.path.splitext(os.path.basename(dt[0]))[0]
            return image_name
        else:
            print("No face found in the database")
            return "Error"
    except ValueError:
        print("Face not found in the database")
        return "Error"


def process_frame(frame):
    face = FindFace(frame)
    cv2.putText(frame, face, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    avg_face.append(face)

    cv2.imshow("video", frame)


dur = 10
st = time.time()


def face_regn():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        counter = 0
        while True:
            ret, frame = cap.read()

            if ret:
                if counter % 30 == 0:
                    executor.submit(FindFace, frame.copy())

                counter += 1

                process_frame(frame)

            key = cv2.waitKey(1)
            if time.time() - st >= dur:
                break
            if key == ord("q"):
                break

    result = most_frequent(avg_face)
    cv2.destroyAllWindows()
    if result == "Error":
        print("Sorry, face not found in the database")
        return None

    else:
        print(result)
        return result


# f = face_regn()
# print(f)
cv2.destroyAllWindows()
