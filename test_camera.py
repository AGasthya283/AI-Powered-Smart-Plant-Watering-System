import cv2
from datetime import datetime

print("Testing all cameras:")
for i in [0, 1, 2, 3]:
    print(f"\nTesting camera {i}:")
    cap = cv2.VideoCapture(i)
    
    if cap.isOpened():
        print(f"Camera {i} opens successfully")
        ret, frame = cap.read()
        if ret and frame is not None:
            h, w = frame.shape[:2]
            # Save the frame to a file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            frame_filename = f"camera_testing/frame_{timestamp}.jpg"
            cv2.imwrite(frame_filename, frame)
            print(f"Can read frames: {w}x{h}")
        else:
            print(f"Opens but cannot read frames")
        cap.release()
    else:
        print(f"Cannot open camera {i}")