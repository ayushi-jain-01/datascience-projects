from flask import Flask, render_template, Response
import cv2
import numpy as np
import os

app = Flask(__name__)

# ---------------- Load models ----------------
face_net = cv2.dnn.readNetFromCaffe(
    "models/deploy.prototxt",
    "models/res10_300x300_ssd_iter_140000.caffemodel"
)

embedder = cv2.dnn.readNetFromTorch(
    "models/openface.nn4.small2.v1.t7"
)

# ---------------- Load known faces ----------------
KNOWN_FACES_DIR = "known_faces"
known_embeddings = []
known_names = []

for person_name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, person_name)

    if not os.path.isdir(person_dir):
        continue

    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)
        image = cv2.imread(image_path)

        if image is None:
            continue

        h, w = image.shape[:2]

        blob = cv2.dnn.blobFromImage(
            image, 1.0, (300, 300),
            (104.0, 177.0, 123.0)
        )

        face_net.setInput(blob)
        detections = face_net.forward()

        if detections.shape[2] > 0:
            box = detections[0, 0, 0, 3:7] * [w, h, w, h]
            x1, y1, x2, y2 = box.astype("int")

            face = image[y1:y2, x1:x2]
            if face.size == 0:
                continue

            face_blob = cv2.dnn.blobFromImage(
                face, 1.0 / 255, (96, 96),
                (0, 0, 0), swapRB=True, crop=True
            )

            embedder.setInput(face_blob)
            embedding = embedder.forward()

            known_embeddings.append(embedding.flatten())
            known_names.append(person_name)

print(f"[INFO] Loaded {len(known_names)} known faces")

# ---------------- Camera ----------------
camera = cv2.VideoCapture(0)

THRESHOLD = 0.7

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300),
            (104.0, 177.0, 123.0)
        )

        face_net.setInput(blob)
        detections = face_net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.6:
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                x1, y1, x2, y2 = box.astype("int")

                face = frame[y1:y2, x1:x2]
                if face.size == 0:
                    continue

                face_blob = cv2.dnn.blobFromImage(
                    face, 1.0 / 255, (96, 96),
                    (0, 0, 0), swapRB=True, crop=True
                )

                embedder.setInput(face_blob)
                embedding = embedder.forward().flatten()

                name = "Unknown"
                min_distance = float("inf")

                for known_emb, known_name in zip(known_embeddings, known_names):
                    distance = np.linalg.norm(known_emb - embedding)
                    if distance < min_distance:
                        min_distance = distance
                        name = known_name

                if min_distance > THRESHOLD:
                    name = "Unknown"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame, name,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2
                )

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(debug=True)