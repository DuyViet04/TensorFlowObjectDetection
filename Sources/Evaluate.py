from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import os


class FolderChooser(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        drives = self.get_drives()
        self.filechooser = FileChooserIconView(path=drives[0], dirselect=True)
        self.select_button = Button(text="Chọn folder")
        self.select_button.bind(on_release=self.print_and_close)
        self.add_widget(self.filechooser)
        self.add_widget(self.select_button)
        self.selected_folder = None  # Biến lưu trữ đường dẫn

    def print_and_close(self, instance):
        self.selected_folder = self.filechooser.path
        print(f"Đường dẫn folder đã chọn: {self.selected_folder}")
        self.parent_popup.dismiss()  # Đóng cửa sổ popup

    def get_selected_folder(self):
        return self.selected_folder

    def get_drives(self):
        if os.name == 'nt':
            import string
            drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        else:
            drives = ['/']
        return drives


class MainApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        open_popup_button = Button(text="Open Folder Chooser")
        open_popup_button.bind(on_release=self.show_folder_chooser)
        root.add_widget(open_popup_button)
        return root

    def show_folder_chooser(self, instance):
        content = FolderChooser()
        folder_chooser_popup = Popup(title='Chọn folder', content=content, size_hint=(0.9, 0.9))
        content.parent_popup = folder_chooser_popup
        folder_chooser_popup.open()


if __name__ == '__main__':
    MainApp().run()
