from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDRoundFlatButton,MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.spinner import MDSpinner

from pytube import YouTube
import threading
import os
import time

interfaz = """ 
MDBoxLayout:
    orientation: 'vertical'
    
    Screen:
        MDIcon:
            icon: 'play-circle'
            font_size: 100
            pos_hint: {"center_x": 0.84, "center_y": 0.9}
            
        MDLabel:
            text: "Wling-Tube"
            theme_text_color: "Custom"
            text_color: "red"
            font_size: 100
            halign: "center"
            pos_hint: {"center_x": 0.42, "center_y": 0.9}
        
        MDIcon:
            icon: 'baseball-diamond'
            font_size: 350
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
        
        MDLabel:
            text: "BY: STE4LPH"
            theme_text_color: "Custom"
            text_color: "black"
            font_size: 20
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 0.85}
            
        MDTextField:
            id: URL                   
            icon_left: "magnify"
            hint_text: "URL, palabras clave..."
            line_color_focus: "blue"
            font_size: 30    
            fill_color_normal: "white"
            mode: "round"                  
            width: 600
            size_hint_x: None
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
        
        MDRectangleFlatIconButton:
            id: mp4
            icon: 'movie'
            icon_color: "white"
            text: "MP4"
            text_color: "white"
            md_bg_color: "#3498DB"
            halign: "center"
            size_hint: 0.25, 0.065
            font_size: 30
            pos_hint: {"center_x": 0.3, "center_y": 0.35}
            opacity: 0
            on_release: app.MP4()
        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
            active: False
        
        MDLabel:
            id: finalizado_label
            text: "La descarga a terminado! ^_^"
            theme_text_color: "Custom"
            text_color: "red"
            font_size: 30
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 0.47}
            opacity: 0
            
        MDRectangleFlatIconButton:
            id: mp3
            icon: 'music-note-outline'
            icon_color: "white"
            text: "MP3"
            text_color: "white"
            md_bg_color: "#3498DB"
            halign: "center"
            size_hint: 0.25, 0.065
            font_size: 30
            pos_hint: {"center_x": 0.3, "center_y": 0.35}
            on_release: app.MP3()
   
        MDRectangleFlatIconButton:
            text: "Descargar"
            text_color: "white"
            icon: "download"
            icon_color: "white"
            size_hint: 0.35, 0.065
            font_size: 30
            md_bg_color: "red"            
            line_color: "red"
            pos_hint: {"center_x": 0.65, "center_y": 0.35}
            on_release: app.DESCARGAR()
"""
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import threading
import os
from kivy.clock import Clock

class MIAPP(MDApp):
    def build(self):
        return Builder.load_string(interfaz)

    def MP3(self):
        global mp3
        mp3 = "musica"
        self.root.ids.mp3.disabled = True
        self.root.ids.mp3.opacity = 0
        self.root.ids.mp4.disabled = False
        self.root.ids.mp4.opacity = 1
        #Clock.schedule_once(self.show_finalizado, 0)

    def MP4(self):
        global mp4
        mp4 = "video"
        self.root.ids.mp4.disabled = True
        self.root.ids.mp4.opacity = 0
        self.root.ids.mp3.disabled = False
        self.root.ids.mp3.opacity = 1          
        
    def DESCARGAR(self):
        def descargar_en_segundo_plano():
            
            if self.root.ids.mp3.opacity == 1:
                
                audio_stream = yt.streams.filter(only_audio=True).first()
                output_path = '/storage/emulated/0/Download'
                download_path = audio_stream.download(output_path=output_path)
                mp3_path = download_path.replace(".mp4", ".mp3")
                os.rename(download_path, mp3_path)
                spinner.active = False
                Clock.schedule_once(self.show_finalizado, 0)
            
            elif self.root.ids.mp4.opacity == 1:
                video_stream = yt.streams.get_highest_resolution()
                output_path = '/storage/emulated/0/Download'
                download_path = video_stream.download(output_path=output_path)
                spinner.active = False
                Clock.schedule_once(self.show_finalizado, 0)
            
        url = self.root.ids.URL.text
        try:
            if len(url) > 0:
                yt = YouTube(url)
                respuesta = True
            else:
                self.show_result_dialog("Error #1", "No ingresaste nada")
                self.root.ids.finalizado_label.opacity = 0
                respuesta = False
        except:
            self.show_result_dialog("Error #2", "La URL es inválida")
            self.root.ids.finalizado_label.opacity = 0
            respuesta = False

        if respuesta:
            spinner = self.root.ids.spinner
            self.root.ids.finalizado_label.opacity = 0
            hilo_one = threading.Thread(target=descargar_en_segundo_plano)
            hilo_one.start()
            self.show_result_dialog("Verificado", "Descargando . . .")
            spinner.active = True

    def show_finalizado(self, dt):
        self.root.ids.finalizado_label.opacity = 1

    def show_result_dialog(self, title_text, result_text):
        dialog = MDDialog(
            title=title_text,
            text=result_text,
            buttons=[
                MDFlatButton(
                    text="Ok",
                    on_release=lambda *args: dialog.dismiss()
                )
            ],
        )
        dialog.open()

if __name__ == "__main__":
    MIAPP().run()
    
