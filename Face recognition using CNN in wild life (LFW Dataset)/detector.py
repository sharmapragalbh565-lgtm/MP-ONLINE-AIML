import pandas as pd
from ultralytics import YOLO
import cv2
import os
import sys

CARNIVORES = [
    "lion", "tiger", "bear", "wolf", "leopard",
    "dog", "cat", "fox"
]
model = YOLO("yolov8n.pt")

print("Welcome to the Animal Detection System!")
print("1: Test a single image")
print("2: Process your dataset folder (using animal_detection_model.csv)")
print("3: Test a video")
choice = input("Enter your choice (1, 2, or 3): ")

if choice == '1':
    img_path = input("Enter the full path to your image file: ")
    if not os.path.exists(img_path):
        print("Image not found. Exiting.")
        sys.exit()
        
    img = cv2.imread(img_path)
    results = model(img)
    carnivore_count = 0
    
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls)
            label = r.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            if label in CARNIVORES:
                color = (0, 0, 255)  # RED in BGR
                carnivore_count += 1
            else:
                color = (0, 255, 0)  # GREEN in BGR
                
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
    print(f"Carnivorous Animals Detected: {carnivore_count}")
    cv2.putText(img, f"Carnivores: {carnivore_count}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    
    cv2.imshow("Single Image Detection", img)
    print("Press any key to close the image window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

elif choice == '2':
    folder_path = input("Enter the folder path containing your dataset images: ")
    csv_path = "animal_detection_model.csv"
    
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found in this directory!")
        sys.exit()
        
    df = pd.read_csv(csv_path)
    print("\nStarting dataset processing...")
    print("Press any key in the image window to proceed to the next image, or press 'q' to quit.\n")
    
    for index, row in df.iterrows():
        img_id = row['image_id']
        
        # Check for common extensions
        img_path = os.path.join(folder_path, f"{img_id}.jpg")
        if not os.path.exists(img_path):
            img_path = os.path.join(folder_path, f"{img_id}.png")
            
        if not os.path.exists(img_path):
            print(f"Skipping {img_id}: Image not found in folder.")
            continue
            
        img = cv2.imread(img_path)
        results = model(img)
        carnivore_count = 0
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                label = r.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                if label in CARNIVORES:
                    color = (0, 0, 255)
                    carnivore_count += 1
                else:
                    color = (0, 255, 0)
                    
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
        cv2.putText(img, f"Carnivores: {carnivore_count}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("Dataset Viewer", img)
        
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            print("Quitting dataset viewer.")
            break
            
    cv2.destroyAllWindows()

elif choice == '3':
    video_path = input("Enter the path to your video file: ")
    if not os.path.exists(video_path):
        print("Video not found. Exiting.")
        sys.exit()
        
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        results = model(frame)
        carnivore_count = 0
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                label = r.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                if label in CARNIVORES:
                    color = (0, 0, 255)
                    carnivore_count += 1
                else:
                    color = (0, 255, 0)
                    
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
        cv2.putText(frame, f"Carnivores: {carnivore_count}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("Video Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
else:
    print("Invalid choice. Exiting.")
