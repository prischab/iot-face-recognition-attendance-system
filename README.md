# IoT-Enabled Face Recognition Attendance System Using Raspberry Pi and OpenCV

An IoT-enabled smart attendance system that automates student attendance using face recognition on a Raspberry Pi. The project uses Python, OpenCV, and the LBPH algorithm to identify students in real time, log attendance locally, and generate color-coded Excel reports for easy review.

## Overview

Traditional attendance systems such as manual roll calls, sign-in sheets, or RFID-based methods are time-consuming and prone to errors such as proxy attendance. This project addresses that problem by building a low-cost, privacy-aware, and fully offline attendance system using face recognition and edge computing.

The system captures student images during enrollment, trains a face recognition model, detects and recognizes students through a live camera feed, logs attendance into a local SQLite database, and exports attendance summaries to Excel.

## Key Features

- Automated face recognition-based attendance marking
- Raspberry Pi-based edge deployment
- Fully offline operation without cloud dependency
- Student enrollment with image dataset creation
- LBPH-based real-time face recognition
- Interval-based re-verification during class sessions
- Attendance logging using SQLite and CSV
- Color-coded Excel attendance reports
- One-hour automated attendance cycle for classroom use

## Problem Statement

Manual attendance systems are inefficient, slow, and vulnerable to inaccuracies. In classrooms and institutions moving toward smart infrastructure, there is a strong need for an automated, secure, and cost-effective attendance tracking solution.

This project was developed to provide a practical and privacy-focused alternative using computer vision and Raspberry Pi hardware.

## Objectives

- Automate classroom attendance using face recognition
- Reduce manual effort and attendance errors
- Build a lightweight system suitable for Raspberry Pi
- Store attendance records locally for privacy and control
- Generate easy-to-read attendance reports for teachers and administrators

## Tech Stack

- **Python**
- **OpenCV**
- **Raspberry Pi 4 Model B**
- **LBPH Face Recognizer**
- **SQLite**
- **Pandas**
- **OpenPyXL**
- **USB Camera / 8 MP Camera Module**

## How the System Works

The system runs in multiple stages:

### 1. Enrollment
Student details such as name, roll number, year, and PRN are entered through a Python-based CLI. The system then captures 50 grayscale face samples for each student and stores them locally.

### 2. Training
The captured images are used to train an LBPH face recognition model. The trained model is saved for future recognition, along with a label mapping file.

### 3. Real-Time Recognition
The camera captures live video frames. Faces are detected using Haar Cascade classifiers and recognized using the trained LBPH model. If the confidence threshold is acceptable, the student is marked present.

### 4. Attendance Logging
Attendance is recorded in a local SQLite database and CSV logs. The system tracks recognition events with timestamp, session interval, student identity, and confidence value.

### 5. Report Generation
At the end of the session, attendance data is exported to Excel. The output is color-coded:
- **Green** for Present
- **Red** for Absent

### 6. Automated Session Control
The system performs recognition every 20 minutes and automatically stops after one hour, simulating a real classroom session.

## Project Structure

iot-face-recognition-attendance-system/
│
├── enroll.py
├── train.py
├── recognize.py
├── run_all.py
├── export_excel.py
├── evaluate_metrics.py
├── labels.txt
├── students.db
├── README.md
│
├── dataset/
├── trainer/
├── logs/
├── output/
└── screenshots/

## Main Modules

- `enroll.py` – captures student data and face samples
- `train.py` – trains the LBPH recognition model
- `recognize.py` – performs live recognition and attendance marking
- `run_all.py` – controls the full automated workflow
- `export_excel.py` – generates Excel attendance summaries
- `evaluate_metrics.py` – evaluates recognition performance
- `labels.txt` – maps label IDs to student records

## Installation

### Prerequisites

- Python 3.x
- Raspberry Pi OS or compatible system
- OpenCV with contrib modules
- SQLite
- Pandas
- OpenPyXL

### Install dependencies

pip install opencv-contrib-python pandas openpyxl

## Usage

### Step 1: Enroll students

python enroll.py

### Step 2: Train the model

python train.py

### Step 3: Start real-time recognition

python recognize.py

### Step 4: Run the complete workflow

python run_all.py

### Step 5: Export attendance report

python export_excel.py

## Experimental Setup

The system was tested using:

- Raspberry Pi 4 Model B (4 GB RAM)
- 8 MP USB camera
- Raspberry Pi OS
- Python 3.10
- OpenCV Contrib
- SQLite
- Pandas and OpenPyXL

The dataset consisted of enrolled student face samples captured under slightly varying lighting conditions.

## Results

The LBPH recognition module achieved the following performance:

- **Recognition Accuracy:** 79.63%
- **False Acceptance Rate (FAR):** 0.31%
- **False Rejection Rate (FRR):** 21.23%
- **Average Detection Time per Frame:** 0.12 seconds

These results show that the system is effective for small-scale classroom deployment where low-cost and offline operation are important.

## Advantages

- Low-cost implementation using Raspberry Pi
- Offline and privacy-aware design
- Lightweight and suitable for edge devices
- Easy reporting through Excel output
- Modular structure for future scalability

## Limitations

- LBPH performance may decrease under strong backlighting or occlusion
- Recognition depends on consistent enrollment quality
- Current version does not include liveness detection
- Best suited for small to medium-sized deployments

## Future Enhancements

- Integrate deep learning-based models such as FaceNet or ArcFace
- Add anti-spoofing and liveness detection
- Support multi-camera synchronization for larger classrooms
- Build a web or mobile dashboard for attendance analytics
- Enable IoT/cloud synchronization using Firebase, MQTT, or AWS IoT
- Improve UI for admin and teacher interaction

## Privacy and Ethics

This project is designed with privacy in mind. Face images and attendance records are processed and stored locally on the device, reducing dependence on cloud services and minimizing data exposure.

For the public version of this repository, real student images, personal attendance records, and sensitive database files should not be uploaded.

## Research Paper

This project is based on the research work:

**IoT-Enabled Face Recognition Attendance System Using Raspberry Pi and OpenCV**

The research explores a privacy-aware and cost-effective attendance automation solution for smart classrooms using computer vision and edge deployment.

## Applications

- Smart classrooms
- Colleges and schools
- Training centers
- Small office attendance systems
- Privacy-sensitive on-device monitoring systems

## Author

**Prischa Bajeli**  
Department of Computer Engineering and Technology  
Dr. Vishwanath Karad MIT World Peace University  
Pune, Maharashtra, India
