import cv2
import numpy as np
import sqlite3
import datetime
import time
import os

# ----------------------------
# Database Connection
# ----------------------------
conn = sqlite3.connect('students.db')
c = conn.cursor()

# ----------------------------
# Mark Attendance Function
# ----------------------------
def mark_attendance(prn, name):
    c.execute("SELECT * FROM attendance WHERE prn=?", (prn,))
    if c.fetchone():
        return  # already marked once in DB

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    c.execute("INSERT INTO attendance (prn, name, time) VALUES (?, ?, ?)", (prn, name, current_time))
    conn.commit()
    print(f"[INFO] Marked once for {name} ({prn}) at {current_time}")

# ----------------------------
# Load Trained Model and Labels
# ----------------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

labels = {}
with open("trainer/labels.txt", "r") as f:
    for line in f:
        prn, name = line.strip().split(",")
        labels[int(prn)] = name

# ----------------------------
# Initialize Camera
# ----------------------------
cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("[INFO] Starting new scan (1 minute)...")
start_time = time.time()

while True:
    ret, frame = cam.read()
    if not ret:
        print("[ERROR] Camera not detected.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_gray = gray[y:y + h, x:x + w]
        face_gray = cv2.resize(face_gray, (200, 200))
        face_gray = cv2.equalizeHist(face_gray)  # Normalize brightness

        id_, conf = recognizer.predict(face_gray)
        if conf < 65:  # stricter threshold to avoid false positives
            name = labels.get(id_, "Unknown")
            prn = id_
            mark_attendance(prn, name)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Recognition", frame)

    # Run for 60 seconds
    if time.time() - start_time > 60:
        print("[INFO] Scan complete. Camera closed safely.")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------------
# Cleanup
# ----------------------------
cam.release()
cv2.destroyAllWindows()
conn.close()

print("[SUMMARY] Scan finished ? attendance saved to database.")
print("[INFO] Waiting 30 minutes for next scan...")
time.sleep(30 * 60)  # 30 minutes

