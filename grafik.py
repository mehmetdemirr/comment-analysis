import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from nlp_model import analyze_keywords

#Bu Yıl Aylara Göre Toplam Değerlendirme Çubuk Grafiği (ayda kaç değerlendirme yapmış)
def plot_star_bar_chart(comments):
    # Aylara göre toplam yıldız sayılarını saklamak için bir sözlük oluştur
    total_stars_by_month = defaultdict(int)
    # Yorumları dön
    for comment in comments:
        if isinstance(comment.tarih, datetime):
            if comment.tarih.year == datetime.now().year:
                # Tarihi aya çevir
                month = comment.tarih.month
                # Yıldız sayısını ilgili aya ekleyin
                total_stars_by_month[month] += 1  #comment.yildiz
    # Yıldız çubuk grafiğini çiz
    labels = [f'{month}' for month in range(1, 13)]
    values = [total_stars_by_month[month] for month in range(1, 13)]

    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Aylar')
    plt.ylabel('Toplam Yıldız Sayısı')
    plt.title('Bu Yıl Aylara Göre Toplam Değerlendirme Çubuk Grafiği')
    # plt.show()

#Son Yıl Toplam Aylara Göre Yorum Grafiği (ayda kaç değerlendirme yapmış)
def ayYorumGrafigi(comments):
     ## Son Yıl Toplam Aylara Göre Yorum Grafiği ##
    # Verileri oluştur
    x = [1, 2, 3, 4,5,6,7,8,9,10,11,12]
    y = [0,0,0,0,0,0,0,0,0,0,0,0]
    # Şu anki tarihi alın
    now = datetime.now()
    # Bu seneye ait yorumları filtreleyin
    for i in comments:
        if isinstance(i.tarih, datetime):
            if i.tarih.year == now.year:
                # print(f"{i.tarih.month}-{i.tarih.year }")
                y[i.tarih.month-1]+=1
    # Grafik oluştur
    plt.plot(x, y)
    plt.xlabel('Aylar')
    plt.ylabel('Yorum Sayısı')
    plt.title('Son Yıl Toplam Aylara Göre Yorum Grafiği')
    # plt.show()
    # # Grafik ve verileri PDF dosyasına ekleyerek kaydet
    # with PdfPages('grafik_ve_veriler.pdf') as pdf:
    #     # Grafik sayfasını ekleyin
    #     pdf.savefig()
    #     plt.close()
    #     # Verileri ekleyin
    #     pdf.attach_note("Bu bir not. İsteğe bağlı olarak eklenebilir.")
    # print("PDF dosyası oluşturuldu.")

#Yıllara Göre Toplam Yıldız Çubuk Grafiği
def plot_yearly_bar_chart(comments):
    # Yıllara göre toplam yıldız sayılarını saklamak için bir sözlük oluştur
    total_stars_by_year = defaultdict(int)
    
    # Yorumları dön
    for comment in comments:
        if isinstance(comment.tarih, datetime):
            # Tarihi yıla çevir
            year = comment.tarih.year
            # Yıldız sayısını ilgili yıla ekleyin
            total_stars_by_year[year] += 1  # comment.yildiz
    
    # Yıldız çubuk grafiğini çiz
    labels = [str(year) for year in sorted(total_stars_by_year.keys())]
    values = [total_stars_by_year[year] for year in sorted(total_stars_by_year.keys())]

    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Yıllar')
    plt.ylabel('Toplam Yıldız Sayısı')
    plt.title('Yıllara Göre Toplam Yıldız Çubuk Grafiği')
    # plt.show()


#Yıldız - Ay /Yıl/Tüm Zaman
def daireGrafigi(comments, grafikTitle):
    ##Genel Yıldız oranı ##
    labels = ['1 Yıldız', '2 Yıldız', '3 Yıldız', '4 Yıldız', '5 Yıldız']
    values = [0, 0, 0, 0, 0]
    for i in comments:
        values[i.yildiz - 1] += 1
    
    # Pasta grafiğini oluştur
    plt.pie(values, labels=labels, autopct=lambda p: '{:.1f}%\n({:d})'.format(p, int(round(p * sum(values) / 100))),
            startangle=90)
    plt.title(grafikTitle)
    
    # Grafiği göster
    plt.axis('equal')  # Dairesel bir görünüm elde etmek için
    # plt.show()


#tüm zaman olumlu olumsuz nötr değerlendirme
def daireGrafigiDegerlendirmeli(comments, grafikTitle):
    # Genel Yıldız oranı
    labels = ['Olumsuz', 'Nötr', 'Olumlu']
    values = [0, 0, 0]
    
    for comment in comments:
        if comment.yildiz <= 2:
            values[0] += 1
        elif comment.yildiz == 3:
            values[1] += 1
        elif comment.yildiz >= 4:
            values[2] += 1
    
    # Pasta grafiğini oluştur
    plt.pie(values, labels=labels, autopct=lambda p: '{:.1f}%\n({:d})'.format(p, int(round(p * sum(values) / 100))),
            startangle=90)
    plt.title(grafikTitle)
    
    # Grafiği göster
    plt.axis('equal')  # Dairesel bir görünüm elde etmek için
    # plt.show()
#dil yorum pasta grafigi
def dil_pasta_grafigi(comments,title):
    # Yorumlardan dil sayılarına ulaşmak için Counter kullan
    dil_sayilari = Counter(comment.dil for comment in comments)

    # Pasta grafiğini oluştur
    labels = dil_sayilari.keys()
    values = dil_sayilari.values()

    plt.pie(values, labels=labels, autopct=lambda p: '{:.1f}%\n({:d})'.format(p, int(round(p * sum(values) / 100))),
            startangle=90)
    plt.title(title)

    # Grafiği göster
    # plt.show()


#yorumların türe göre pasta grafiği
def tur_pasta_grafigi(comments, title):
    # Yorumlardan tür sayılarına ulaşmak için Counter kullan
    tur_sayilari = Counter(comment.tur for comment in comments)

    # Pasta grafiğini oluştur
    labels = tur_sayilari.keys()
    values = tur_sayilari.values()

    plt.pie(values, labels=labels, autopct=lambda p: '{:.1f}%\n({:d})'.format(p, int(round(p * sum(values) / 100))),
            startangle=90)
    plt.title(title)

    # Grafiği göster
    # plt.show()

def save_to_pdf(file_name, comments):
    # PDF dosyasına grafikleri ve metinleri ekle
    pdf_pages = PdfPages(file_name)

    # Birinci grafik
    plt.figure(figsize=(8, 4))
    plot_star_bar_chart(comments)
    plt.title("Bu Yıl Aylara Göre Toplam Değerlendirme Grafiği")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # İkinci grafik
    plt.figure(figsize=(8, 4))
    ayYorumGrafigi(comments)
    plt.title("Son Yıl Toplam Aylara Göre Yorum Grafiği ")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Üçüncü grafik
    plt.figure(figsize=(8, 4))
    plot_yearly_bar_chart(comments)
    plt.title("Yıllara Göre Toplam Yıldız Çubuk Grafiği")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Dördüncü grafik
    plt.figure(figsize=(8, 4))
    tur_pasta_grafigi(comments,"Tüm Zaman Değerlendirme Pasta Grafiği")
    plt.title("Yıllara Göre Toplam Yıldız Çubuk Grafiği")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Beşinci grafik
    plt.figure(figsize=(8, 4))
    daireGrafigiDegerlendirmeli(comments,"Tüm Zaman Yıldız Değerlendirme Pasta Grafiği")
    plt.title("Yıllara Göre Toplam Yıldız Çubuk Grafiği")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Altıncı grafik
    plt.figure(figsize=(8, 4))
    dil_pasta_grafigi(comments,"Tüm Zaman Yorum Dili Dağılımı Pasta Grafiği")
    plt.title("Yorumların Dillere Göre Dağılımı")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # Yedinci grafik
    plt.figure(figsize=(8, 4))
    tur_pasta_grafigi(comments,"Tüm Zaman Tür Dağılımı Pasta Grafiği")
    plt.title("Yorumların İçeriğine Değerlendirmesine Göre Dağılımı")
    pdf_pages.savefig(bbox_inches='tight', pad_inches=0.5)
    plt.close()

    # PDF dosyasını kapat
    pdf_pages.close()

def yorumlarRapor(comments):
# CommentList'ten bir DataFrame oluşturun
    df = pd.DataFrame([[comment.yazar, comment.icerigi, comment.tarih, comment.yildiz, comment.GBT, comment.tur, comment.dil] for comment in comments],
                    columns=['Yorum Yazarı', 'Yorum İçeriği', 'Tarih', 'Yıldız', 'GBT', 'Tur', 'Dil'])

    # DataFrame'i Excel dosyasına yazın
    df.to_excel('rapor.xlsx', index=False)

def create_custom_pdf(file_name, comments):
    text=""
    # Pozitif duyguya sahip yorumların en sık geçen 5 kelimesini analiz et
    positive_keywords = analyze_keywords(comments, "Pozitif")
    text+=f"Pozitif duygu icin en sik geçen kelimeler:\n{positive_keywords}"
    # Negatif duyguya sahip yorumların en sık geçen 5 kelimesini analiz et
    negative_keywords = analyze_keywords(comments, "Negatif")
    text+=f"\n\nNegatif duygu icin en sik gecen kelimeler:\n{negative_keywords}"
    # PDF dosyasını oluştur
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Metni PDF'e ekle
    styles = getSampleStyleSheet()
    custom_text_paragraph = Paragraph(text, styles['Normal'])
    elements = [custom_text_paragraph]

    # PDF dosyasını oluşturun
    pdf.build(elements)

    # PDF dosyasını kaydet
    with open(file_name, 'wb') as f:
        f.write(pdf_buffer.getvalue())


# def tablo(comments): # type: ignore
#     # Verileri tanımla
#     kategoriler = ["Yazar","İçeriği"]
#     veri1 = [1,2]#[comment.yazar for comment in comments]
#     veri2 =  [3,4]# [comment.icerigi for comment in comments]

#     # Tabloyu oluştur
#     fig, ax = plt.subplots()

#     # Tabloya verileri ekle
#     ax.bar(kategoriler, veri1, label='Veri 1', color='blue')
#     ax.bar(kategoriler, veri2, label='Veri 2', color='orange', bottom=veri1)

#     # Eksen etiketlerini ve başlığı ekle
#     ax.set_xlabel('Kategoriler')
#     ax.set_ylabel('Değerler')
#     ax.set_title('İki Veri Setine Sahip Tablo')

#     # Legend (leyenda) ekleyerek hangi renklerin hangi veriyi temsil ettiğini gösterin
#     ax.legend()

#     # Tabloyu göster
#     # plt.show()




# def tablo(comments):
#     df = pd.DataFrame([[comment.yazar, comment.icerigi, comment.tarih, comment.yildiz, comment.GBT, comment.dil, comment.tur] for comment in comments],
#                   columns=['Yazar', 'İçerik', 'Tarih', 'Yıldız', 'GBT', 'Dil', 'Tür'])
#     # Tabloyu oluştur
#     fig, ax = plt.subplots()
#     # Tabloyu gizle
#     ax.axis('off')
#    # Tabloyu oluştur
#     table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', fontsize=12)  # Font boyutunu ayarla
#     table.auto_set_font_size(False)  # Otomatik font boyutunu kapat
#     table.set_fontsize(12)  # Font boyutunu ayarla
#     # Tablonun genişliğini ve yüksekliğini ayarla
#     table.auto_set_column_width([0, 1, 2, 3, 4, 5, 6])  # Tüm sütunları sığacak şekilde ayarla
#     # Tablonun yüksekliğini ayarla
#     table.auto_set_column_width(0)  # İlgili sütunu baz alarak genişlik ayarla
#     # Tabloyu göster
#     # plt.show()

# def draw_table(data, pdf):
#     # Tabloyu oluştur
#     table_style = [('GRID', (0, 0), (-1, -1), 1, colors.black),
#                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                    ('ALIGN', (0, 0), (-1, -1), 'CENTER')]

#     table = Table(data, style=table_style)

#     # Tabloyu PDF'ye ekle
#     table.wrapOn(pdf, 400, 300) # type: ignore
#     table.drawOn(pdf, 50, 50) # type: ignore