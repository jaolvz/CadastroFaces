from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


class TelaInicial(Screen):
    pass
class gerenciador_Telas(ScreenManager):
    pass
class CadastroRosto(MDApp):
    def build(self):
        return Builder.load_file('telas.kv')
CadastroRosto().run()