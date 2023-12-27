from tkinter import Tk, Label, Entry, Button,messagebox
from google_analis import GoogleAnalisScraper
from grafik import save_to_pdf,yorumlarRapor,create_custom_pdf

# Ana pencereyi oluştur
root = Tk()
def show_completed_message():
    messagebox.showinfo("Tamamlandı", "Tamamlandı")

def center_window(window, width, height):
    # Ekranın genişliğini ve yüksekliğini al
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Pencerenin x ve y konumunu ayarla
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Pencerenin boyutunu ve konumunu ayarla
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_browser():
    url = entry.get()
    google_analis_scraper = GoogleAnalisScraper(url)
    google_analis_scraper.scrape_reviews()
    google_analis_scraper.close_driver()
    google_analis_scraper.reviews_print()
    #yorum analiz grafik
    save_to_pdf(file_name="grafikler_tablo.pdf",comments=google_analis_scraper.comments_list)
    #yorumların excel listesi
    yorumlarRapor(comments=google_analis_scraper.comments_list)
    #en çok kullanılan 5 pozitif ve negatif kelime
    create_custom_pdf(file_name="negatif-pozitif-kelimeler.pdf",comments=google_analis_scraper.comments_list)

    show_completed_message()
    # root.destroy()

# Pencere boyutunu ve konumunu ayarla
window_width = 600
window_height = 200
center_window(root, window_width, window_height)
root.title("Google İşletme Analiz Botu")

# URL girişi için etiket
label = Label(root, text="URL:")
label.pack()

# URL giriş alanı
entry = Entry(root, width=100)
entry.pack()

# Tarayıcıyı açan düğme
button = Button(root, text="Çalıştır", command=open_browser)
button.pack()

# Pencereyi başlat
root.mainloop()
