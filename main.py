from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Carrega a interface do usuário do arquivo main.kv
Builder.load_file('main.kv')

class MyApp(App):
    def build(self):
        return MyBoxLayout()

class MyBoxLayout(BoxLayout):
    pass

if __name__ == '__main__':
    MyApp().run()
