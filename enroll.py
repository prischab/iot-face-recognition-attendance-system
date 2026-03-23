import cv2, os, sqlite3

# --- DB setup ---
conn = sqlite3.connect('students.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students (
              prn INTEGER PRIMARY KEY,
              name TEXT NOT NULL)''')
conn.commit()

# --- Input student info ---
name = input("Enter student name: ")
prn = int(input("Enter PRN (unique ID): "))

# --- Save to DB if new ---
c.execute("INSERT OR IGNORE INTO students VALUES (?, ?)", (prn, name))
conn.commit()

# --- Create dataset folder ---
folder = f"dataset/{name}_{prn}"
os.makedirs(folder, exist_ok=True)

# --- Camera setup ---
cam  = cv2.VideoCapture(0)
# change 0 to 1 if you have multiple cameras
if not cam.isOpened():
    print("? Camera not detected. Check connection.")
    exit()

count = 0
print("[INFO] Position your face in front of the camera. Press 'q' to stop early.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("? Frame not captured.")
        break

    # show preview window
    cv2.imshow("Enrollment Preview", frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    count += 1
    cv2.imwrite(f"{folder}/{count}.jpg", gray)

    if cv2.waitKey(1) == ord('q') or count >= 50:
        break

cam.release()
cv2.destroyAllWindows()
print(f"[INFO] Captured {count} images for {name} ({prn}).")

conn.close()

