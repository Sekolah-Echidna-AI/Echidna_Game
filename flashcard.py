import pygame
import sys

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Quiz App")

BG_COLOUR = "#0a092d"
FLASHCARD_COLOUR = "#2e3856"
FLIPPED_COLOUR = "#595e6d"
FONT = pygame.font.SysFont("Arial", 30)

SCREEN.fill(BG_COLOUR)

demo_quiz_data = {
{
    "Ibukota Indonesia adalah?": "Jakarta",
    "Siapa penemu teori relativitas?": "Albert Einstein",
    "Hukum Newton ke-1 dikenal sebagai hukum apa?": "Hukum Kelembaman",
    "3 + 7 * 2": "17",
    "Jika x^2 - 9 = 0, berapakah x?": "3 atau -3",
    "Organel sel yang menghasilkan energi disebut?": "Mitokondria",
    "Simbol kimia besi adalah?": "Fe",
    "Siapa presiden pertama Indonesia?": "Soekarno",
    "Sungai terpanjang di dunia adalah?": "Sungai Nil",
    "Sinonim kata 'besar' adalah?": "Raksasa atau luas",
    "Antonim kata 'cepat' adalah?": "Lambat",
    "Kalimat 'Saya sedang belajar' dalam bahasa Inggris?": "I am studying",
    "Hukum permintaan menyatakan ketika harga naik, permintaan akan...?": "Berkurang",
    "Alat musik tradisional Jawa yang dipukul disebut?": "Gamelan",
    "Luas segitiga dengan alas 10 cm dan tinggi 5 cm?": "25 cm²",
    "Percepatan gravitasi di bumi adalah?": "9,8 m/s²",
    "Makromolekul utama penyusun membran sel adalah?": "Lipid",
    "pH larutan netral adalah?": "7",
    "Indonesia merdeka pada tahun?": "1945",
    "Benua dengan populasi terbesar?": "Asia",
    "Sinonim kata 'baik' adalah?": "Bagus atau hebat",
    "Kalimat 'Dia suka membaca buku setiap hari' dalam bahasa Inggris?": "He/She likes reading books every day",
    "Struktur pasar dengan satu penjual disebut?": "Monopoli",
    "Teknik melukis dengan cat air di atas plester basah disebut?": "Fresco",
    "Selesaikan persamaan: 2y + 5 = 15": "y = 5",
    "Jika benda bergerak 10 m/s selama 3 detik, jarak yang ditempuh?": "30 m",
    "Sistem tubuh manusia yang mengatur hormon disebut?": "Sistem endokrin",
    "Rumus molekul air adalah?": "H2O",
    "Siapa penulis 'Laskar Pelangi'?": "Andrea Hirata",
    "Samudra terbesar di dunia adalah?": "Samudra Pasifik",
    "Sebutkan gas utama penyusun udara?": "Nitrogen",
    "Jenis ikatan kimia yang terjadi antara logam dan nonlogam disebut?": "Ionik",
    "Tingkat keasaman larutan asam sulfat pekat?": "Asam kuat",
    "Perubahan wujud dari cair menjadi gas disebut?": "Penguapan",
    "Rumus luas lingkaran adalah?": "π × r²",
    "Bilangan prima antara 10 dan 20 adalah?": "11, 13, 17, 19",
    "Siapa pahlawan nasional yang dijuluki 'Bapak Pendidikan Indonesia'?": "Ki Hajar Dewantara",
    "Gunung tertinggi di Indonesia adalah?": "Puncak Jaya",
    "Hewan yang bertelur disebut?": "Ovipar",
    "Sebutkan organ pernapasan utama manusia?": "Paru-paru",
    "Sebutkan alat musik tiup tradisional Sumatera Barat?": "Saluang",
    "Kalau 25% dari 200 adalah...?": "50",
    "Jika percepatan = 4 m/s² dan massa = 3 kg, gaya = ?": "12 N",
    "Jumlah sisi segilima adalah?": "5",
    "Contoh teks eksposisi adalah?": "Artikel ilmiah",
    "Kalimat majemuk setara memiliki ciri?": "Memiliki dua klausa yang setara",
    "Sebutkan salah satu negara ASEAN": "Malaysia",
    "Peran fotosintesis tumbuhan adalah?": "Menghasilkan oksigen dan glukosa",
    "Bilangan desimal 0,75 jika diubah menjadi persen adalah?": "75%",
    "Contoh simetri lipat pada bentuk geometri?": "Segitiga sama sisi"
}
}

current_question = ""
current_answer = ""

card_turned = False

index = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                card_turned = not card_turned
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and index < len(demo_quiz_data) - 1:
                index += 1
                card_turned = False
            elif pygame.key.get_pressed()[pygame.K_LEFT] and index > 0:
                index -= 1
                card_turned = False
    
    current_question = list(demo_quiz_data)[index]
    current_answer = list(demo_quiz_data.values())[index]
    current_question_object = FONT.render(current_question, True, "white")
    current_question_rect = current_question_object.get_rect(center=(400, 400))
    current_answer_object = FONT.render(current_answer, True, "white")
    current_answer_rect = current_answer_object.get_rect(center=(400, 400))
    current_index_object = FONT.render(f"{index+1}/{len(demo_quiz_data)}", True, "white")
    current_index_rect = current_index_object.get_rect(center=(400, 600))
    
    if not card_turned:
        SCREEN.fill(BG_COLOUR)
        pygame.draw.rect(SCREEN, FLASHCARD_COLOUR, (150, 250, 500, 300))
        SCREEN.blit(current_question_object, current_question_rect)
    else:
        SCREEN.fill(BG_COLOUR)
        pygame.draw.rect(SCREEN, FLIPPED_COLOUR, (150, 250, 500, 300))
        SCREEN.blit(current_answer_object, current_answer_rect)
    
    SCREEN.blit(current_index_object, current_index_rect)
    
    pygame.display.update()