# main.py
from tcmb_analyzer import TCMBKrediKartiAnalizoru

def main():
    print("Kredi Kartı Analiz Sistemi (Dinamik Haftalık CSV Modu) Başlatılıyor...")
    
    # Sınıfa CSV dosyasının yolunu vererek başlat
    # Dosya yolu: 'data/veri.csv'
    analizor = TCMBKrediKartiAnalizoru(input_file="data/veri.csv")
    
    # Analiz sürecini çalıştır
    analizor.calistir()

if __name__ == "__main__":
    main()