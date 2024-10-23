
from kivy.clock import Clock
import cv2
from Detector import DetectImage
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics.texture import  Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class RealTimeDectector(Screen):
    def __init__(self, **kwargs):
        super(RealTimeDectector, self).__init__(**kwargs)
        self.name = 'RealtimeDetectionScreen'
        self.HUDLayout = FloatLayout()
        self.DisplayImage = Image(allow_stretch=True, keep_ratio=True)
        self.OpenImageViewer_Btn = Button(size_hint=(0.12, 0.08),
                                          text = "ImageViewer",
                                          on_press=self.OnPressAlbumBtn,
                                          pos_hint={'center_x': 0.9, 'center_y': 0.1})
        self.HUDLayout.add_widget(self.DisplayImage)
        self.HUDLayout.add_widget(self.OpenImageViewer_Btn)

        self.CameraCaptureSource = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1 / 15)
        self.add_widget(self.HUDLayout)
    def update(self,dt):
        ret, frame = self.CameraCaptureSource.read()
        if ret:
            print('----------------------------')
            DetectedFrame = DetectImage(ImageToDetect= frame , threshold= 0.5)
            buf = cv2.flip(DetectedFrame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.DisplayImage.texture = image_texture


    def OnPressAlbumBtn(self,instance):
        print("OpenPictureInFolder")
        self.manager.transition.direction='left'  # Thiết lập hiệu ứng chuyển tiếp
        self.manager.current = 'ImageViewerScreen'  # Chuyển sang màn hình 2
        self.CameraCaptureSource.release()

    def on_enter(self):
        if self.CameraCaptureSource is not None:
            self.CameraCaptureSource = cv2.VideoCapture(0)
            print("enter CameraCaptureSource")
    def on_stop(self):
        self.CameraCaptureSource.release()