from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
import reconhecimento_facial as rf
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel

class TelaInicial(Screen):
    def abrir_camera(self):
        rf.abrir_camera()

class FacesCadastradas(Screen):
    def on_enter(self, *args):
        nomes_cadastrados = rf.buscar_todos_nomes()
        lista = self.ids.lista
        for nome in nomes_cadastrados:
            tile = MDSmartTile(source=f"imagensRostos/{nome}.jpg",
                               radius=25,
                               pos_hint= {"center_x": .5,"center_y": .5, },
                               size_hint= (None,None),
                               box_color= (1, 1, 1, .2),
                               size=("220dp","220dp"),


                               )  # Substitua pelo caminho da imagem
            label = MDLabel(text=nome,
                            bold=True,
                            theme_text_color= "Custom",
                            text_color= "white",
                            halign='center')
            tile.add_widget(label)

            if len(rf.buscar_todos_nomes()) > 0:
                lista.add_widget(tile)
    def on_leave(self):
        lista = self.ids.lista
        for child in lista.children[:]:
            lista.remove_widget(child)
class CadastrarNovaFace (Screen):
    def explorador_arquivos(self):
        self.file_manager = MDFileManager(
            exit_manager=self.fechar_manager,
            select_path=self.arquivo_selecionado,
        )
        self.file_manager.ext = ['.jpg'] # faz com que só sejam procurados arquivos com essas extensões
        self.file_manager.show('/')
    def fechar_manager(self, *args):
        self.file_manager.close()
    def arquivo_selecionado(self, path):
        nome = self.ids.nome_rosto.text

        if rf.cadastro_rosto(nome,path) == 1:
            self.fechar_manager()
            self.aviso(1) # rosto nao existe e pode ser cadastrado
        elif rf.cadastro_rosto(nome,path) == 2:
            self.aviso(2) # não existe rosto na foto

        elif rf.cadastro_rosto(nome,path) == 3:
            self.aviso(3)
        else:
            self.aviso(0)


    def aviso(self,existenciaRosto):
        if existenciaRosto == 1:
            snackbar = Snackbar(text="Rosto cadastrado com sucesso!")

        elif  existenciaRosto == 2:
            snackbar = Snackbar(text="Essa imagem já contem um rosto cadastrado!")

        elif existenciaRosto == 3:
            snackbar = Snackbar(text="Esse nome já foi cadastrado!")
        else:
            snackbar = Snackbar(text="Não foi possivel detectar um rosto nessa imagem!")
        snackbar.open()
class gerenciador_Telas(ScreenManager):
    pass
class CadastroRosto(MDApp):
    def build(self):
        return Builder.load_file('telas.kv')
CadastroRosto().run()