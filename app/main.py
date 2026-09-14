from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

class MessengerApp(App):
    def build(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((SERVER_IP, SERVER_PORT))
        except Exception as e:
            print("Ошибка:", e)

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat.bind(minimum_height=self.chat.setter('height'))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)

        bottom = BoxLayout(size_hint=(1, 0.15), spacing=5)
        self.input = TextInput(hint_text='Сообщение...', multiline=False)
        send_btn = Button(text='Отпр', size_hint=(0.3, 1))
        send_btn.bind(on_press=self.send_msg)
        bottom.add_widget(self.input)
        bottom.add_widget(send_btn)
        root.add_widget(bottom)

        threading.Thread(target=self.receive, daemon=True).start()
        return root

    def add_msg(self, text):
        lbl = Label(text=text, size_hint_y=None, height=40, halign='left')
        self.chat.add_widget(lbl)
        self.scroll.scroll_y = 0

    def send_msg(self, instance):
        msg = self.input.text.strip()
        if msg:
            try:
                self.sock.send(msg.encode())
            except:
                pass
            self.add_msg(f"[Вы]: {msg}")
            self.input.text = ''

    def receive(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    Clock.schedule_once(lambda dt, m=data.decode(): self.add_msg(m))
            except:
                break

if __name__ == '__main__':
    MessengerApp().run()
