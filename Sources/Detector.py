import numpy as np
import cv2
from tensorflow.lite.python.interpreter import Interpreter

#input = (inputvalue - input mean)/input_std
input_mean = 127.5
input_std = 127.5 #input standard deviation
def DetectImage(ImageToDetect, threshold):
    lblpath = '../ModelObjectDetections/SSDMobileNetv2/saved_model/labelmap.txt'
    with open(lblpath, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    '''Load the TFLite model'''
    interpreter = Interpreter(model_path='../ModelObjectDetections/SSDMobileNetv2/saved_model/detect.tflite')
    interpreter.allocate_tensors()

    """Cho quá trình lập trình gọn hơn"""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    imH, imW, _ = ImageToDetect.shape

    '''Tiền xử lý để đưa ảnh vào model'''
    image_rgb = cv2.cvtColor(ImageToDetect, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image_rgb, (width, height))
    input_ImageData = np.expand_dims(resized_image, axis=0)

    # chuẩn hóa giá trị trong mảng ảnh để đúng với khoảng giá trị mà huấn luyện mô hình
    bFloatInput = (input_details[0]['dtype'] == np.float32)
    if bFloatInput:
              input_ImageData = (np.float32(input_ImageData) - input_mean) / input_std

    '''nhan dien anh'''
    # Set the tensor to the input data
    interpreter.set_tensor(input_details[0]['index'], input_ImageData)
    # Run inference
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[0]['index'])[0]  # Confidence of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0]

    # Visualize results on the image
    for i in range(len(scores)):
        if scores[i] > threshold:
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            cv2.rectangle(ImageToDetect, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            ObjectName = labels[int(classes[i])]
            print(f'{classes[i]}:{ObjectName}')
            label = '%s: %d%%' % (ObjectName, int(scores[i] * 100))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(ymin, labelSize[1] + 10)
            cv2.putText(ImageToDetect, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (256, 256, 256),2)  # Draw label text

    return ImageToDetect

