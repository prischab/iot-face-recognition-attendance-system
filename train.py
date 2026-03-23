import cv2, os, numpy as np
from PIL import Image

path = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades +
                                 "haarcascade_frontalface_default.xml")

faces, ids = [], []
for folder in os.listdir(path):
    if "_" not in folder:
        continue
    prn = int(folder.split("_")[-1])
    for image in os.listdir(os.path.join(path, folder)):
        img = Image.open(os.path.join(path, folder, image)).convert("L")
        img_np = np.array(img, "uint8")
        dets = detector.detectMultiScale(img_np)
        for (x, y, w, h) in dets:
            faces.append(img_np[y:y+h, x:x+w])
            ids.append(prn)

os.makedirs("trainer", exist_ok=True)
recognizer.train(faces, np.array(ids))
recognizer.save("trainer/trainer.yml")

# --- Save Label Mappings (PRN to Folder Name or Student Name) ---
with open("trainer/labels.txt", "w") as f:
    for folder in os.listdir(path):
        if "_" not in folder:
            continue
        prn = folder.split("_")[-1]
        name = folder.split("_")[0]
        f.write(f"{prn},{name}\n")

print("? Training complete and labels.txt generated successfully.")

