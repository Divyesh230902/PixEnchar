import flet
import PixEnchar
from PixEnchar import PixEnchar
from time import sleep
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Text,
    icons,
    ProgressRing,
)


class FilePickerApp:
    def __init__(self, page: Page):
        self.page = page
        self.selected_files = Text()
        self.progress_ring = ProgressRing()
        self.save_file_path = Text()
        self.directory_path = Text()
        self.setup_file_dialogs()
        self.setup_buttons()

    def setup_file_dialogs(self):
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        self.save_file_dialog = FilePicker(on_result=self.save_file_directory)
        self.get_directory_dialog = FilePicker(on_result=self.get_directory_result)

        self.page.overlay.extend(
            [self.pick_files_dialog, self.save_file_dialog, self.get_directory_dialog]
        )

    def setup_buttons(self):
        self.start_progress_ring_button = ElevatedButton(
            "Start",
            icon=icons.PLAY_CIRCLE,
            on_click=lambda _: self.run_backend(self.directory_path.value,self.save_file_path.value), 
        )

        self.page.add(
            flet.Column(controls=[
        flet.Row([
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: self.pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                self.selected_files,
            ]),
        flet.Row([
                ElevatedButton(
                    "Save Directory",
                    icon=icons.SAVE,
                    on_click=lambda _: self.save_file_dialog.get_directory_path(),
                    disabled=self.page.web,
                ),
                self.save_file_path,
            ]),
        flet.Row([
                ElevatedButton(
                    "Input directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: self.get_directory_dialog.get_directory_path(),
                    disabled=self.page.web,
                ),
                self.directory_path,
            ])
    ])
        )
        self.page.add(self.start_progress_ring_button)

    def create_button_with_action(self, label, icon, action, text_widget):
        return flet.Row(
            [
                ElevatedButton(label, icon=icon, on_click=action),
                text_widget,
            ]
        )

    def pick_files_result(self, e: FilePickerResultEvent):
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.selected_files.update()

    def save_file_directory(self, e: FilePickerResultEvent):
        self.save_file_path.value = e.path if e.path else "Cancelled!"
        self.save_file_path.update()
        text_output= self.save_file_path.value
        return self.show_output(text_output)
    
    def show_output(self,dfg):
        print("Output:" ,dfg) 

    def get_directory_result(self, e: FilePickerResultEvent):
        self.directory_path.value = e.path if e.path else "Cancelled!"
        self.directory_path.update()

    def start_progress_ring(self):
        pr = flet.ProgressRing()
        self.page.add(flet.Column(
            [flet.ProgressRing(), flet.Text("wait for a moment...")],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        ))

        for i in range(0, 101):
            pr.value = i * 0.01
            sleep(0.1)
            self.page.update()

        for i in range(0, 101):
            self.progress_ring.value = i * 0.01
            sleep(0.1)
            self.page.update()

        if self.selected_files.value:
            files = self.selected_files.value.split(",")
            output_path = self.save_file_path.value
            for i in range(5):
                if i < len(files):
                    self.progress_ring.update(i / 5)
                    with open(f"{output_path}/{files[i]}", "wb") as f:
                        f.write(open(files[i], "rb").read())
            self.progress_ring.stop()

        self.page.add(Text("Completed!"))
    
    def run_backend(self,input_path, output_path):
        pe = PixEnchar(input_path, output_path)
        pe.pixenchar()
        pe.change_dpi() 

def main(page: Page):
    app = FilePickerApp(page)

flet.app(target=main)

  

# if __name__ == '__main__':
#     input_path = FilePickerApp.directory_path()
#     output_path = FilePickerApp.save_file_path()

#     pe = PixEnchar(input_path, output_path)
#     pe.pixenchar()
#     pe.change_dpi()
# sk = PixEnchar.PixEnchar(FilePickerApp.save_file_directory,FilePickerApp.get_directory_result)