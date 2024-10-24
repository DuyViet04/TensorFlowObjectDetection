from kivy.uix.screenmanager import ScreenManager
from WebcamRealtimeDectector import RealTimeDectector
from ImageViewer import ImageViewerScreen
from kivy.app import App

class MyApp(App):
    def build(self):
        self.title = 'StudentDetectionApp'
        sm = ScreenManager()
        self.CameraPage = RealTimeDectector()
        self.ImageViewerPage = ImageViewerScreen()
        sm.add_widget(self.CameraPage)
        sm.add_widget(self.ImageViewerPage)
        return sm

MyApp().run()
