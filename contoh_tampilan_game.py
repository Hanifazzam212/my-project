from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar # Import MDToolbar
from kivy.metrics import dp
import random
import time

class Beranda(MDScreen):
    """Layar pertama saat aplikasi dibuka"""
    def __init__(self, **kw):
        super().__init__(**kw)
        
        # Main layout untuk seluruh layar
        main_layout = MDBoxLayout(orientation='vertical')

        # MDToolbar di bagian atas untuk tombol 'undo' dan judul layar
        toolbar = MDToolbar(title="Pilih Level", title_align="center") # Judul untuk layar Beranda, dengan teks terpusat
        # Tombol 'undo' di pojok kiri atas (menggunakan ikon panah kiri untuk navigasi)
        toolbar.left_action_items = [['arrow-left', lambda x: self.go_back_action()]]
        main_layout.add_widget(toolbar)

        # Konten yang sudah ada (judul game dan tombol level)
        content_layout = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(40), pos_hint={"center_y": 0.5})
        
        judul = MDLabel(
            text="🧠 GAME KECERDASAN 🧠", 
            halign="center", 
            font_style="H4",
            theme_text_color="Primary"
        )
        content_layout.add_widget(judul)
        
        # Tombol untuk pilihan level
        levels = ["TK", "SD", "SMP", "SMA"]
        for level_text in levels:
            btn_level = MDRaisedButton(
                text=f"LEVEL {level_text}",
                pos_hint={"center_x": 0.5},
                size_hint=(0.8, None),
                on_release=lambda instance, level=level_text: self.start_level_game(level)
            )
            content_layout.add_widget(btn_level)

        main_layout.add_widget(content_layout) # Tambahkan content_layout ke main_layout
        self.add_widget(main_layout) # Tambahkan main_layout ke layar

    def go_back_action(self):
        # Karena Beranda adalah layar awal, tombol 'back' di sini tidak memiliki tujuan layar sebelumnya.
        # Ini bisa digunakan untuk keluar aplikasi atau hanya sebagai placeholder.
        print("Tombol Kembali/Undo ditekan di layar Beranda (tidak ada layar sebelumnya untuk kembali).")
        # Jika Anda ingin tombol ini untuk keluar aplikasi, Anda bisa uncomment baris di bawah:
        # from kivymd.app import MDApp
        # MDApp.get_running_app().stop()

    def start_level_game(self, level, *args):
        self.manager.get_screen('layar_kuis').selected_level = level
        self.manager.current = 'layar_kuis'

class LayarKuis(MDScreen):
    """Layar tempat pertanyaan muncul"""
    selected_level = None # Menambahkan atribut untuk level yang dipilih

    # Definisikan daftar soal untuk setiap level
    questions_data = {
        "TK": [
            {"question": "Berapa banyak jari di satu tangan?", "options": ["Satu", "Dua", "Lima", "Sepuluh"], "answer": 2},
            {"question": "Apa warna langit di siang hari?", "options": ["Merah", "Biru", "Kuning", "Hijau"], "answer": 1},
            {"question": "Hewan apa yang suka makan pisang?", "options": ["Kucing", "Anjing", "Monyet", "Ikan"], "answer": 2},
        ],
        "SD": [
            {"question": "Berapa hasil dari 2 + 3?", "options": ["4", "5", "6", "7"], "answer": 1},
            {"question": "Negara kita disebut apa?", "options": ["Malaysia", "Singapura", "Indonesia", "Thailand"], "answer": 2},
            {"question": "Apa nama benda yang bisa kita gunakan untuk menulis di buku?", "options": ["Sendok", "Pensil", "Gunting", "Sisir"], "answer": 1},
        ],
        "SMP": [
            {"question": "Berapa akar kuadrat dari 81?", "options": ["7", "8", "9", "10"], "answer": 2},
            {"question": "Apa ibukota negara Indonesia?", "options": ["Bandung", "Surabaya", "Yogyakarta", "Jakarta"], "answer": 3},
            {"question": "Jika sebuah segitiga memiliki tiga sisi yang sama panjang, itu disebut segitiga apa?", "options": ["Siku-siku", "Sama kaki", "Sama sisi", "Sembarang"], "answer": 2},
        ],
        "SMA": [
            {"question": "Jika 5 kucing menangkap 5 tikus dalam 5 menit, berapa lama 100 kucing menangkap 100 tikus?", "options": ["100 menit", "20 menit", "5 menit", "1 menit"], "answer": 2},
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
        self.score = 0
        self.index_soal = 0
        self.lives = 3 # Inisialisasi nyawa
        self.tampilkan_soal()

    def tampilkan_soal(self):
        self.clear_widgets() # Bersihkan layar dari soal sebelumnya
        
        if self.index_soal < len(self.questions) and self.lives > 0: # Cek nyawa juga
            q_data = self.questions[self.index_soal]
            self.start_time = time.time() # Mulai hitung waktu
            
            layout = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20), pos_hint={"center_y": 0.5})
            
            top_info_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
            progress = MDLabel(text=f"Soal {self.index_soal + 1}/{len(self.questions)}", halign="left", theme_text_color="Hint")
            lives_label = MDLabel(text=f"Nyawa: {self.lives} ❤️", halign="right", theme_text_color="Primary")
            top_info_layout.add_widget(progress)
            top_info_layout.add_widget(lives_label)

            pertanyaan = MDLabel(
                text=q_data["question"],
                halign="center",
                font_style="H6"
            )
            
            layout.add_widget(top_info_layout) # Tambahkan layout info atas
            layout.add_widget(pertanyaan)
            
            # Buat tombol untuk setiap opsi pilihan ganda
            for i, option in enumerate(q_data['options']):
                btn = MDRaisedButton(
                    text=option,
                    pos_hint={"center_x": 0.5},
                    size_hint=(0.9, None),
                    on_release=lambda instance, idx=i: self.cek_jawaban(idx)
                )
                layout.add_widget(btn)
            
            self.add_widget(layout)
        else:
            # Jika soal habis, kirim skor ke layar hasil dengan status 'completed'
            self.manager.get_screen('layar_hasil').skor_akhir = self.score
            self.manager.get_screen('layar_hasil').game_status = 'completed'
            self.manager.current = 'layar_hasil'

    def cek_jawaban(self, user_choice_index):
        q_data = self.questions[self.index_soal]
        elapsed = time.time() - self.start_time
        
        # Logika skor dari kode Anda
        if user_choice_index == q_data['answer']:
            if elapsed <= 10:
                self.score += 10
            elif elapsed <= 20:
                self.score += 8
            else:
                self.score += 5
        else:
            self.lives -= 1 # Kurangi nyawa jika jawaban salah
            if self.lives == 0:
                # Jika nyawa habis, langsung ke layar hasil dengan status 'game_over'
                self.manager.get_screen('layar_hasil').skor_akhir = self.score
                self.manager.get_screen('layar_hasil').game_status = 'game_over'
                self.manager.current = 'layar_hasil'
                return # Hentikan eksekusi lebih lanjut
                
        self.index_soal += 1
        self.tampilkan_soal()

class LayarHasil(MDScreen):
    """Layar untuk menampilkan nilai akhir"""
    skor_akhir = 0
    game_status = 'completed' # Menambahkan status permainan

    def on_enter(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', spacing=dp(20), padding=dp(40), pos_hint={"center_y": 0.5})
        
        if self.game_status == 'game_over':
            game_over_label = MDLabel(
                text="GAME OVER!",
                halign="center",
                font_style="H2",
                theme_text_color="Error" # Warna merah untuk Game Over
            )
            layout.add_widget(game_over_label)

        hasil = MDLabel(
            text=f"SKOR AKHIR: {self.skor_akhir}",
            halign="center",
            font_style="H3",
            theme_text_color="Primary"
        )
        
        btn_ulang = MDRaisedButton(
            text="MAIN LAGI",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, 'current', 'layar_beranda')
        )
        
        layout.add_widget(hasil)
        layout.add_widget(btn_ulang)
        self.add_widget(layout)

class GameApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange" # Warna tema aplikasi
        
        sm = MDScreenManager()
        sm.add_widget(Beranda(name='layar_beranda'))
        sm.add_widget(LayarKuis(name='layar_kuis'))
        sm.add_widget(LayarHasil(name='layar_hasil'))
        
        return sm

if __name__ == "__main__":
    GameApp().run()
