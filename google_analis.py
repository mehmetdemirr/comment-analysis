from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
from nlp_model import dilTespit,degerlendirmeTespit

from selenium.webdriver.firefox.options import Options

# Firefox tarayıcısını başlatmak için seçenekleri belirtin
options = Options()
options.headless = True
# Kullanıcı tarayıcı dilini Türkçe olarak belirle
options.add_argument("--intl.accept_languages=tr")
# Kullanıcı tarayıcı başlığını değiştirin
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def basindaki_sayiyi_al(string):
    sayi = ''
    for karakter in string:
        if karakter.isdigit() or karakter=='.':
            sayi += karakter
        else:
            break

    if sayi:
        return int(sayi.replace(".", ""))
    else:
        return None
    
def donustur(tarih_ifadesi):
    if "az önce" in tarih_ifadesi:
        return datetime.now()
    elif "dakika" in tarih_ifadesi:
        if "bir" in tarih_ifadesi:
            return datetime.now() - timedelta(minutes=1)
        else :
            return datetime.now() - timedelta(minutes=basindaki_sayiyi_al(tarih_ifadesi)) # type: ignore
    elif "saat" in tarih_ifadesi:
        if "bir" in tarih_ifadesi:
            return datetime.now() - timedelta(hours=1)
        else :
            return datetime.now() - timedelta(hours=basindaki_sayiyi_al(tarih_ifadesi)) # type: ignore
    elif "gün" in tarih_ifadesi:
        if "bir" in tarih_ifadesi:
            return datetime.now() - timedelta(days=1)
        else :
            return datetime.now() - timedelta(days=basindaki_sayiyi_al(tarih_ifadesi)) # type: ignore
    elif "hafta" in tarih_ifadesi:
        if "bir" in tarih_ifadesi:
            return datetime.now() - timedelta(weeks=1)
        else :
            return datetime.now() - timedelta(weeks=basindaki_sayiyi_al(tarih_ifadesi)) # type: ignore
    elif "ay" in tarih_ifadesi:
        if "bir" in tarih_ifadesi:
            return datetime.now() - timedelta(days=30)
        else :
            return datetime.now() - timedelta(days=30*basindaki_sayiyi_al(tarih_ifadesi)) # type: ignore
    elif "yıl" in tarih_ifadesi:
        if "bir" in tarih_ifadesi:
            return datetime.now() - timedelta(days=30*12)
        else :
            return datetime.now() - timedelta(days=30*12*basindaki_sayiyi_al(tarih_ifadesi)) # type: ignore
    else :
        return datetime.now()

class Comment:
    def __init__(self, yazar, icerigi, tarih, yildiz, GBT,dil,tur):
        self.yazar = yazar
        self.icerigi = icerigi
        self.tarih = tarih
        self.yildiz = yildiz
        self.GBT = GBT
        self.dil= dil
        self.tur=tur # negatif nötr pozitif

class GoogleAnalisScraper:
    def __init__(self, company_url):
        self.company_url = company_url
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Firefox(options=options)
        self.comments_list = []

    def get_total_reviews(self):
        self.driver.get(self.company_url)
        time.sleep(3)
        tabSayisi =len(self.driver.find_elements(By.CLASS_NAME,'hh2c6'))
        dahaFazlaYorum = self.driver.find_element(By.CSS_SELECTOR, f'[data-tab-index="{tabSayisi-2}"].hh2c6')
        dahaFazlaYorum.click()
        time.sleep(2)
        element = self.driver.find_element(By.CLASS_NAME,"jANrlb")
        # Bu div'in içindeki fontBodySmall class name li div'i bul
        inner_elementToplamYorum = element.find_element(By.CLASS_NAME,"fontBodySmall")
        # Bu div'in içindeki fontDisplayLarge class name li div'i bul
        inner_elementOrtalamaYildiz = element.find_element(By.CLASS_NAME,"fontDisplayLarge")
        toplamYorumSayisi =inner_elementToplamYorum.text
        sayi= basindaki_sayiyi_al(toplamYorumSayisi)
        print(f"toplam yorum : {sayi}")
        ortalamaYildiz = inner_elementOrtalamaYildiz.text#self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]').text                                       
        
        print(f"ortalama yıldız : {ortalamaYildiz}")
        return sayi

    def scroll_to_load_reviews(self):
        yorumlar = self.driver.find_elements(By.CSS_SELECTOR, '.jftiEf.fontBodyMedium')
        body = self.driver.find_element(By.CSS_SELECTOR, '.m6QErb.DxyBCb.kA9KIf.dS8AEf')
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", body)

        while True:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",body)
            yorumlar = self.driver.find_elements(By.CSS_SELECTOR, '.jftiEf.fontBodyMedium')
            print(f"{len(yorumlar)} yorum geldi...")
            # Beklenen toplam yorum sayısına ulaşıldıysa döngüyü sonlandır
            if len(yorumlar) >= self.total_reviews:
                break

    def scrape_reviews(self):
        self.total_reviews = self.get_total_reviews()
        self.scroll_to_load_reviews()
        yorumlar = self.driver.find_elements(By.CSS_SELECTOR, '.jftiEf.fontBodyMedium')
        for index, yorum in enumerate(yorumlar):
            yorumYazari = yorum.find_element(By.CLASS_NAME, 'd4r55').text
            yorumYildizSayisi = len(yorum.find_elements(By.CSS_SELECTOR, '.hCCjke.vzX5Ic'))
            yorumTarih = donustur(yorum.find_element(By.CLASS_NAME,'rsqaWe').text)
            try:
                yorumIcerigi = yorum.find_element(By.CLASS_NAME, 'wiI7pd').text
            except Exception:
                yorumIcerigi =""
            dil = dilTespit(yorumIcerigi) if yorumIcerigi != "" else "Yorum Yok"
            tur = degerlendirmeTespit(yorumIcerigi) if yorumIcerigi != "" else "Yorum Yok"
            comment = Comment(yorumYazari, yorumIcerigi, yorumTarih,yorumYildizSayisi,"",dil,tur)
            self.comments_list.append(comment)
            # print(f"{index+1}-{yorumYazari}-{yorumYildizSayisi} Yıldız - {yorumTarih}\n{yorumIcerigi}")
    # def gbt_anser_add_reviews(self):
    #     for comment in self.comments_list:
    #          response = gbt.normal(f"Kullanıcı Yorumu:'{comment.icerigi}\nHangi dil? ve pozitif negatif, nötr  veya bilinmiyor? Örnek Çıktı: türkçe-pozitif")
    #          comment.GBT=response
    #          print(response)
    def reviews_print(self):
        for index,comment in enumerate(self.comments_list):
            print(f"İndex:{index+1} ,Yazar: {comment.yazar}, Yorum: {comment.icerigi}, Tarih: {comment.tarih}, Yıldız: {comment.yildiz}, GBT: {comment.GBT}, Dil: {comment.dil}, Tür: {comment.tur}")
    def close_driver(self):
        self.driver.quit()

# # Example usage:
# if __name__ == "__main__":
#     product_url = "https://www.google.com/maps/place/Akdeniz+%C3%9Cniversitesi/@36.8958224,30.6476724,17z/data=!3m1!4b1!4m16!1m9!3m8!1s0x14c391c4eb3bc819:0x29c30089f6e24174!2sAkdeniz+%C3%9Cniversitesi!8m2!3d36.8958224!4d30.6502473!9m1!1b1!16s%2Fm%2F027j5lx!3m5!1s0x14c391c4eb3bc819:0x29c30089f6e24174!8m2!3d36.8958224!4d30.6502473!16s%2Fm%2F027j5lx?entry=ttu"
#     google_analis_scraper = GoogleAnalisScraper(product_url)
#     google_analis_scraper.scrape_reviews()
#     google_analis_scraper.close_driver()
#     google_analis_scraper.reviews_print()
#     # commentList=[
#     #     Comment("yorumYazari", "yorumIcerigi",datetime.now(),1,"","",""),
#     #     Comment("yorumYazari", "yorumIcerigi",datetime(year=2022,month=2,day=1),1,"","",""),
#     #     Comment("yorumYazari", "yorumIcerigi",datetime(year=2022,month=3,day=1),4,"","",""),
#     #     Comment("yorumYazari", "yorumIcerigi",datetime(year=2023,month=4,day=1),5,"","",""),
#     #     Comment("yorumYazari", "ddd",datetime(year=2023,month=5,day=1),2,"","",""),
#     #     Comment("mehmet", "yorumIcerigi", datetime(year=2021,month=5,day=1),2,"","",""),
#     #     Comment("a", "yorumIcerigi", datetime(year=2021,month=6,day=1),3,"","",""),
#     #     Comment("a", "yorumIcerigi", datetime(year=2020,month=9,day=1),3,"","",""),
#     #     Comment("a", "yorumIcerigi", datetime(year=2023,month=6,day=1),3,"","",""),
#     # ]

#     ######################
#     ######################
#     # daireGrafigi(comments=commentList,grafikTitle="Tüm Yorumların Yıldız Değerlendirme Grafiği")
#     #plot_star_bar_chart(comments=commentList)
#     # plot_yearly_bar_chart(comments=commentList)
#     # tablo(comments=commentList)
#     # daireGrafigiDegerlendirmeli(comments=commentList,grafikTitle="Tüm Yorumların Değerlendirme Grafiği")
#     save_to_pdf(file_name="grafikler_tablo.pdf",comments=google_analis_scraper.comments_list)
#     yorumlarRapor(comments=google_analis_scraper.comments_list)