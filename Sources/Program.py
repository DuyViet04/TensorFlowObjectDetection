from charset_normalizer import detect
from kivy.clock import Clock
import cv2
from Detector import DetectImage
from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import  Texture
from kivy.uix.floatlayout import FloatLayout

class StudentCardDetector(App):
    def build(self):
        self.HUDLayout = FloatLayout()
        self.DisplayImage = Image(allow_stretch=True, keep_ratio=True)
        self.HUDLayout.add_widget(self.DisplayImage)
        self.CameraCaptureSource = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1 / 5)
        return self.HUDLayout

    def update(self,dt):
        ret, frame = self.CameraCaptureSource.read()
        if ret:
            print('----------------------------')
            DetectedFrame = DetectImage(ImageToDetect= frame , threshold= 0.5)
            buf = cv2.flip(DetectedFrame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.DisplayImage.texture = image_texture
        else:
            print("cant find your camera")
            self.CameraCaptureSource.release()

    def on_stop(self):
        self.CameraCaptureSource.release()

StudentCardDetector().run()