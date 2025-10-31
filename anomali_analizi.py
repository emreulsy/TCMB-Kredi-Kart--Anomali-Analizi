# anomali_analizi.py
import pandas as pd
import os

# --- AYARLAR ---
# Bu rapor, haftalık yıllık büyümeyi baz alacak
INPUT_FILE = 'output/rapor_haftalik_yillik_buyume.csv' 
OUTPUT_FILE = 'output/rapor_anomaliler.csv'

# Bir verinin "anomali" sayılması için ortalamadan kaç standart sapma
# (kaç kat) uzaklaşması gerektiğini belirler.
# 2.5, istatistiksel olarak anlamlı ama çok da nadir olmayan
# "incelenmeye değer" olayları yakalamak için iyi bir ayardır.
STD_DEV_THRESHOLD = 2.5 

def anomali_tespiti():
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

    print("Anomaliler tespit ediliyor...")
    anomali_listesi = []

    # Her bir sektör sütununda tek tek gezin
    for sektor in data.columns:
        sektor_verisi = data[sektor].dropna() # Boş verileri atla
        
        # Sektörün "normal" koridorunu hesapla
        ortalama_buyume = sektor_verisi.mean()
        standart_sapma = sektor_verisi.std()
        
        # Anomali sınırlarını belirle
        ust_sinir = ortalama_buyume + (STD_DEV_THRESHOLD * standart_sapma)
        alt_sinir = ortalama_buyume - (STD_DEV_THRESHOLD * standart_sapma)
        
        # Sınırların dışına çıkan verileri bul
        anomaliler = sektor_verisi[ (sektor_verisi > ust_sinir) | (sektor_verisi < alt_sinir) ]
        
        # Bulunan anomalileri listeye ekle
        for tarih, deger in anomaliler.items():
            if deger > ust_sinir:
                tip = "Pozitif Şok (Beklenmedik Büyüme)"
                beklenen_sinir = ust_sinir
            else:
                tip = "Negatif Şok (Beklenmedik Düşüş)"
                beklenen_sinir = alt_sinir
                
            anomali_listesi.append({
                'Tarih': tarih.strftime('%Y-%m-%d'),
                'Sektor_Kodu': sektor,
                'Gerceklesen_Buyume_Yuzde': round(deger, 2),
                'Beklenen_Normal_Sinir_Yuzde': round(beklenen_sinir, 2),
                'Ortalama_Buyume_Yuzde': round(ortalama_buyume, 2),
                'Anomali_Tipi': tip
            })

    if not anomali_listesi:
        print("İncelenen dönemde belirgin bir anomali bulunamadı.")
        return

    print(f"Toplam {len(anomali_listesi)} adet incelenmeye değer anomali bulundu.")
    
    # Anomali listesini DataFrame'e çevir ve kaydet
    df_anomali = pd.DataFrame(anomali_listesi)
    df_anomali.sort_values(by='Tarih', inplace=True)
    
    try:
        df_anomali.to_csv(OUTPUT_FILE, encoding='utf-8-sig', index=False)
        print(f"Anomali raporu başarıyla kaydedildi: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Rapor kaydedilirken hata oluştu: {e}")

# Script'i çalıştırmak için ana fonksiyon
if __name__ == "__main__":
    anomali_tespiti()