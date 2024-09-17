import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
LAMP_PIN = 7
IR_AREA_THRESHOLD = 70
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LAMP_PIN, GPIO.OUT, initial=GPIO.LOW)
def activate_lamp():
    GPIO.output(LAMP_PIN, GPIO.HIGH)
    print("Lamp activated")
def deactivate_lamp():
    GPIO.output(LAMP_PIN, GPIO.LOW)
    print("Lamp deactivated")
def detect_ir_light(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, ir_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(ir_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        contour_area = cv2.contourArea(max_contour)
        
        if contour_area > IR_AREA_THRESHOLD:
            M = cv2.moments(max_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            return True    
    return False
def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)    
    while True:
        ret, frame = cap.read()        
        if ret:
            ir_light_detected = detect_ir_light(frame)
            if ir_light_detected:
                activate_lamp()
            else:
                deactivate_lamp()
            
            cv2.imshow('Enchanted Lamp', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Unable to capture frame")
            break   
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exit")
    finally:
        GPIO.cleanup()
