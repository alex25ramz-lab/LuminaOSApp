# main.py
# -----------------------------------------------------------------
#   LUMINA OS – CYBERPUNK HUD EDITION (V5 COMPLETA)
#   Incluye: Shop, Temas Dinámicos, Bitácora Flash y Modo Overclock
# -----------------------------------------------------------------

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '720')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

import json
import os
import threading
import requests  
from random import choice
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

API_URL = "https://focusmind-server.onrender.com/api/misiones"

# -----------------------------------------------------------------
# KV‑STRING: Interfaz Sci-Fi / Cyberpunk Terminal V5
# -----------------------------------------------------------------
KV = '''
ScreenManager:
    id: screen_manager
    LoginScreen:
    MainScreen:

<LoginScreen>:
    name: "login_screen"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.04, 0.06, 0.09, 1
        padding: dp(24)
        spacing: dp(20)
        alignment: "center"

        Widget:
            size_hint_y: None
            height: dp(40)

        MDIconButton:
            icon: "terminal"
            user_font_size: "64sp"
            theme_text_color: "Custom"
            text_color: app.theme_color
            pos_hint: {"center_x": .5}

        MDLabel:
            text: "LUMINA OS"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_color
            bold: True

        MDLabel:
            text: "SISTEMA OPERATIVO DE ENFOQUE & PRODUCTIVIDAD"
            font_style: "Caption"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.7, 0.8, 0.9, 0.8

        MDTextField:
            id: user_input
            hint_text: "Identificador de Operador"
            mode: "rectangle"
            line_color_focus: app.theme_color
            text_color_focus: 1, 1, 1, 1
            hint_text_color_focus: app.theme_color
            pos_hint: {"center_x": .5}
            size_hint_x: 0.9

        MDFillRoundFlatButton:
            text: "INICIALIZAR SISTEMA"
            md_bg_color: app.theme_color
            text_color: 0.04, 0.06, 0.09, 1
            pos_hint: {"center_x": .5}
            size_hint_x: 0.9
            bold: True
            on_release: app.procesar_login(user_input.text)

        Widget:

<MainScreen>:
    name: "main_screen"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.04, 0.06, 0.09, 1

        MDTopAppBar:
            id: toolbar
            title: app.toolbar_title
            elevation: 2
            md_bg_color: 0.07, 0.09, 0.14, 1
            specific_text_color: app.theme_color
            left_action_items: [["orbit", lambda x: app.disparar_chequeo_web(0)]]
            right_action_items: [["store", lambda x: app.abrir_tienda()], ["shield-check", lambda x: app.show_profile()]]

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                # -------------------- PANEL HUD ESTADO --------------------
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(60)
                    spacing: dp(10)
                    
                    MDCard:
                        radius: [10,]
                        md_bg_color: 0.08, 0.12, 0.18, 0.9
                        padding: dp(8)
                        ripple_behavior: True
                        on_release: app.ver_racha()
                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: dp(6)
                            MDIconButton:
                                icon: "fire"
                                theme_text_color: "Custom"
                                text_color: (1, 0.5, 0, 1) if app.racha > 0 else (0.4, 0.4, 0.4, 1)
                                pos_hint: {"center_y": .5}
                            MDBoxLayout:
                                orientation: "vertical"
                                pos_hint: {"center_y": .5}
                                MDLabel:
                                    text: "RACHA"
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: 0.6, 0.7, 0.8, 1
                                MDLabel:
                                    text: str(app.racha) + " DÍAS"
                                    font_style: "Subtitle2"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                    MDCard:
                        radius: [10,]
                        md_bg_color: 0.08, 0.12, 0.18, 0.9
                        padding: dp(8)
                        ripple_behavior: True
                        on_release: app.command_desafio()
                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: dp(6)
                            MDIconButton:
                                icon: "lightning-bolt"
                                theme_text_color: "Custom"
                                text_color: app.theme_color
                                pos_hint: {"center_y": .5}
                            MDBoxLayout:
                                orientation: "vertical"
                                pos_hint: {"center_y": .5}
                                MDLabel:
                                    text: "DESAFÍO"
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: 0.6, 0.7, 0.8, 1
                                MDLabel:
                                    text: "ACTIVO"
                                    font_style: "Subtitle2"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: app.theme_color

                # -------------------- NIVEL / XP HUD --------------------
                MDCard:
                    size_hint_y: None
                    height: dp(80)
                    radius: [10,]
                    md_bg_color: 0.08, 0.12, 0.18, 0.9
                    padding: dp(12)
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(6)
                        MDBoxLayout:
                            MDLabel:
                                text: "NIVEL " + str(app.nivel)
                                font_style: "Subtitle1"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.theme_color
                            MDLabel:
                                text: str(app.xp) + " / " + str(app.xp_for_next) + " XP"
                                font_style: "Caption"
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: 0.7, 0.8, 0.9, 1
                        MDProgressBar:
                            id: xp_bar
                            value: app.xp_percent
                            color: app.theme_color
                            size_hint_y: None
                            height: dp(6)

                # -------------------- POMODORO TIMER --------------------
                MDCard:
                    size_hint_y: None
                    height: dp(130)
                    radius: [10,]
                    md_bg_color: 0.08, 0.12, 0.18, 0.9
                    padding: dp(12)
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)
                        MDLabel:
                            text: "MÓDULO DE ENFOQUE POMODORO"
                            font_style: "Caption"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.6, 0.7, 0.8, 1
                        MDLabel:
                            id: timer_label
                            text: app.time_str
                            font_style: "H3"
                            halign: "center"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                        MDBoxLayout:
                            spacing: dp(10)
                            size_hint_x: None
                            width: self.minimum_width
                            pos_hint: {"center_x": .5}
                            MDFillRoundFlatButton:
                                id: timer_btn
                                text: "INICIAR CICLO"
                                md_bg_color: app.theme_color
                                text_color: 0.04, 0.06, 0.09, 1
                                bold: True
                                on_release: app.toggle_timer()
                            MDFillRoundFlatButton:
                                text: "⚡ OVERCLOCK"
                                md_bg_color: 1, 0.2, 0.4, 1
                                text_color: 1, 1, 1, 1
                                bold: True
                                on_release: app.activar_overclock()

                # -------------------- PANEL DE CONTROL DE MISIONES --------------------
                MDCard:
                    size_hint_y: None
                    height: dp(200)
                    radius: [10,]
                    md_bg_color: 0.08, 0.12, 0.18, 0.9
                    padding: dp(12)
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)
                        MDLabel:
                            text: "REGISTRO DE OPERACIONES"
                            font_style: "Caption"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.theme_color
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(42)
                            spacing: dp(8)
                            MDTextField:
                                id: task_input
                                hint_text: "Escribir nueva misión..."
                                mode: "rectangle"
                                line_color_focus: app.theme_color
                                text_color_focus: 1, 1, 1, 1
                            MDFillRoundFlatButton:
                                text: "REGISTRAR"
                                md_bg_color: app.theme_color
                                text_color: 0.04, 0.06, 0.09, 1
                                bold: True
                                on_release: app.add_task_post()
                        ScrollView:
                            MDList:
                                id: task_list

                # -------------------- BITÁCORA FLASH --------------------
                MDCard:
                    size_hint_y: None
                    height: dp(150)
                    radius: [10,]
                    md_bg_color: 0.08, 0.12, 0.18, 0.9
                    padding: dp(12)
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(6)
                        MDLabel:
                            text: "BITÁCORA FLASH (NOTAS DE CAMPO)"
                            font_style: "Caption"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.theme_color
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(40)
                            spacing: dp(8)
                            MDTextField:
                                id: log_input
                                hint_text: "Anotación rápida..."
                                mode: "rectangle"
                                line_color_focus: app.theme_color
                                text_color_focus: 1, 1, 1, 1
                            MDFillRoundFlatButton:
                                text: "GUARDAR"
                                md_bg_color: app.theme_color
                                text_color: 0.04, 0.06, 0.09, 1
                                bold: True
                                on_release: app.guardar_nota_bitacora()
                        ScrollView:
                            MDList:
                                id: bitacora_list

                # -------------------- REGISTRO DE EVENTOS --------------------
                MDLabel:
                    text: "CONSOLA DE EVENTOS Y LOGROS"
                    font_style: "Caption"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.6, 0.7, 0.8, 0.8
                    padding: [dp(4), dp(8), 0, 0]

                MDBoxLayout:
                    id: feed_container
                    orientation: "vertical"
                    spacing: dp(12)
                    size_hint_y: None
                    height: self.minimum_height

                # ---------- ACCIONES RÁPIDAS ----------
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(45)
                    spacing: dp(8)
                    MDFillRoundFlatButton:
                        text: "🎯 OBJETIVO"
                        font_size: dp(11)
                        md_bg_color: 0.12, 0.16, 0.24, 1
                        text_color: app.theme_color
                        on_release: app.command_objetivo()
                    MDFillRoundFlatButton:
                        text: "🔮 PREDICCIÓN"
                        font_size: dp(11)
                        md_bg_color: 0.12, 0.16, 0.24, 1
                        text_color: app.theme_color
                        on_release: app.command_predecir()
'''

class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class FeedPostCard(MDCard):
    likes = NumericProperty(0)
    liked = BooleanProperty(False)

    def __init__(self, autor, contenido, hashtag="#SystemLog", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = "140dp"
        self.radius = [10]
        self.md_bg_color = [0.08, 0.12, 0.18, 0.9]
        self.padding = "12dp"
        self.spacing = "4dp"
        
        app = MDApp.get_running_app()
        header = MDBoxLayout(size_hint_y=None, height="28dp", spacing="6dp")
        header.add_widget(MDIconButton(icon="account-badge-outline", theme_text_color="Custom", text_color=app.theme_color, size_hint=(None, None), size=("24dp", "24dp")))
        header.add_widget(MDLabel(text=f"OPERADOR: @{autor}", font_style="Caption", bold=True, theme_text_color="Custom", text_color=app.theme_color))
        self.add_widget(header)
        
        self.add_widget(MDLabel(text=contenido, font_style="Body2", theme_text_color="Custom", text_color=[0.9, 0.95, 1, 1]))
        self.add_widget(MDLabel(text=hashtag, font_style="Caption", theme_text_color="Custom", text_color=[0.5, 0.6, 0.7, 1]))
        
        self.footer = MDBoxLayout(size_hint_y=None, height="28dp", spacing="6dp")
        self.like_btn = MDIconButton(icon="thumb-up-outline", theme_text_color="Custom", text_color=[1, 1, 1, 1], size_hint=(None, None), size=("24dp", "24dp"))
        self.like_btn.bind(on_release=self.press_like)
        
        self.likes_label = MDLabel(text="0 confirmaciones", font_style="Caption", theme_text_color="Custom", text_color=[0.6, 0.7, 0.8, 0.7])
        
        self.footer.add_widget(self.like_btn)
        self.footer.add_widget(self.likes_label)
        self.add_widget(self.footer)

    def press_like(self, instance):
        app = MDApp.get_running_app()
        self.liked = not self.liked
        if self.liked:
            self.likes += 1
            self.like_btn.icon = "thumb-up"
            self.like_btn.text_color = app.theme_color
            app.add_xp(10, Notify=False)
        else:
            self.likes -= 1
            self.like_btn.icon = "thumb-up-outline"
            self.like_btn.text_color = [1, 1, 1, 1]
            
        self.likes_label.text = f"{self.likes} confirmaciones"


class ContainerCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class TaskItem(OneLineAvatarIconListItem):
    def __init__(self, task_text, **kwargs):
        super().__init__(**kwargs)
        self.text = task_text
        self.theme_text_color = "Custom"
        self.text_color = (1, 1, 1, 1)
        self.cb = ContainerCheckbox()
        self.cb.bind(active=self.toggle_done)
        self.add_widget(self.cb)
        self.completed = False

    def toggle_done(self, checkbox, value):
        if value and not self.completed:
            self.completed = True
            self.cb.disabled = True
            app = MDApp.get_running_app()
            app.add_xp(150)
            app.publicar_logro_feed(f"Misión Ejecutada: {self.text}")


class LuminaCyberApp(MDApp):
    usuario_actual = StringProperty("Invitado")
    toolbar_title = StringProperty("LUMINA OS :: TERMINAL")
    nivel = NumericProperty(1)
    xp = NumericProperty(0)
    xp_for_next = NumericProperty(1000)
    xp_percent = NumericProperty(0)
    racha = NumericProperty(1)
    timer_running = BooleanProperty(False)
    seconds_left = NumericProperty(25 * 60)
    time_str = StringProperty("25:00")
    theme_color = ListProperty([0, 0.94, 1, 1])  # Color Cyan por defecto

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        self.data_file = os.path.join(self.user_data_dir, "lumina_data.json")
        self.root = Builder.load_string(KV)
        self.dialog = None
        self.ultima_mision_id = None  
        
        self.cargar_progreso_local()
        
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.disparar_chequeo_web, 4)
        return self.root

    def procesar_login(self, username):
        username = username.strip()
        if not username:
            self.show_dialog("ERROR DE ACCESO", "Se requiere un identificador de operador válido.")
            return
        
        self.usuario_actual = username
        self.toolbar_title = f"LUMINA OS :: @{username.upper()}"
        self.root.current = "main_screen"
        
        self.publicar_logro_feed(f"Sesión iniciada en el terminal de control.", hashtag="#SystemReady")
        self.disparar_chequeo_web(0)

    def disparar_chequeo_web(self, dt):
        if self.root and self.root.current == "main_screen":
            threading.Thread(target=self.fetch_datos_servidor, daemon=True).start()

    def fetch_datos_servidor(self):
        try:
            response = requests.get(API_URL, timeout=4)
            if response.status_code == 200:
                data = response.json()
                asignado = str(data.get("asignar_a", "")).strip().lower()
                usuario_target = str(self.usuario_actual).strip().lower()
                
                mision_texto = data.get("mision")
                mision_id = data.get("id")
                minutos = int(data.get("minutos", 25))

                if asignado == usuario_target and mision_id != self.ultima_mision_id:
                    self.ultima_mision_id = mision_id
                    Clock.schedule_once(lambda dt: self.cargar_mision_remota(mision_texto, minutes=minutos))
        except Exception as e:
            print(f"Sincronizando con servidor... (Detalle: {e})")

    def cargar_mision_remota(self, texto_mision, minutes):
        main_ids = self.root.get_screen('main_screen').ids
        main_ids.task_input.text = str(texto_mision)
        
        self.seconds_left = minutes * 60
        m, s = divmod(self.seconds_left, 60)
        self.time_str = f"{int(m):02d}:{int(s):02d}"

        self.publicar_logro_feed(f"Comando remoto recibido: {texto_mision}", hashtag="#RemoteOverride")
        self.show_dialog("🚨 COMANDO REMOTO", f"Nueva instrucción desde el servidor:\n\n'{texto_mision}'")

    def publicar_logro_feed(self, texto, hashtag="#Operaciones"):
        nuevo_post = FeedPostCard(autor=self.usuario_actual, contenido=texto, hashtag=hashtag)
        self.root.get_screen('main_screen').ids.feed_container.add_widget(nuevo_post)

    def ver_racha(self):
        self.show_dialog("🔥 ESTADO DE RACHA", f"Operador @{self.usuario_actual}, mantienes una secuencia activa de {self.racha} días.")

    def toggle_timer(self):
        self.timer_running = not self.timer_running
        self.root.get_screen('main_screen').ids.timer_btn.text = "PAUSAR CICLO" if self.timer_running else "INICIAR CICLO"

    def update_timer(self, dt):
        if self.root.current != "main_screen":
            return
            
        if self.timer_running and self.seconds_left > 0:
            self.seconds_left -= 1
            m, s = divmod(self.seconds_left, 60)
            self.time_str = f"{int(m):02d}:{int(s):02d}"
        elif self.seconds_left == 0 and self.timer_running:
            self.timer_running = False
            self.root.get_screen('main_screen').ids.timer_btn.text = "INICIAR CICLO"
            self.seconds_left = 25 * 60
            self.time_str = "25:00"
            self.add_xp(250)
            self.publicar_logro_feed("Ciclo Pomodoro de 25 minutos completado exitosamente.", hashtag="#FocusComplete")
            self.show_dialog("⏰ CICLO FINALIZADO", "Bloque de enfoque completado. Registro actualizado.")

    def activar_overclock(self):
        self.timer_running = True
        self.seconds_left = 15 * 60  # Bloque rápido e intenso de 15 minutos
        self.root.get_screen('main_screen').ids.timer_btn.text = "PAUSAR CICLO"
        self.show_dialog("⚡ OVERCLOCK ACTIVADO", "Modo de alto rendimiento activado: 15 minutos de enfoque estricto sin distracciones.")

    def add_task_post(self):
        main_ids = self.root.get_screen('main_screen').ids
        txt = main_ids.task_input.text.strip()
        if not txt: return
        item = TaskItem(txt)
        main_ids.task_list.add_widget(item)
        main_ids.task_input.text = ""
        self.publicar_logro_feed(f"Misión añadida a la cola: {txt}", hashtag="#NewTask")

    def guardar_nota_bitacora(self):
        main_ids = self.root.get_screen('main_screen').ids
        txt = main_ids.log_input.text.strip()
        if not txt: return
        item = TwoLineListItem(text=txt, secondary_text="Anotación de Campo", theme_text_color="Custom", text_color=(1, 1, 1, 1), secondary_text_color=(0.6, 0.7, 0.8, 0.7))
        main_ids.bitacora_list.add_widget(item)
        main_ids.log_input.text = ""

    def abrir_tienda(self):
        msg = f"CRÉDITOS DISPONIBLES: {self.xp} XP\n\n1. Tema Matrix Green (300 XP)\n2. Tema Solar Amber (500 XP)\n3. Recompensa Café/Break (1000 XP)"
        
        def comprar_item(costo, accion):
            if self.xp >= costo:
                self.xp -= costo
                accion()
                self.guardar_progreso_local()
                self.dialog.dismiss()
                self.show_dialog("🛒 COMPRA EXITOSA", "Recompensa canjeada correctamente.")
            else:
                self.show_dialog("❌ FONDOS INSUFICIENTES", "Necesitas más XP para desbloquear este elemento.")

        if self.dialog:
            self.dialog.dismiss()
            
        self.dialog = MDDialog(
            title="🛒 CYBER SHOP & RECOMPENSAS",
            text=msg,
            size_hint=(0.85, None),
            buttons=[
                MDFillRoundFlatButton(
                    text="MATRIX (300 XP)",
                    md_bg_color=(0, 0.9, 0.3, 1),
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: comprar_item(300, lambda: setattr(self, 'theme_color', [0, 1, 0.4, 1]))
                ),
                MDFillRoundFlatButton(
                    text="AMBER (500 XP)",
                    md_bg_color=(1, 0.7, 0, 1),
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: comprar_item(500, lambda: setattr(self, 'theme_color', [1, 0.7, 0, 1]))
                ),
                MDFillRoundFlatButton(
                    text="CERRAR",
                    md_bg_color=(0.2, 0.2, 0.2, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def add_xp(self, amount, Notify=True):
        self.xp += amount
        self.xp_percent = (self.xp / self.xp_for_next) * 100
        if self.xp >= self.xp_for_next:
            self.nivel += 1
            self.xp -= self.xp_for_next
            self.xp_for_next = int(self.xp_for_next * 1.25)
            self.xp_percent = (self.xp / self.xp_for_next) * 100
            self.publicar_logro_feed(f"¡SISTEMA ACTUALIZADO AL NIVEL {self.nivel}!", hashtag="#LevelUp")
            if Notify:
                self.show_dialog("🚀 ASCENSO DE NIVEL", f"Capacidad del sistema incrementada. Nivel actual: {self.nivel}.")
        self.guardar_progreso_local()

    def command_objetivo(self):
        objetivos = ["Refactorizar arquitectura de software", "Optimizar tiempos de ejecución", "Auditar seguridad de API", "Diseñar interfaz táctica"]
        obj = choice(objetivos)
        self.root.get_screen('main_screen').ids.task_input.text = obj

    def command_predecir(self):
        pred = ["Rendimiento estimado +20% para la sesión actual", "Secuencia de tareas optimizada con éxito", "Cero interrupciones detectadas en el entorno"]
        self.show_dialog("🔮 ANÁLISIS PREDICTIVO", choice(pred))

    def command_desafio(self):
        desafios = ["Completa 2 misiones sin pausar el Pomodoro", "Mantén el ciclo activo por 50 minutos para doble XP"]
        self.show_dialog("⚡ DESAFÍO TÁCTICO", choice(desafios))

    def guardar_progreso_local(self):
        data = {
            "nivel": self.nivel,
            "xp": self.xp,
            "xp_for_next": self.xp_for_next,
            "racha": self.racha
        }
        try:
            with open(self.data_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error guardando datos locales: {e}")

    def cargar_progreso_local(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.nivel = data.get("nivel", 1)
                    self.xp = data.get("xp", 0)
                    self.xp_for_next = data.get("xp_for_next", 1000)
                    self.racha = data.get("racha", 1)
                    self.xp_percent = (self.xp / self.xp_for_next) * 100
            except Exception as e:
                print(f"Error cargando datos locales: {e}")

    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.85, None),
            buttons=[
                MDFillRoundFlatButton(
                    text="CONFIRMAR",
                    md_bg_color=self.theme_color,
                    text_color=(0.04, 0.06, 0.09, 1),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def show_profile(self):
        self.show_dialog("🛡️ EXPEDIENTE DE OPERADOR", f"OPERADOR: @{self.usuario_actual.upper()}\nNivel de Acceso: {self.nivel}\nExperiencia Acumulada: {self.xp} XP")

if __name__ == "__main__":
    LuminaCyberApp().run()