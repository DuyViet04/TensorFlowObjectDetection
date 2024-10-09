import tensorflow as tf
import numpy as np
import cv2

model = tf.saved_model.load('../ModelObjectDetections/SSDMobileNetv2/saved_model')

'''def LoadLabel(cocoPath):
    with open('../ModelObjectDetections/coco.names', 'r') as f:
        labelArr = [line.strip() for line in f.readlines()]
    labelArr.insert(0,'__background__')
    return labelArr

labels = LoadLabel('../ModelObjectDetections/coco.names')'''

labels = ['__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
          'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter',
          'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
          'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
          'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
          'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
          'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
          'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
          'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
          'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = camera.read()
    if ret:
        imageNp = np.array(frame)
        inputTensor = tf.convert_to_tensor(np.expand_dims(imageNp, 0), dtype=tf.uint8)
        detection = model(inputTensor)
        boxes = detection['detection_boxes'].numpy()
        classes = detection['detection_classes'].numpy().astype(int)
        scores = detection['detection_scores'].numpy()

        for i in range(classes.shape[1]):
            classId = int(classes[0, i])
            score = scores[0, i]

            if np.any(score > 0.5):
                h, w, _ = imageNp.shape
                ymin, xmin, ymax, xmax = boxes[0, i]

                xmin = int(xmin * w)
                xmax = int(xmax * w)
                ymin = int(ymin * h)
                ymax = int(ymax * h)

                className = labels[classId]
                cv2.rectangle(imageNp, (xmin, ymin), (xmax, ymax), (255, 255, 255), 2)
                label = f"Class: {className}, Score: {score:.2f}"
                cv2.putText(imageNp, label, (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Camera', imageNp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
