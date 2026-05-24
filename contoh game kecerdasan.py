import random
import time

class GameKecerdasan:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.questions = []
        self.load_questions()
    
    def load_questions(self):
        """Memuat semua soal ke dalam list"""
        self.questions = [
            {
                "question": "Jika 5 kucing menangkap 5 tikus dalam 5 menit, berapa lama 100 kucing menangkap 100 tikus?",
                "options": ["100 menit", "20 menit", "5 menit", "1 menit"],
                "answer": 2  # 5 menit (setiap kucing menangkap 1 tikus dalam 5 menit)
            },
            {
                "question": "Sebuah rumah menghadap selatan. Seekor beruang datang ke rumah tersebut. Apa warna beruang itu?",
                "options": ["Putih", "Coklat", "Hitam", "Kuning"],
                "answer": 0  # Putih (rumah menghadap selatan hanya ada di kutub utara)
            },
            {
                "question": "Ayah punya 3 anak: Budi, Budi, dan Budi. Berapa nama anak perempuannya?",
                "options": ["Budi", "Tidak ada", "Budiarti", "Perempuan tidak disebutkan"],
                "answer": 1  # Tidak ada (semua anak laki-laki)
            },
            {
                "question": "Mana yang lebih berat: 1 kg besi atau 1 kg kapas?",
                "options": ["Besi", "Kapas", "Sama berat", "Tidak bisa ditimbang"],
                "answer": 2  # Sama berat
            },
            {
                "question": "Sebuah kelelawar dan bola total Rp110.000. Kelelawar Rp100.000 lebih mahal dari bola. Berapa harga bola?",
                "options": ["Rp5.000", "Rp10.000", "Rp15.000", "Rp50.000"],
                "answer": 0  # Rp5.000 (kelelawar Rp105.000)
            },
            {
                "question": "Lomba lari, anda start di posisi ke-6. Setiap orang yang anda lewati akan ke posisi berapa?",
                "options": ["Ke-5", "Ke-7", "Ke-6", "Tetap di posisi awal"],
                "answer": 3  # Tetap di posisi awal (anda naik posisi, mereka tidak berubah)
            },
            {
                "question": "Jika ada 12 ikan di akuarium dan 11 mati, berapa yang tersisa?",
                "options": ["1", "0", "11", "12"],
                "answer": 0  # 1 (yang masih hidup)
            },
            {
                "question": "Sebuah tangga punya 7 anak tangga. Seseorang naik 2 anak tangga, turun 1. Berapa kali ia harus naik untuk sampai atas?",
                "options": ["4", "5", "6", "7"],
                "answer": 2  # 6 kali (naik bersih 1 anak tangga per 3 langkah)
            },
            {
                "question": "Dokter memberikan 3 pil dan bilang 'minum 1 pil setiap setengah jam'. Berapa lama 3 pil habis?",
                "options": ["1 jam", "1,5 jam", "3 jam", "1 jam 30 menit"],
                "answer": 1  # 1 jam (pil 1 jam 0 menit, pil 2 jam 30 menit, pil 3 jam 1 jam)
            },
            {
                "question": "Anda punya korek api. Masuk kamar gelap ada lilin, kompor gas, dan lampu minyak. Mana yang Anda nyalakan pertama?",
                "options": ["Lilin", "Kompor gas", "Lampu minyak", "Korek api"],
                "answer": 3  # Korek api (harus dinyalakan dulu)
            }
        ]
    
    def display_header(self):
        """Menampilkan header game"""
        print("=" * 60)
        print("🧠 SELAMAT DATANG DI GAME UJI KECERDASAN 🧠")
        print("=" * 60)
        print("Aturan:")
        print("- Jawab 10 soal pilihan ganda")
        print("- Pilih jawaban dengan angka 0-3")
        print("- Semakin cepat benar, bonus poin!")
        print("- Good Luck! 🎯")
        print("=" * 60)
        input("\nTekan Enter untuk mulai...")
    
    def ask_question(self, q_data, index):
        """Menampilkan soal dan pilihan jawaban"""
        print(f"\n📝 SOAL {index + 1}/10")
        print(f"❓ {q_data['question']}")
        print("-" * 50)
        for i, option in enumerate(q_data['options']):
            print(f"{i}. {option}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            choice = int(input("Pilih jawaban (0-3): "))
            elapsed = time.time() - start_time
            
            if 0 <= choice <= 3:
                if choice == q_data['answer']:
                    self.total_questions += 1
                    if elapsed <= 10:
                        self.score += 10
                        print("✅ BENAR! 🎉 Bonus waktu!")
                    elif elapsed <= 20:
                        self.score += 8
                        print("✅ BENAR! 👍")
                    else:
                        self.score += 5
                        print("✅ BENAR! (sedikit lambat)")
                    return True
                else:
                    print("❌ SALAH! Jawaban benar adalah:", q_data['options'][q_data['answer']])
                    self.total_questions += 1
                    return False
            else:
                print("❌ Pilihan tidak valid!")
                return False
        except ValueError:
            print("❌ Masukkan angka 0-3 saja!")
            return False
    
    def play(self):
        """Menjalankan game utama"""
        self.display_header()
        random.shuffle(self.questions)  # Acak soal
        
        for i, q in enumerate(self.questions):
            self.ask_question(q, i)
            if i < len(self.questions) - 1:
                input("\nTekan Enter untuk soal berikutnya...")
        
        # Tampilkan hasil akhir
        self.show_results()
    
    def show_results(self):
        """Menampilkan hasil akhir"""
        print("\n" + "=" * 60)
        print("🏆 HASIL AKHIR 🏆")
        print("=" * 60)
        
        percentage = (self.score / 100) * 100
        print(f"📊 Skor Anda: {self.score}/100 ({percentage:.1f}%)")
        print(f"📝 Total soal dijawab: {self.total_questions}/10")
        
        if percentage >= 90:
            print("🥇 GENIUS! Anda luar biasa! 🌟")
        elif percentage >= 70:
            print("🥈 SANGAT BAGUS! Terus latih otak Anda! 💪")
        elif percentage >= 50:
            print("🥉 LUMAYAN! Masih perlu latihan! 📚")
        else:
            print("😅 Perlu latihan lebih keras! Jangan menyerah! 🔥")
        
        print("=" * 60)

# Jalankan game
if __name__ == "__main__":
    game = GameKecerdasan()
    game.play()
    
    # Opsi main lagi
    while True:
        play_again = input("\nMain lagi? (y/n): ").lower()
        if play_again == 'y':
            game.__init__()  # Reset game
            game.play()
        else:
            print("Terima kasih telah bermain! 🧠✨")
            break