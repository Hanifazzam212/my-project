from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import random
import time

# Simulasi ukuran layar mobile (Portrait)
Window.size = (360, 640)

class LayarHome(MDScreen):
    """Layar pembuka aplikasi"""
    def __init__(self, **kw):
        super().__init__(**kw)
        
        # Gunakan FloatLayout sebagai root agar bisa memposisikan tombol di pojok
        self.root_layout = MDFloatLayout()

        # Layout utama untuk konten tengah
        content_layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(5))
        content_layout.add_widget(MDBoxLayout(size_hint_y=0.25)) # Top spacer

        content_layout.add_widget(MDLabel(
            text="KUIS PINTAR",
            halign="center",
            font_style="H4", # Ukuran lebih mobile-friendly
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))

        content_layout.add_widget(MDLabel(
            text="Uji wawasan dan kecepatan berpikirmu!",
            halign="center",
            font_style="Body2", # Font lebih kecil untuk subtitle
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        ))

        content_layout.add_widget(MDBoxLayout(size_hint_y=0.3)) # Middle spacer

        btn_mulai = MDRaisedButton(
            text="MULAI BERMAIN",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height=dp(56),
            elevation=4,
            on_release=lambda x: setattr(self.manager, 'current', 'layar_beranda')
        )
        content_layout.add_widget(btn_mulai)
        content_layout.add_widget(MDBoxLayout(size_hint_y=0.2)) # Bottom spacer
 
        self.root_layout.add_widget(content_layout)

        # Tombol Mode Terang/Gelap di pojok kanan atas
        self.theme_btn = MDIconButton(
            icon="weather-night",
            pos_hint={"top": 0.98, "right": 0.98},
            on_release=self.toggle_theme
        )
        self.root_layout.add_widget(self.theme_btn)
        
        self.add_widget(self.root_layout)

    def toggle_theme(self, instance):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
            self.theme_btn.icon = "weather-sunny"
            bg_color = [0.1, 0.1, 0.1, 1]
        else:
            app.theme_cls.theme_style = "Light"
            self.theme_btn.icon = "weather-night"
            bg_color = [0.98, 0.98, 0.98, 1]
        
        # Terapkan warna latar belakang ke SEMUA layar
        for screen in self.manager.screens:
            screen.md_bg_color = bg_color

class Beranda(MDScreen):
    """Layar untuk memilih level permainan"""
    def __init__(self, **kw):
        super().__init__(**kw)
        
        # Main layout untuk seluruh layar
        main_layout = MDBoxLayout(orientation='vertical')

        # MDToolbar di bagian atas
        toolbar = MDTopAppBar(title="Pilih Jenjang")
        toolbar.left_action_items = [['arrow-left', lambda x: self.go_back_action()]]
        main_layout.add_widget(toolbar)

        # Konten
        content_layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(25))
        
        content_layout.add_widget(MDLabel(
            text="SIAP UNTUK TANTANGAN?", 
            halign="center", 
            font_style="H6",
            theme_text_color="Primary",
            bold=True
        ))
        
        content_layout.add_widget(MDLabel(
            text="Pilih tingkat kesulitan",
            halign="center",
            font_style="Caption",
            theme_text_color="Secondary"
        ))
        
        content_layout.add_widget(MDBoxLayout(size_hint_y=0.1)) # Spacer

        # Tombol untuk pilihan level dengan ikon
        levels = [
            ("TK", "baby-face-outline"),
            ("SD", "school"),
            ("SMP", "book-open-variant"),
            ("SMA", "brain")
        ]
        
        for level_text, icon_name in levels:
            btn_level = MDRaisedButton(
                text=f"   LEVEL {level_text}",
                pos_hint={"center_x": 0.5},
                size_hint=(0.9, None),
                height=dp(50),
                on_release=lambda instance, level=level_text: self.start_level_game(level)
            )
            # Adding icon manually to MDRaisedButton text isn't ideal, 
            # but KivyMD's MDRectangleFlatIconButton is another option.
            # Let's use a simpler approach for now or switch to a better button.
            content_layout.add_widget(btn_level)

        content_layout.add_widget(MDBoxLayout(size_hint_y=0.2)) # Bottom spacer

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def go_back_action(self):
        self.manager.current = 'layar_home'

    def start_level_game(self, level, *args):
        self.manager.get_screen('layar_kuis').selected_level = level
        self.manager.current = 'layar_kuis'

class LayarKuis(MDScreen):
    """Layar tempat pertanyaan muncul"""
    selected_level = None # Menambahkan atribut untuk level yang dipilih
    timer_event = None # Melacak event Clock
    total_time = 10 # Waktu per soal dalam detik

    # Definisikan daftar soal untuk setiap level
    questions_data = {
        "TK": [
            {"question": "Berapa banyak jari di satu tangan?", "options": ["Satu", "Dua", "Lima", "Sepuluh"], "answer": 2},
            {"question": "Apa warna langit di siang hari?", "options": ["Merah", "Biru", "Kuning", "Hijau"], "answer": 1},
            {"question": "Hewan apa yang suka makan pisang?", "options": ["Kucing", "Anjing", "Monyet", "Ikan"], "answer": 2},
            {"question": "Apa bunyi kucing?", "options": ["Guk", "Meong", "Moo", "Kwek"], "answer": 1},
            {"question": "Bagian tubuh apa yang digunakan untuk melihat?", "options": ["Hidung", "Telinga", "Mata", "Mulut"], "answer": 2},
            {"question": "Hewan apa yang terbang di langit?", "options": ["Ikan", "Burung", "Kuda", "Ular"], "answer": 1},
            {"question": "Angka setelah dua adalah?", "options": ["Satu", "Tiga", "Empat", "Lima"], "answer": 1},
            {"question": "Apa warna rumput?", "options": ["Biru", "Merah", "Hijau", "Kuning"], "answer": 2},
        ],
        "SD": [
            {"question": "Berapa hasil dari 2 + 3?", "options": ["4", "5", "6", "7"], "answer": 1},
            {"question": "Jika kamu punya 5 apel dan kamu makan 2, berapa apel yang tersisa?", "options": ["2", "3", "4", "5"], "answer": 1},
            {"question": "Berapa jumlah roda pada sepeda?", "options": ["1", "2", "3", "4"], "answer": 1},
            {"question": "Pahlawan super yang bisa terbang dan memiliki jubah merah adalah?", "options": ["Batman", "Spiderman", "Superman", "Iron Man"], "answer": 2},
            {"question": "Negara kita disebut apa?", "options": ["Malaysia", "Singapura", "Indonesia", "Thailand"], "answer": 2},
            {"question": "Apa nama benda yang bisa kita gunakan untuk menulis di buku?", "options": ["Sendok", "Pensil", "Gunting", "Sisir"], "answer": 1},
            {"question": "Apa hewan tercepat di darat?", "options": ["Singa", "Harimau", "Cheetah", "Gajah"], "answer": 2},
            {"question": "Berapa jumlah hari dalam seminggu?", "options": ["5", "6", "7", "8"], "answer": 2},
            {"question": "Planet terbesar di tata surya kita adalah?", "options": ["Bumi", "Mars", "Jupiter", "Saturnus"], "answer": 2},
            {"question": "Berapa sisi yang dimiliki sebuah persegi?", "options": ["2", "3", "4", "5"], "answer": 2},
            {"question": "Apa warna bendera Indonesia?", "options": ["Merah dan Putih", "Biru dan Putih", "Hijau dan Kuning", "Hitam dan Merah"], "answer": 0},
        ],
        "SMP": [
            {"question": "Berapa akar kuadrat dari 81?", "options": ["7", "8", "9", "10"], "answer": 2},
            {"question": "Siapa penemu hukum gravitasi?", "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Nikola Tesla"], "answer": 1},
            {"question": "Organ tubuh yang berfungsi memompa darah ke seluruh tubuh adalah?", "options": ["Paru-paru", "Otak", "Jantung", "Hati"], "answer": 2},
            {"question": "Bagian tumbuhan yang bertugas menyerap air dan nutrisi dari tanah adalah?", "options": ["Daun", "Batang", "Bunga", "Akar"], "answer": 3},
            {"question": "Apa ibukota negara Indonesia?", "options": ["Bandung", "Surabaya", "Yogyakarta", "Jakarta"], "answer": 3},
            {"question": "Jika sebuah segitiga memiliki tiga sisi yang sama panjang, itu disebut segitiga apa?", "options": ["Siku-siku", "Sama kaki", "Sama sisi", "Sembarang"], "answer": 2},
            {"question": "Senyawa kimia dengan rumus H2O dikenal sebagai apa?", "options": ["Garam", "Gula", "Air", "Udara"], "answer": 2},
            {"question": "Siapa penemu lampu pijar?", "options": ["Isaac Newton", "Albert Einstein", "Thomas Edison", "Nikola Tesla"], "answer": 2},
            {"question": "Berapa jumlah benua di dunia?", "options": ["5", "6", "7", "8"], "answer": 2},
            {"question": "Gas yang paling melimpah di atmosfer Bumi adalah?", "options": ["Oksigen", "Hidrogen", "Nitrogen", "Karbon Dioksida"], "answer": 2},
            {"question": "Apakah satuan terkecil dari materi?", "options": ["Molekul", "Sel", "Atom", "Elektron"], "answer": 2},
        ],
        "SMA": [
            {"question": "Jika 5 kucing menangkap 5 tikus dalam 5 menit, berapa lama 100 kucing menangkap 100 tikus?", "options": ["100 menit", "20 menit", "5 menit", "1 menit"], "answer": 2},
            {"question": "Berapa kecepatan cahaya dalam ruang hampa?", "options": ["300.000 km/s", "150.000 km/s", "600.000 km/s", "Tidak terbatas"], "answer": 0},
            {"question": "Siapa pengarang novel 'Laskar Pelangi'?", "options": ["Tere Liye", "Andrea Hirata", "Pramoedya Ananta Toer", "Chairil Anwar"], "answer": 1},
            {"question": "Berapa jumlah kromosom normal pada manusia?", "options": ["23", "46", "48", "24"], "answer": 1},
            {"question": "Sebuah rumah menghadap selatan. Seekor beruang datang ke rumah tersebut. Apa warna beruang itu?", "options": ["Putih", "Coklat", "Hitam", "Kuning"], "answer": 0},
            {"question": "Ayah punya 3 anak: Budi, Budi, dan Budi. Berapa nama anak perempuannya?", "options": ["Budi", "Tidak ada", "Budiarti", "Perempuan tidak disebutkan"], "answer": 1},
            {"question": "Mana yang lebih berat: 1 kg besi atau 1 kg kapas?", "options": ["Besi", "Kapas", "Sama berat", "Tidak bisa ditimbang"], "answer": 2},
            {"question": "Jika ada 12 ikan di akuarium dan 11 mati, berapa yang tersisa?", "options": ["1", "0", "11", "12"], "answer": 3} # Jawaban saya koreksi ke 12 karena bangkai ikan tetap di sana hehe
        ]
    }

    def on_enter(self):
        # Memuat soal berdasarkan level yang dipilih
        if self.selected_level and self.selected_level in self.questions_data:
            self.questions = list(self.questions_data[self.selected_level]) # Menggunakan salinan daftar soal
        else:
            # Fallback jika tidak ada level yang dipilih atau level tidak valid
            self.questions = list(self.questions_data["SMA"])
            
        random.shuffle(self.questions)
        self.max_possible_score = len(self.questions) * 10 # Menghitung skor maksimum yang mungkin
        self.score = 0
        self.index_soal = 0
        self.lives = 3 # Inisialisasi nyawa
        self.timer_event = None
        self.quiz_start_time = time.time() # Mulai waktu kuis keseluruhan
        self.tampilkan_soal()

    def on_leave(self):
        """Hentikan timer saat meninggalkan layar kuis"""
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None

    def tampilkan_soal(self):
        self.clear_widgets() # Bersihkan layar dari soal sebelumnya

        # Hentikan timer sebelumnya jika ada
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
        
        if self.index_soal < len(self.questions) and self.lives > 0: # Cek nyawa juga
            q_data = self.questions[self.index_soal]
            self.start_time = time.time() # Mulai hitung waktu
            self.remaining_time = self.total_time
            
            # Layout utama (tanpa center_y agar bisa diatur manual dengan spacer)
            layout = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
            
            # 1. Bagian Atas: Waktu & Info
            self.timer_bar = MDProgressBar(
                value=100,
                max=100,
                type="determinate",
                size_hint_y=None,
                height=dp(4),
                color=self.theme_cls.primary_color
            )
            layout.add_widget(self.timer_bar)

            top_info_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
            progress = MDLabel(text=f"Soal {self.index_soal + 1}/{len(self.questions)}", halign="left", theme_text_color="Hint", font_style="Caption")
            lives_label = MDLabel(text=f"Nyawa: {self.lives} ❤️", halign="right", theme_text_color="Error", font_style="Caption")
            top_info_layout.add_widget(progress)
            top_info_layout.add_widget(lives_label)
            layout.add_widget(top_info_layout)

            # Spacer untuk mendorong soal ke tengah
            layout.add_widget(MDBoxLayout(size_hint_y=0.4))

            # 2. Bagian Tengah: Soal
            card_pertanyaan = MDCard(
                orientation='vertical',
                padding=dp(15),
                size_hint=(1, None),
                height=dp(120),
                elevation=2,
                radius=[dp(12),],
                ripple_behavior=True
            )
            pertanyaan = MDLabel(
                text=q_data["question"],
                halign="center",
                font_style="Subtitle1",
                theme_text_color="Primary"
            )
            card_pertanyaan.add_widget(pertanyaan)
            layout.add_widget(card_pertanyaan)
            
            # Spacer untuk mendorong pilihan jawaban ke bawah
            layout.add_widget(MDBoxLayout(size_hint_y=0.6))

            # 3. Bagian Bawah: Pilihan Jawaban
            self.option_buttons = []
            options_layout = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
            for i, option in enumerate(q_data['options']):
                btn = MDRaisedButton(
                    text=option,
                    pos_hint={"center_x": 0.5},
                    size_hint=(1, None), # Full width untuk mobile
                    on_release=lambda instance, idx=i: self.cek_jawaban(idx)
                )
                options_layout.add_widget(btn)
                self.option_buttons.append(btn)
            layout.add_widget(options_layout)
            
            # Padding bawah tambahan
            layout.add_widget(MDBoxLayout(size_hint_y=0.1))

            self.add_widget(layout)
            
            # Mulai penghitungan mundur
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)
        else:
            self.selesai_kuis()

    def cek_jawaban(self, user_choice_index):
        # Hentikan timer segera setelah ada jawaban
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
            
        q_data = self.questions[self.index_soal]
        correct_answer = q_data['answer']
        
        # Matikan semua tombol agar tidak bisa diklik lagi
        for btn in self.option_buttons:
            btn.disabled = True

        if user_choice_index == correct_answer:
            self.score += 10
            # Beri warna hijau pada tombol yang benar
            self.option_buttons[user_choice_index].md_bg_color = [0.1, 0.7, 0.1, 1] 
        else:
            self.lives -= 1
            # Beri warna merah pada tombol yang salah
            self.option_buttons[user_choice_index].md_bg_color = [0.8, 0.1, 0.1, 1]
            # Tunjukkan jawaban yang benar dengan warna hijau
            self.option_buttons[correct_answer].md_bg_color = [0.1, 0.7, 0.1, 1]
                
        # Beri jeda 1 detik sebelum lanjut ke soal berikutnya
        Clock.schedule_once(self.next_question, 1.2)

    def next_question(self, dt):
        if self.lives <= 0:
            self.selesai_kuis(game_over=True)
        else:
            self.index_soal += 1
            self.tampilkan_soal()

    def selesai_kuis(self, game_over=False):
        total_time = int(time.time() - self.quiz_start_time)
        self.manager.get_screen('layar_hasil').skor_akhir = self.score
        self.manager.get_screen('layar_hasil').game_status = 'game_over' if game_over else 'completed'
        self.manager.get_screen('layar_hasil').max_possible_score = self.max_possible_score
        self.manager.get_screen('layar_hasil').sisa_nyawa = self.lives
        self.manager.get_screen('layar_hasil').waktu_total = total_time
        self.manager.current = 'layar_loading'

    def update_timer(self, dt):
        """Fungsi yang dipanggil setiap 0.1 detik untuk memperbarui progress bar"""
        self.remaining_time -= dt
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.timer_bar.value = 0
            Clock.unschedule(self.timer_event)
            self.timer_event = None
            
            # Waktu habis = kurangi nyawa
            self.lives -= 1
            if self.lives <= 0:
                self.selesai_kuis(game_over=True)
            else:
                self.index_soal += 1
                self.tampilkan_soal()
        else:
            # Perbarui nilai progress bar (100 -> 0)
            self.timer_bar.value = (self.remaining_time / self.total_time) * 100

class LayarLoading(MDScreen):
    """Layar loading transisi sebelum hasil"""
    def on_enter(self):
        self.clear_widgets()
        
        layout = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(40), pos_hint={"center_y": 0.5})
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        # Spinner loading
        from kivymd.uix.spinner import MDSpinner
        spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            pos_hint={"center_x": 0.5},
            active=True,
            line_width=dp(4)
        )
        layout.add_widget(spinner)
        
        layout.add_widget(MDLabel(
            text="Sedang memproses jawaban...",
            halign="center",
            font_style="H6",
            theme_text_color="Secondary"
        ))
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.4))
        
        self.add_widget(layout)
        
        # Simulasi proses (setTimeout di JS = Clock.schedule_once di Kivy)
        Clock.schedule_once(self.go_to_result, 2.0)

    def go_to_result(self, dt):
        self.manager.current = 'layar_hasil'

class LayarHasil(MDScreen):
    """Layar untuk menampilkan nilai akhir"""
    skor_akhir = 0
    game_status = 'completed'
    max_possible_score = 0
    sisa_nyawa = 0
    waktu_total = 0

    def on_enter(self):
        self.clear_widgets()
        
        layout = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15), pos_hint={"center_y": 0.5})
        
        # Header Info
        header_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(80), spacing=dp(2))
        
        if self.game_status == 'game_over':
            msg_text = "GAME OVER!"
            icon_color = "Error"
        elif self.skor_akhir == self.max_possible_score and self.max_possible_score > 0:
            msg_text = "SEMPURNA!"
            icon_color = "Primary"
        else:
            msg_text = "SELESAI!"
            icon_color = "Secondary"

        header_box.add_widget(MDLabel(
            text=msg_text,
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color=icon_color
        ))
        header_box.add_widget(MDLabel(
            text="Ringkasan hasil kuis",
            halign="center",
            font_style="Caption",
            theme_text_color="Secondary"
        ))
        layout.add_widget(header_box)

        # 3 Kotak Berjejer (Horizontal Layout)
        stats_layout = MDBoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=None, height=dp(110))
        
        # Kotak Kiri: Sisa Nyawa (Merah)
        card_lives = self.create_stat_card("NYAWA", f"{self.sisa_nyawa}", "heart", "Error", [0.9, 0.1, 0.1, 1])
        
        # Kotak Tengah: Poin (Kuning)
        card_score = self.create_stat_card("POIN", f"{self.skor_akhir}", "star", "Primary", [1, 0.8, 0, 1])
        
        # Kotak Kanan: Waktu (Hijau)
        card_time = self.create_stat_card("WAKTU", f"{self.waktu_total}s", "clock", "Secondary", [0.1, 0.7, 0.1, 1])
        
        stats_layout.add_widget(card_lives)
        stats_layout.add_widget(card_score)
        stats_layout.add_widget(card_time)
        
        layout.add_widget(stats_layout)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.1))
        
        btn_ulang = MDRaisedButton(
            text="MAIN LAGI",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height=dp(56),
            on_release=lambda x: setattr(self.manager, 'current', 'layar_beranda')
        )
        layout.add_widget(btn_ulang)

        btn_home = MDRaisedButton(
            text="MENU UTAMA",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height=dp(56),
            md_bg_color=[0.5, 0.5, 0.5, 1],
            on_release=lambda x: setattr(self.manager, 'current', 'layar_home')
        )
        layout.add_widget(btn_home)
        
        self.add_widget(layout)

    def create_stat_card(self, title, value, icon, color, border_color):
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            elevation=2,
            radius=[dp(15),],
            spacing=dp(5),
            line_color=border_color,
            line_width=dp(2)
        )
        card.add_widget(MDIcon(
            icon=icon,
            halign="center",
            font_size=dp(30),
            theme_text_color=color,
            pos_hint={"center_x": 0.5}
        ))
        card.add_widget(MDLabel(
            text=value,
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Primary"
        ))
        card.add_widget(MDLabel(
            text=title,
            halign="center",
            font_style="Caption",
            theme_text_color="Secondary"
        ))
        return card

class GameApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green" # Warna tema aplikasi
        
        sm = MDScreenManager()
        sm.add_widget(LayarHome(name='layar_home'))
        sm.add_widget(Beranda(name='layar_beranda'))
        sm.add_widget(LayarKuis(name='layar_kuis'))
        sm.add_widget(LayarLoading(name='layar_loading'))
        sm.add_widget(LayarHasil(name='layar_hasil'))
        
        # Set the initial screen
        sm.current = 'layar_home'
        
        # Inisialisasi warna background awal (Light Mode)
        for screen in sm.screens:
            screen.md_bg_color = [0.98, 0.98, 0.98, 1]
        
        return sm

if __name__ == "__main__":
    GameApp().run()
print('Memuat antarmuka grafis (GUI) game kecerdasan...')
