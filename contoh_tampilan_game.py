from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFillRoundFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
import random
import time

# Simulasi ukuran layar mobile (Portrait)
Window.size = (360, 640)

# Konfigurasi Tema
THEMES = {
    "Green": {
        "primary": "Green",
        "bg_light": "#F1F8E9",
        "bg_dark": "#1B5E20",
        "accent": "#FFC107"
    },
    "Blue": {
        "primary": "Blue",
        "bg_light": "#E3F2FD",
        "bg_dark": "#0D47A1",
        "accent": "#00BCD4"
    }
}

class LayarHome(MDScreen):
    """Layar pembuka aplikasi yang lebih interaktif"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.root_layout = MDFloatLayout()

        # Dekorasi Lingkaran di Background (Simulasi)
        self.add_decoration()

        content_layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(10))
        content_layout.add_widget(MDBoxLayout(size_hint_y=0.2))

        # Logo/Icon Animasi
        self.logo = MDIcon(
            icon="brain",
            font_size=dp(80),
            halign="center",
            theme_text_color="Primary",
            pos_hint={"center_x": 0.5}
        )
        content_layout.add_widget(self.logo)

        content_layout.add_widget(MDLabel(
            text="KUIS PINTAR",
            halign="center",
            font_style="H4",
            theme_text_color="Primary",
            bold=True,
        ))

        content_layout.add_widget(MDLabel(
            text="Asah otakmu dengan tantangan seru!",
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
        ))

        content_layout.add_widget(MDBoxLayout(size_hint_y=0.2))

        self.btn_mulai = MDFillRoundFlatButton(
            text="MULAI BERMAIN",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height=dp(56),
            font_size=dp(18),
            on_release=self.start_anim
        )
        content_layout.add_widget(self.btn_mulai)
        
        # Pilihan Mode (Light/Dark)
        self.theme_btn = MDFillRoundFlatIconButton(
            icon="weather-night",
            text="DARK MODE",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height=dp(50),
            on_release=self.toggle_theme
        )
        content_layout.add_widget(self.theme_btn)

        content_layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        self.root_layout.add_widget(content_layout)
        self.add_widget(self.root_layout)

    def add_decoration(self):
        # Placeholder untuk dekorasi visual tambahan jika diperlukan
        pass

    def toggle_theme(self, instance):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
            self.theme_btn.icon = "weather-sunny"
            self.theme_btn.text = "LIGHT MODE"
        else:
            app.theme_cls.theme_style = "Light"
            self.theme_btn.icon = "weather-night"
            self.theme_btn.text = "DARK MODE"
        
        # Animasi kecil pada logo saat ganti tema
        anim = Animation(font_size=dp(100), duration=0.2) + Animation(font_size=dp(80), duration=0.2)
        anim.start(self.logo)

    def start_anim(self, instance):
        anim = Animation(font_size=dp(22), duration=0.1) + Animation(font_size=dp(18), duration=0.1)
        anim.bind(on_complete=lambda *args: setattr(self.manager, 'current', 'layar_beranda'))
        anim.start(instance)

class Beranda(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        main_layout = MDBoxLayout(orientation='vertical')
        
        self.toolbar = MDTopAppBar(title="Pilih Jenjang", elevation=4)
        self.toolbar.left_action_items = [['arrow-left', lambda x: self.go_back()]]
        main_layout.add_widget(self.toolbar)

        content = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        # Card Header
        header_card = MDCard(
            orientation='vertical', padding=dp(15), size_hint=(1, None), height=dp(100),
            radius=[dp(20),], elevation=2, md_bg_color=MDApp.get_running_app().theme_cls.primary_color
        )
        header_card.add_widget(MDLabel(
            text="SIAP BELAJAR?", halign="center", font_style="H5", 
            theme_text_color="Custom", text_color=[1,1,1,1], bold=True
        ))
        header_card.add_widget(MDLabel(
            text="Pilih tingkat kesulitan di bawah", halign="center", 
            font_style="Caption", theme_text_color="Custom", text_color=[0.9,0.9,0.9,1]
        ))
        content.add_widget(header_card)

        levels = [
            ("TK", "baby-face-outline", "Belajar Mengenal"),
            ("SD", "school", "Dasar Pengetahuan"),
            ("SMP", "book-open-variant", "Uji Pemahaman"),
            ("SMA", "brain", "Tantangan Logika")
        ]
        
        for level_text, icon, desc in levels:
            btn = MDCard(
                orientation='horizontal', padding=dp(10), size_hint=(1, None), height=dp(70),
                radius=[dp(15),], ripple_behavior=True, on_release=lambda x, l=level_text: self.start_level(l)
            )
            btn.add_widget(MDIcon(icon=icon, size_hint_x=0.2, halign="center", theme_text_color="Primary"))
            
            text_box = MDBoxLayout(orientation='vertical', padding=[dp(10), 0])
            text_box.add_widget(MDLabel(text=f"Level {level_text}", font_style="H6", bold=True))
            text_box.add_widget(MDLabel(text=desc, font_style="Caption", theme_text_color="Secondary"))
            
            btn.add_widget(text_box)
            btn.add_widget(MDIcon(icon="chevron-right", size_hint_x=0.1, halign="center"))
            content.add_widget(btn)

        content.add_widget(MDBoxLayout()) # Spacer
        main_layout.add_widget(content)
        self.add_widget(main_layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'layar_home'

    def start_level(self, level):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.get_screen('layar_kuis').selected_level = level
        self.manager.current = 'layar_kuis'

class LayarKuis(MDScreen):
    selected_level = None
    timer_event = None
    total_time = 10

    questions_data = {
        "TK": [
            {"question": "Berapa banyak jari di satu tangan?", "options": ["Satu", "Dua", "Lima", "Sepuluh"], "answer": 2},
            {"question": "Apa warna langit di siang hari?", "options": ["Merah", "Biru", "Kuning", "Hijau"], "answer": 1},
            {"question": "Hewan apa yang suka makan pisang?", "options": ["Kucing", "Anjing", "Monyet", "Ikan"], "answer": 2},
            {"question": "Apa bunyi suara kucing?", "options": ["Guk guk", "Meong", "Moo", "Kwek kwek"], "answer": 1},
            {"question": "Buah apa yang berwarna merah?", "options": ["Pisang", "Jeruk", "Apel", "Salak"], "answer": 2},
            {"question": "Kendaraan yang punya roda dua adalah?", "options": ["Mobil", "Sepeda", "Bus", "Kereta"], "answer": 1},
        ],
        "SD": [
            {"question": "Berapa hasil dari 2 + 3?", "options": ["4", "5", "6", "7"], "answer": 1},
            {"question": "Ibukota Indonesia adalah?", "options": ["Bandung", "Jakarta", "Surabaya", "Medan"], "answer": 1},
            {"question": "Siapa presiden pertama Indonesia?", "options": ["B.J. Habibie", "Soeharto", "Soekarno", "Gus Dur"], "answer": 2},
            {"question": "Pancasila memiliki berapa sila?", "options": ["3", "4", "5", "6"], "answer": 2},
            {"question": "Hewan yang bernapas dengan insang adalah?", "options": ["Kucing", "Burung", "Ikan", "Kancil"], "answer": 2},
            {"question": "Berapa jumlah kaki pada laba-laba?", "options": ["4", "6", "8", "10"], "answer": 2},
        ],
        "SMP": [
            {"question": "Akar dari 81 adalah?", "options": ["7", "8", "9", "10"], "answer": 2},
            {"question": "H2O adalah rumus kimia dari?", "options": ["Garam", "Gula", "Air", "Udara"], "answer": 2},
            {"question": "Planet ketiga dalam tata surya adalah?", "options": ["Merkurius", "Venus", "Bumi", "Mars"], "answer": 2},
            {"question": "Benua terkecil di dunia adalah?", "options": ["Asia", "Eropa", "Australia", "Afrika"], "answer": 2},
            {"question": "Siapa penemu lampu pijar?", "options": ["Albert Einstein", "Thomas Edison", "Isaac Newton", "Graham Bell"], "answer": 1},
            {"question": "Negara manakah yang dijuluki Negeri Matahari Terbit?", "options": ["Cina", "Korea", "Jepang", "Thailand"], "answer": 2},
        ],
        "SMA": [
            {"question": "Kecepatan cahaya (km/s)?", "options": ["300.000", "150.000", "600.000", "Instan"], "answer": 0},
            {"question": "1 kg besi vs 1 kg kapas?", "options": ["Besi", "Kapas", "Sama", "Beda massa"], "answer": 2},
            {"question": "Siapa penulis novel 'Laskar Pelangi'?", "options": ["Tere Liye", "Andrea Hirata", "Habiburrahman", "Dee Lestari"], "answer": 1},
            {"question": "Logaritma 100 dengan basis 10 adalah?", "options": ["1", "2", "10", "100"], "answer": 1},
            {"question": "Sila keempat Pancasila dilambangkan dengan?", "options": ["Bintang", "Pohon Beringin", "Kepala Banteng", "Padi dan Kapas"], "answer": 2},
            {"question": "Siapakah bapak Proklamator Indonesia?", "options": ["Soeharto & Adam Malik", "Soekarno & Moh. Hatta", "Habibie & Gus Dur", "Ki Hajar Dewantara"], "answer": 1},
        ]
    }

    def on_enter(self):
        level = self.selected_level if self.selected_level in self.questions_data else "SMA"
        self.questions = list(self.questions_data[level])
        random.shuffle(self.questions)
        self.score = 0
        self.index_soal = 0
        self.lives = 3
        self.quiz_start_time = time.time()
        self.tampilkan_soal()

    def tampilkan_soal(self):
        self.clear_widgets()
        if self.timer_event: Clock.unschedule(self.timer_event)

        if self.index_soal < len(self.questions) and self.lives > 0:
            q_data = self.questions[self.index_soal]
            self.remaining_time = self.total_time
            
            layout = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
            
            # Header Info
            header = MDBoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
            self.score_lbl = MDLabel(text=f"Score: {self.score}", bold=True, theme_text_color="Primary")
            self.lives_lbl = MDLabel(text=f"{'❤️' * self.lives}", halign="right", theme_text_color="Error")
            header.add_widget(self.score_lbl)
            header.add_widget(self.lives_lbl)
            layout.add_widget(header)

            # Timer Bar (INTERAKTIF: Akan berkedip jika < 3s)
            self.timer_bar = MDProgressBar(value=100, max=100, size_hint_y=None, height=dp(6))
            layout.add_widget(self.timer_bar)

            layout.add_widget(MDBoxLayout(size_hint_y=0.1))

            # Soal Card
            self.q_card = MDCard(
                orientation='vertical', padding=dp(20), radius=[dp(20),], elevation=3,
                size_hint=(1, None), height=dp(150), pos_hint={"center_x": 0.5}
            )
            self.q_card.add_widget(MDLabel(
                text=q_data["question"], halign="center", font_style="H6", bold=True
            ))
            layout.add_widget(self.q_card)

            layout.add_widget(MDBoxLayout(size_hint_y=0.1))

            # Options
            self.btns = []
            for i, opt in enumerate(q_data["options"]):
                b = MDFillRoundFlatButton(
                    text=opt, size_hint=(1, None), height=dp(50),
                    on_release=lambda x, idx=i: self.cek_jawaban(idx)
                )
                layout.add_widget(b)
                self.btns.append(b)

            layout.add_widget(MDBoxLayout())
            self.add_widget(layout)
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.05)
            
            # Animasi Masuk
            self.q_card.opacity = 0
            anim = Animation(opacity=1, duration=0.5)
            anim.start(self.q_card)
        else:
            self.selesai_kuis()

    def update_timer(self, dt):
        self.remaining_time -= dt
        perc = (self.remaining_time / self.total_time) * 100
        self.timer_bar.value = perc
        
        if self.remaining_time < 3:
            self.timer_bar.color = [1, 0, 0, 1]
            # Efek getar sederhana pada bar
            self.timer_bar.height = dp(8) if int(self.remaining_time * 10) % 2 == 0 else dp(6)
        
        if self.remaining_time <= 0:
            self.cek_jawaban(-1)

    def cek_jawaban(self, choice):
        if self.timer_event: Clock.unschedule(self.timer_event)
        correct = self.questions[self.index_soal]["answer"]
        
        for b in self.btns: b.disabled = True
        
        if choice == correct:
            self.score += 10
            self.btns[choice].md_bg_color = [0.1, 0.8, 0.1, 1]
            self.score_lbl.text = f"Score: {self.score} +10!"
        else:
            self.lives -= 1
            if choice != -1:
                self.btns[choice].md_bg_color = [0.8, 0.1, 0.1, 1]
            self.btns[correct].md_bg_color = [0.1, 0.8, 0.1, 1]
            # Shake animation on card for wrong answer
            anim = Animation(pos_hint={"center_x": 0.52}, duration=0.05) + \
                   Animation(pos_hint={"center_x": 0.48}, duration=0.05) + \
                   Animation(pos_hint={"center_x": 0.5}, duration=0.05)
            anim.start(self.q_card)

        Clock.schedule_once(self.next, 1.5)

    def next(self, dt):
        self.index_soal += 1
        self.tampilkan_soal()

    def selesai_kuis(self):
        self.manager.get_screen('layar_hasil').skor = self.score
        self.manager.get_screen('layar_hasil').lives = self.lives
        self.manager.current = 'layar_hasil'

class LayarHasil(MDScreen):
    skor = 0
    lives = 0
    def on_enter(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        title = "GAME OVER" if self.lives <= 0 else "LUAR BIASA!"
        layout.add_widget(MDLabel(text=title, halign="center", font_style="H4", bold=True, theme_text_color="Primary"))
        
        res_card = MDCard(radius=[dp(25),], padding=dp(20), orientation='vertical', elevation=4)
        res_card.add_widget(MDLabel(text=f"SKOR AKHIR", halign="center", font_style="Overline"))
        res_card.add_widget(MDLabel(text=f"{self.skor}", halign="center", font_style="H2", bold=True, theme_text_color="Primary"))
        res_card.add_widget(MDLabel(text=f"Sisa Nyawa: {'❤️' * self.lives}", halign="center"))
        layout.add_widget(res_card)
        
        layout.add_widget(MDFillRoundFlatIconButton(
            icon="replay", text="MAIN LAGI", pos_hint={"center_x": 0.5}, size_hint=(0.8, None),
            on_release=lambda x: setattr(self.manager, 'current', 'layar_beranda')
        ))
        
        layout.add_widget(MDRaisedButton(
            text="MENU UTAMA", pos_hint={"center_x": 0.5}, size_hint=(0.8, None),
            on_release=lambda x: setattr(self.manager, 'current', 'layar_home'),
            md_bg_color=[0.5, 0.5, 0.5, 1]
        ))
        
        layout.add_widget(MDBoxLayout())
        self.add_widget(layout)

class GameApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        sm = MDScreenManager()
        sm.add_widget(LayarHome(name='layar_home'))
        sm.add_widget(Beranda(name='layar_beranda'))
        sm.add_widget(LayarKuis(name='layar_kuis'))
        sm.add_widget(LayarHasil(name='layar_hasil'))
        return sm

if __name__ == "__main__":
    GameApp().run()
