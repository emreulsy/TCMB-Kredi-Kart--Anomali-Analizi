# korelasyon_analizi.py
import pandas as pd
import os
import warnings

# --- AYARLAR ---
# Bu analiz, enflasyondan arındırılmış en temiz veriyi, yani AYLIK PAYLARI kullanacak.
INPUT_FILE = 'output/rapor_aylik_paylar.csv' 
OUTPUT_PRE_COVID = 'output/rapor_korelasyon_PandemiOncesi.csv'
OUTPUT_POST_COVID = 'output/rapor_korelasyon_YeniNormal.csv'

# Pandemi dönemlerini tanımlayalım
PRE_COVID_END = '2020-02-29'
# Yeni normali, en sert kapanmaların bittiği ve enflasyonist dönemin başladığı
# 2022 başı olarak alabiliriz.
POST_COVID_START = '2022-01-01'

def korelasyon_analizi():
    print(f"'{INPUT_FILE}' raporu okunuyor...")
    try:
        # Tarih sütununu index olarak okuyarak başlayalım
        data = pd.read_csv(INPUT_FILE, index_col='Tarih', parse_dates=True)
    except FileNotFoundError:
        print(f"HATA: '{INPUT_FILE}' bulunamadı.")
        print("Lütfen önce 'python.exe main.py' komutunu çalıştırarak ana raporları oluşturduğunuzdan emin olun.")
        return
    except Exception as e:
        print(f"Hata: {e}")
        return

    print("Veri dönemlere ayrılıyor...")
    
    # Dönem 1: Pandemi Öncesi
    pre_covid_data = data.loc[data.index <= PRE_COVID_END]
    
    # Dönem 2: Yeni Normal (Pandemi sonrası ve yüksek enflasyon dönemi)
    post_covid_data = data.loc[data.index >= POST_COVID_START]

    if pre_covid_data.empty:
        print("HATA: Pandemi öncesi (2020-02 öncesi) veri bulunamadı.")
        return
    if post_covid_data.empty:
        print("HATA: Pandemi sonrası (2022-01 sonrası) veri bulunamadı.")
        return

    print("Korelasyon matrisleri hesaplanıyor...")

    # Korelasyon matrislerini hesapla
    # .corr() fonksiyonu, her sütunun diğer her sütunla olan ilişkisini hesaplar
    # warnings.catch_warnings() bloğu, standart sapması 0 olan (örn: hiç değişmeyen)
    # sektörler için oluşabilecek anlamsız uyarıları gizler.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        corr_pre_covid = pre_covid_data.corr().round(2)
        corr_post_covid = post_covid_data.corr().round(2)

    try:
        # Raporları kaydet
        corr_pre_covid.to_csv(OUTPUT_PRE_COVID, encoding='utf-8-sig')
        print(f"Pandemi öncesi korelasyon raporu kaydedildi: {OUTPUT_PRE_COVID}")
        
        corr_post_covid.to_csv(OUTPUT_POST_COVID, encoding='utf-8-sig')
        print(f"Yeni normal korelasyon raporu kaydedildi: {OUTPUT_POST_COVID}")
        
        print("\nAnaliz tamamlandı. Şimdi iki CSV dosyasını karşılaştırabilirsiniz.")
        
    except Exception as e:
        print(f"Rapor kaydedilirken hata oluştu: {e}")

# Script'i çalıştırmak için ana fonksiyon
if __name__ == "__main__":
    korelasyon_analizi()