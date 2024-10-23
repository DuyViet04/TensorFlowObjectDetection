from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import os
import cv2
from Detector import DetectImage

class ImageViewer(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        self.orientation = 'vertical'  # Đảm bảo layout theo chiều dọc

        # Tạo mảng chứa tất cả đường dẫn hình ảnh
        self.images = []
        self.current_index = 0

        # Tạo widget hiển thị ảnh
        self.image_widget = Image(size_hint=(1, 1))
        self.add_widget(self.image_widget)

        # Tạo label để hiển thị thông báo "Không có ảnh"
        self.label = Label(text="", font_size='15sp', size_hint=(1, 0.1), halign='center')
        self.add_widget(self.label)

        # Layout cho các nút điều khiển
        button_layout = BoxLayout(size_hint=(1, 0.1), padding=[100, 0, 100, 0], spacing=20)
        button_layout.pos_hint = {'center_x': 0.5}  # Căn giữa button_layout

        # Nút Quay lại
        self.prev_button = Button(text='Trước')
        self.prev_button.bind(on_press=self.show_previous_image)
        button_layout.add_widget(self.prev_button)

        # Nút Tiếp theo
        self.next_button = Button(text='Tiếp')
        self.next_button.bind(on_press=self.show_next_image)
        button_layout.add_widget(self.next_button)

        self.add_widget(button_layout)

        # Hiển thị ảnh đầu tiên hoặc thông báo nếu không có ảnh
        self.update_image()
    def ConstructFolderPath(self,folder_path):
        self.folder_path = folder_path
        # Tạo mảng chứa tất cả đường dẫn hình ảnh
        self.images = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if
                       f.endswith(('.png', '.jpg', '.jpeg'))]
        self.update_image()
    def update_image(self):
        # Kiểm tra nếu không có ảnh trong thư mục
        if not self.images:
            self.image_widget.texture = None  # Xóa ảnh hiện tại
            self.label.text = "Thư mục không có ảnh"  # Hiển thị thông báo
            return

        image_path = self.images[self.current_index]
        image = cv2.imread(image_path)

        if image is not None:
            DetectedImage = DetectImage(image, 0.5)
            image = cv2.cvtColor(DetectedImage, cv2.COLOR_BGR2RGB)  # Chuyển đổi từ BGR sang RGB
            image = cv2.resize(image, (1300, 1100))  # Thay đổi kích thước ảnh
            # Tạo một texture mới và gán vào image_widget
            texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
            texture.blit_buffer(image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            texture.flip_vertical()
            self.image_widget.texture = texture
            self.label.text = ""  # Xoá thông báo nếu có ảnh
        else:
            self.image_widget.texture = None  # Xoá ảnh nếu không thể tải
            self.label.text = "Không thể tải ảnh"  # Hiển thị thông báo nếu không thể tải ảnh
            print(f"Could not load image: {image_path}")

    def show_previous_image(self, instance):
        if self.images:  # Kiểm tra xem có ảnh hay không
            self.current_index = (self.current_index - 1) % len(self.images)
            self.update_image()

    def show_next_image(self, instance):
        if self.images:  # Kiểm tra xem có ảnh hay không
            self.current_index = (self.current_index + 1) % len(self.images)
            self.update_image()


class FolderChooser(FloatLayout):
    def __init__(self, bSelectFolder = True, **kwargs):
        super(FolderChooser, self).__init__(**kwargs)

        self.file_chooser = FileChooserIconView(dirselect=True, size_hint=(1, 0.75),
                                                on_touch_up=self.update_preview_folder,
                                                pos_hint = {'center_x': 0.5, 'center_y': 0.5})

        '''button to select folder actually'''
        self.select_btn = Button(on_release= self.select_folder,
                               text='Select Folder',size_hint=(1, 0.1),font_size='18sp',
                               pos_hint={'center_x': 0.5, 'center_y': 0})
        if(bSelectFolder):
            self.file_chooser.filters = ['*.']
        self.file_chooser.path = 'D:/'
        '''preview duong dan file'''
        self.preview_folder_label = Label(text='No folder selected',
                                          font_size='18',
                                          pos_hint={'center_x': 0.5, 'center_y': 0.1})

        self.add_widget(self.file_chooser)
        self.add_widget(self.select_btn)
        self.add_widget(self.preview_folder_label)

        self.selected_folder_path = None

    '''function execute selecting folder'''
    def select_folder(self, instance):
        # lấy folder
        selected_folder = self.file_chooser.selection
        if selected_folder:
            print(selected_folder[0])
            self.ImagesViewer.current_index = 0
            self.ImagesViewer.ConstructFolderPath(selected_folder[0])
            self.parent_popup.dismiss()
        else:
            self.preview_folder_label.text = 'No folder selected'

    def update_preview_folder(self, filechooser, selection):
        selected_folder = self.file_chooser.selection
        if selected_folder:
            self.preview_folder_label.text = f'Selected folder: {selected_folder[0]}'
        else:
            self.preview_folder_label.text = 'No folder selected'



'''Man hinh cho chuc nang xem anh'''
class ImageViewerScreen(Screen):
    def __init__(self, **kwargs):
        super(ImageViewerScreen, self).__init__(**kwargs)
        self.name = 'ImageViewerScreen'

        self.MainLayout = FloatLayout()

        self.OpenSelectFolder_Btn = Button(on_release= self.show_folder_chooser,
                                           text = "Select Open Dir",
                                           size_hint= (None,None),
                                           pos_hint = {'center_x': 0.9, 'center_y': 0.9})
        self.RealTimeMode_Btn = Button(on_release = self.OpenRealtimeMode,
                                       text = "< Back",
                                       size_hint = (0.1,0.08),
                                       pos_hint = {'center_x':0.05,'center_y' : 0.1})

        self.ImagesViewer = ImageViewer()
        self.MainLayout.add_widget(self.ImagesViewer)
        self.MainLayout.add_widget(self.OpenSelectFolder_Btn)
        self.MainLayout.add_widget(self.RealTimeMode_Btn)

        self.add_widget(self.MainLayout)


    def show_folder_chooser(self, instance):
        PopupObjectContent = FolderChooser()
        folder_chooser_popup = Popup(title='Chọn folder', content=PopupObjectContent, size_hint=(0.9, 0.9))
        PopupObjectContent.parent_popup = folder_chooser_popup
        PopupObjectContent.ImagesViewer = self.ImagesViewer
        folder_chooser_popup.open()
    def OpenRealtimeMode(self,instance):
        print("Realtime Detect Mode")
        self.manager.transition.direction='right'  # Thiết lập hiệu ứng chuyển tiếp
        self.manager.current = 'RealtimeDetectionScreen'  # Chuyển sang màn hình 2