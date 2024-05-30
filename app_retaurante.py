from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.lang import Builder

# Para realizar as chamadas na API REST
import requests

# Para gerenciar o tamanho da janela
from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '700')

# Popup para exibir mensagem de erro de autenticação
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

#class PopupErro(Popup):
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        self.title = 'Erro de autenticação'
#        self.size_hint = (0.7, 0.4)
#        self.auto_dismiss = False
#
#        self.box = BoxLayout(orientation='vertical')
#        self.box.add_widget(
#            Label(
#                text="Usuário ou senha inválidos!",
#            )
#        )
#
#        self.box.add_widget(
#            Button(
#                text="Fechar",
#                on_press=self.dismiss
#            )
#        )
#
#        self.add_widget(self.box)



#         self.popup_box = BoxLayout(orientation='vertical')
#         self.popup_box.add_widget(
#             Label(
#                 text='Usuário ou senha inválidos!',
#                 halign='center',
#                 text_size=(200, None),
#                 size_hint_y=None, height=100
#             )
#         )
#         self.popup_box.add_widget(Button(text='Fechar', on_press=self.dismiss))
#         self.add_widget(self.popup_box)

class PopupErro(Popup):
    pass





class TelaLogin(Screen):
        
    def autenticar(self):
        usuario = self.ids.txt_usuario.text
        senha = self.ids.txt_senha.text
               
        url = 'https://9717-168-232-136-83.ngrok-free.app/restaurante/autenticar'
        #url = 'http://localhost:5500/restaurante/autenticar'
        dados = {'usuario': usuario, 'senha': senha}
        resposta = requests.post(url, json=dados)
        if resposta.status_code == 200:
            self.manager.current = 'tela_principal'
        else:
            popup_erro = PopupErro()
            popup_erro.open()
            # PopupErro().open()

class TelaPrincipal(Screen):
    pass

class TelaGarcom(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import sqlite3
        #consulta ao vanco de dados para obter o cardapio
        conn = sqlite3.connect('cardapio.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM  cardapio')
        self.cardapio = cursor.fetchall()
        conn.close()
        self.cardapio_itens = [item[1] for item in self.cardapio if item[5] == 'Bar']
        #####
        self.pedido_mesa = {
            "mesa": "",
            "cozinha": [],
            "bar": [],
            "status": "pendente"
        }


    def atualiza_lista_cardapio(self):
        if self.ids.radio_bar.active:
            self.ids.itens_cardapio.values = [item[1] for item in self.cardapio if item[5] == 'Bar']
        elif self.ids.radio_cozinha.active:
            self.ids.itens_cardapio.values = [item[1] for item in self.cardapio if item[5] == 'Cozinha']

        self.ids.itens_cardapio.text = "Selecione"

    def decrementa_qtd_item(self):
        if int(self.ids.qtd_item.text) > 0:
            self.ids.qtd_item.text = str(int(self.ids.qtd_item.text) - 1)

    def incrementa_qtd_item(self):
        self.ids.qtd_item.text = str(int(self.ids.qtd_item.text) + 1)

    def inclui_pedido_na_lista(self):
        if self.ids.mesa_id.text == "Mesa":
            return
        qtd = self.ids.qtd_item.text
        pedido = self.ids.itens_cardapio.text
        if qtd == '0' or pedido == "Selecione":
            return
        
        self.ids.qtd_item.text = "0"
        self.ids.itens_cardapio.text = "Selecione"

        self.ids.itens_pedido.text += f"\n{qtd} - {pedido}"

        self.pedido_mesa['mesa'] = self.ids.mesa_id.text

        if self.ids.radio_bar.active:
            self.pedido_mesa['bar'].append(f"{qtd} - {pedido}")
        elif self.ids.radio_cozinha.active:
            self.pedido_mesa['cozinha'].append(f"{qtd} - {pedido}")

    def enviar_pedido(self):
        url = 'http://cf9d-168-232-136-83.ngrok-free.app/restaurante/criar_pedido'
        resposta = requests.post(url, json=self.pedido_mesa)



class GerenciadorTelas(ScreenManager):
    pass

# Builder.load_file('restaurante_float.kv')
# Builder.load_file('restaurante_grid.kv')
kv = Builder.load_file('restaurante_mixed_layout.kv')

class RestauranteApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    RestauranteApp().run()