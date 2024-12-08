import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt
from datetime import datetime
from PIL import Image
import numpy as np

def crop_meter_reading(input_path, output_path):
    
    img = Image.open(input_path)
    
    img_array = np.array(img)
    
    height,width = img_array.shape[:2]
    top = int(height * 0.30) #0.35
    bottom = int(height * 0.64) #0.48
    left = int(width * 0.07) #0.45
    right = int(width * 0.95) #0.85

    
    cropped_img = img.crop((left,top,right,bottom))
    
    cropped_img.save(output_path)
    
    print(f"cropped image seved to {output_path}")


def preprocess_image(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrasted = clahe.apply(gray)
    
    
    binary = cv2.adaptiveThreshold(contrasted,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    
    
    titles = ['original', 'gray', 'binary']
    images = [image, gray, binary]
    for i in range(3):
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
    
    return gray



def draw_boxes(image, boxes):
    h,w, _ = image.shape
    for b in boxes.splitlines():
        b = b.split()
        if len(b) == 6:
            x,y,x2,y2 = int(b[1]), h- int(b[2]), int(b[3]), h- int(b[4])
            cv2.rectangle(image,(x,y),(x2,y2), (0,255,0),2)
            
    return image
               
 

def read_meter_value(image):
    
    preprocessed = preprocess_image(image)
    
    text1 = pytesseract.image_to_string(preprocessed, config='--psm 9 -c tessedit_char_whitelist=0123456789')
    text2 = pytesseract.image_to_string(preprocessed, config='--psm 13 -c tessedit_char_whitelist=0123456789')
    
    print(f"psm 9:{text1}\npsm 13:{text2}\n")
    
    text = text1 if sum(c.isdigit() for c in text1) > sum(c.isdigit() for c in text2) else text2
    
    boxes = pytesseract.image_to_boxes(preprocessed, config='--psm 13 -c tessedit_char_whitelist=0123456789')
    
    image_with_boxes = draw_boxes(image.copy(),boxes)
    
    plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
    plt.title('Recognized Numbers')
    plt.axis('off')
    plt.show()
    
     
    cleaned_text = "".join(c for c in text if c.isdigit() or c in ".,")
    
    return cleaned_text.strip()


def save_meter_reading(value, filename='meter_readings.txt'):
    current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    formatted_value = f"{value[:4]},{value[4:]}" if len(value) > 4 else value
    with open(filename, 'a') as f:
        f.write(f"[Read at: {current_time}] Meter Value: {formatted_value}\n")
        
        

def capture_image():
    
    camera = PiCamera()
    
    sleep(2)
    
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"vizora_teljes_{date_time}.jpg"
    
    camera.capture(filename)
    print(f"image capture: {filename}")
    
    camera.close()
        




today = datetime.today()
date_time = today.strftime("%Y%m%d%H%M")
print(today)

#capture_image()
input_image_path = "/home/pi/Desktop/projekt/Uj probalkozasok/vizora_teljes.jpg"
output_image_path = f"/home/pi/Desktop/projekt/Uj probalkozasok/cropped_jokep_{date_time}.jpeg"

crop_meter_reading(input_image_path,output_image_path)

image1 = cv2.imread(f'cropped_jokep_{date_time}.jpeg')

value1 = read_meter_value(image1)

save_meter_reading(value1)
print(f"meter 1 : {value1}")


