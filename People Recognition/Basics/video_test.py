import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("op", help="operation you want to perform over the image", type=str, 
                    choices = ['identity', 'emboss', 'canny', 'blur', 'sharpen', 'sobel', 'gray'])
parser.add_argument("--video", help="use a video file", type=str)
args = parser.parse_args()

if args.video:
    cap = cv2.VideoCapture(args.video)
else:
    cap = cv2.VideoCapture(0)

kernels = {
    'emboss': np.array([[-2, -1,  0],
                        [-1,  1,  1],
                        [ 0,  1,  2]]),
    'identity': np.array([[0, 0, 0],
                          [0, 1, 0],
                          [0, 0, 0]]),
    'sharpen' : np.array([[ 0, -1,  0],
                          [-1,  5, -1],
                          [ 0, -1,  0]]),
    'blur' : np.ones((3, 3)) * 1/9,
}

while cap.isOpened():
    success, frame = cap.read()
    
    if not success:
        if args.video: break
        else: continue
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    if args.op == 'gray':
        frame = gray
    elif args.op == 'sobel':
        frame = cv2.Sobel(src=frame, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    elif args.op == 'canny':
        frame = cv2.Canny(frame, threshold1=100, threshold2=200)
    else:
        frame = cv2.filter2D(frame, -1, kernels[args.op])
    
    cv2.imshow('Basics AI - @Home', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()