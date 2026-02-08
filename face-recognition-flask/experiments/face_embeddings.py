import cv2
import numpy as np

# -------- Load face detector --------
face_net = cv2.dnn.readNetFromCaffe(
    "models/deploy.prototxt",
    "models/res10_300x300_ssd_iter_140000.caffemodel"
)

# -------- Load face embedding model --------
embedder = cv2.dnn.readNetFromTorch(
    "models/openface.nn4.small2.v1.t7"
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Face detection
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

            # STEP 1: Crop face (ROI)
            face = frame[y1:y2, x1:x2]
            if face.size == 0:
                continue

            # STEP 2: Face embedding
            face_blob = cv2.dnn.blobFromImage(
                face, 1.0 / 255, (96, 96),
                (0, 0, 0), swapRB=True, crop=True
            )

            embedder.setInput(face_blob)
            embedding = embedder.forward()

            print("Embedding shape:", embedding.shape)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Face ROI + Embedding", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()