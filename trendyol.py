from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import gbt

def basindaki_sayiyi_al(string):
        sayi = ''
        for karakter in string:
            if karakter.isdigit():
                sayi += karakter
            else:
                break
        if sayi:
            return int(sayi)
        else:
            return None

class Comment:
    def __init__(self, satici, isim, tarih, yildizlar, yorumIcerigi, GBT):
        self.satici = satici
        self.isim = isim
        self.tarih = tarih
        self.yildizlar = yildizlar
        self.yorumIcerigi = yorumIcerigi
        self.GBT = GBT

class TrendyolScraper:
    def __init__(self, product_url):
        self.product_url = product_url
        self.driver = webdriver.Firefox()
        self.comments_list = []

    def get_total_reviews(self):
        self.driver.get(self.product_url)
        time.sleep(3)
        dahaFazlaYorum = self.driver.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/div[2]/div/div[3]')
        dahaFazlaYorum.click()
        time.sleep(2)
        toplamYorumSayisi = self.driver.find_element(By.XPATH, '//*[@id="rating-and-review-app"]/div/div/div/div[1]/div/div[3]/div[2]/div[3]/div').text
        return basindaki_sayiyi_al(toplamYorumSayisi)

    def scroll_to_load_reviews(self):
        yorumlar = self.driver.find_elements(By.CLASS_NAME, 'comment')
        body = self.driver.find_element(By.XPATH, '//*[@id="rating-and-review-app"]/div/div/div/div[3]')
        self.driver.execute_script("arguments[0].scrollIntoView();", body)

        while len(yorumlar) != self.total_reviews:
            self.driver.execute_script("window.scrollBy(0, 400);")
            yorumlar = self.driver.find_elements(By.CLASS_NAME, 'comment')

    def scrape_reviews(self):
        self.total_reviews = self.get_total_reviews()
        self.scroll_to_load_reviews()
        yorumlar = self.driver.find_elements(By.CLASS_NAME, 'comment')
        for index, yorum in enumerate(yorumlar):
            yorumIcerigi = yorum.find_element(By.CLASS_NAME, "comment-text").text
            satici = yorum.find_element(By.CLASS_NAME, "seller-name-info").text
            yildizlar = yorum.find_elements(By.XPATH, "//div[contains(@class, 'full') and contains(@style, 'width: 100%; max-width: 100%')]")
            isim = yorum.find_elements(By.CLASS_NAME, "comment-info-item")[0].text
            tarih = yorum.find_elements(By.CLASS_NAME, "comment-info-item")[1].text
            response = '-'#gbt.normal(f"Kullanıcı Yorumu '{yorumIcerigi}' ne anlatmak istemiş yorumda ")
            comment = Comment(satici, isim, tarih, len(yildizlar), yorumIcerigi, response)
            self.comments_list.append(comment)
            # print(f"{index + 1} Satıcı: {satici} İsim: {isim} Tarih:{tarih} Yıldız:{len(yildizlar)}\n-{yorumIcerigi}\n GBT:{response}")
    def gbt_anser_add_reviews(self):
        for comment in self.comments_list:
             response = gbt.normal(f"Kullanıcı Yorumu '{comment.yorumIcerigi}' ne anlatmak istemiş yorumda ")
             comment.GBT=response
             print(response)
    def reviews_print(self):
        for index,comment in enumerate(self.comments_list):
            print(f"İndex:{index+1} ,Satıcı: {comment.satici}, İsim: {comment.isim}, Tarih: {comment.tarih}, Yıldız: {comment.yildizlar}, Yorum: {comment.yorumIcerigi}, GBT: {comment.GBT}")
        
    def close_driver(self):
        self.driver.quit()

# Example usage:
if __name__ == "__main__":
    product_url = "https://www.trendyol.com/powerfox/air-pods-3-nesil-uyumlu-pastel-renkli-silikon-koruma-kopcali-airpods-kilif-p-737922541?boutiqueId=61&merchantId=118106"
    trendyol_scraper = TrendyolScraper(product_url)
    trendyol_scraper.scrape_reviews()
    trendyol_scraper.close_driver()
    trendyol_scraper.reviews_print()
    trendyol_scraper.gbt_anser_add_reviews()
    trendyol_scraper.reviews_print()