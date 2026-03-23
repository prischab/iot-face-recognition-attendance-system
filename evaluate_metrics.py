import cv2
import time
import numpy as np

# Load LBPH model and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def evaluate_run(run_id=1):
    cam = cv2.VideoCapture(0)
    total_frames, tp, fp, fn = 0, 0, 0, 0
    frame_times = []

    print(f"\n[INFO] Starting evaluation run {run_id} ... Press 'q' to stop.")
    start_time = time.time()

    while True:
        frame_start = time.time()
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        total_frames += 1

        if len(faces) == 0:
            fn += 1  # no detection this frame
        for (x, y, w, h) in faces:
            id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 85:
                tp += 1  # correctly recognized
            else:
                fp += 1  # unrecognized/unknown face

        frame_times.append(time.time() - frame_start)
        cv2.imshow("Evaluation", frame)
        if cv2.waitKey(1) & 0xFF == ord("q") or time.time() - start_time > 20:
            break

    cam.release()
    cv2.destroyAllWindows()

    # Calculate metrics
    accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
    far = fp / (tp + fp) if (tp + fp) > 0 else 0
    frr = fn / (tp + fn) if (tp + fn) > 0 else 0
    avg_latency = np.mean(frame_times)

    return accuracy, far, frr, avg_latency

# Run three times with different seeds
results = []
for seed in [0, 42, 99]:
    np.random.seed(seed)
    accuracy, far, frr, latency = evaluate_run(seed)
    results.append((accuracy, far, frr, latency))

# Show summary
print("\n===== SUMMARY =====")
for i, (acc, far, frr, lat) in enumerate(results, 1):
    print(f"Run {i}: Accuracy={acc*100:.2f}%, FAR={far*100:.2f}%, FRR={frr*100:.2f}%, Latency={lat:.3f}s")

means = np.mean(results, axis=0)
stds = np.std(results, axis=0)
print(f"\nMean: Accuracy={means[0]*100:.2f}%, FAR={means[1]*100:.2f}%, FRR={means[2]*100:.2f}%, Latency={means[3]:.3f}s")
print(f"Std Dev: Accuracy={stds[0]*100:.2f}%, FAR={stds[1]*100:.2f}%, FRR={stds[2]*100:.2f}%, Latency={stds[3]:.3f}s")
