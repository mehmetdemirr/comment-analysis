from langdetect import detect
import langid
import guess_language
from googletrans import Translator
from transformers import pipeline
import spacy
from collections import Counter
# from textblob import TextBlob
# from polyglot.detect import Detector
# import pycld2



def clean_text_normal(text):
    # Gerektiğine göre metni temizleme işlemleri burada yapılabilir
    cleaned_text = text.replace("\n", "").replace("\r", "")
    return cleaned_text

def clean_text_utf(text):
    # Geçerli UTF-8 karakterlere sahip olanları koru
    cleaned_text = ''.join(char for char in text if char.isprintable() and ord(char) < 128)
    return cleaned_text

def dilTespit(comment):
    comment=clean_text_normal(comment)
    # langid
    langid_lang, _ = langid.classify(comment)
    
    # langdetect
    langdetect_lang = detect(comment) if len(comment) >= 10 else "" 

    #guess language
    guess_language_lang = guess_language.guess_language(comment)

    try:
        translator = Translator()
        dil = translator.detect(comment).lang
    except Exception as e:
        print(f"hata: {e}")
        dil=""


    #***pycld2
    #     _, _, _, pycld2_detected_language = pycld2.detect(clean_text_utf(comment)
    # ,  returnVectors=True)
    #****spacy    *****Hatalı veriyor****
    # spacy_lang = nlp(comment).lang_
    #****text blob
    # c = TextBlob(comment) 
    # textblob_lang=c.detect_language()
    # polyglot
    # polyglot_lang = Detector(comment)
    

    # En yaygın dilin seçimi
    languages = [langid_lang, langdetect_lang,guess_language_lang]
    most_common_lang = max(set(languages), key=languages.count)
    
    return dil

nlpDegerlendirme = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def degerlendirmeTespit(comment):
    # Yorumu analiz et
    result = nlpDegerlendirme(comment)
    # Sentiment etiketini al
    sentiment_label = result[0]['label']
    return sentiment_label
nlp = spacy.load("en_core_web_lg")
def analyze_sentiment(comment):
    # Yorumu işleyin
    doc = nlp(comment)
    # Duygu skorunu kontrol edin
    sentiment_score = doc.sentiment
    # Duygu skoruna göre pozitif veya negatif olarak etiketleyin
    sentiment = "Pozitif" if sentiment_score >= 0 else "Negatif"
    return sentiment

def analyze_keywords(comments, sentiment):
    # Belirtilen duyguya sahip yorumlardan kelimeleri çıkarma
    keyword_counter = Counter()
    for comment in comments:
        if analyze_sentiment(comment.icerigi) == sentiment:
            for token in nlp(comment.icerigi):
                if token.is_alpha and not token.is_stop:
                    keyword_counter[token.lemma_] += 1

    # En sık geçen 5 kelimeyi döndür
    return keyword_counter.most_common(5)


# Yorumları dil tespiti yap
# comments = [
#     "Hello, how are you?",
#     "Bonjour, comment ça va?",
#     "Hola, ¿cómo estás?",
#     "你好，你好吗？",
#     "nasılsın ?",
# ]

# for comment in comments:
#     language, confidence = langid.classify(comment)

#     print(f"Yorum: {comment}")
#     print(f"Tespit Edilen Dil: {language}")
#     #print(f"Güvenlik: {confidence}\n")

# Duygu analizi için modeli yükle

# # Yorumları sınıflandır
# comments = [
#     "Bu ürünü gerçekten çok sevdim, harika!",
#     "Maalesef beklediğim gibi değildi.",
#     "Bu ürün hakkında bir şey söylemek zor.",
#     "Tam olarak ne düşündüğümü anlayamadım.",
#     "ürün güzel.",
# ]

# for comment in comments:
#     result = nlp(comment)
#     sentiment = result[0]['label'] # type: ignore
#     confidence = result[0]['score'] # type: ignore

#     print(f"Yorum: {comment}")
#     print(f"Duygu: {sentiment}")
#     print(f"Güvenlik: {confidence}\n")

