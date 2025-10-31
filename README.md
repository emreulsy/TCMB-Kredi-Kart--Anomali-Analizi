# TCMB Kredi Kartı Anomali Analizi
A Python-based analysis system that processes TCMB EVDS credit card data (2018-2025) to generate reports on consumer trends, detect statistical anomalies, and analyze post-pandemic behavioral shifts.
# TCMB Kredi Kartı Harcama Analiz Sistemi

Bu proje, Türkiye Cumhuriyet Merkez Bankası (TCMB) Elektronik Veri Dağıtım Sistemi (EVDS) üzerinden alınan 2018-2025 dönemi haftalık kredi kartı harcama verilerini analiz etmek için geliştirilmiş bir Python sistemidir.

Projenin temel amacı, yüzeysel tespitlerin ("Pandemide havayolları düştü") ötesine geçerek, "gözden kaçan" içgörüleri, istatistiksel anomalileri ve tüketici davranışındaki kalıcı yapısal kırılmaları (örn: 2018 Kur Krizi, 2020 Pandemisi) ortaya çıkarmaktır.

## Temel Özellikler

Bu sistem, manuel olarak indirilen `data/veri.csv` dosyasını okur ve 30'dan fazla sektörü dinamik olarak tanır. Aşağıdaki 3 katmanlı analizi otomatik olarak yapar ve `output/` klasörüne kaydeder:

### Katman 1: Veri İşleme ve Temel Raporlar
Sistem, ham haftalık veriyi işler ve temel trend raporları oluşturur:
1.  **`rapor_haftalik_toplamlar.csv`**: Sektörlerin haftalık nominal harcama tutarları.
2.  **`rapor_aylik_toplamlar.csv`**: Haftalık verinin aylık toplamlara dönüştürülmüş hali.
3.  **`rapor_buyume_istatistikleri.csv`**: Sektörlerin 2018'den 2025'e kümülatif büyüme istatistikleri.

### Katman 2: Davranışsal Analiz Raporları
Enflasyon gibi "gürültüleri" filtrelemek ve gerçek tüketici davranışını anlamak için "pay" analizleri üretir:
4.  **`rapor_haftalik_paylar.csv`**: Her sektörün, o haftaki toplam harcama sepetinden aldığı yüzde pay.
5.  **`rapor_aylik_paylar.csv`**: Uzun vadeli trend analizi için aylık harcama payları.
6.  **`rapor_haftalik_yillik_buyume.csv`**: Mevsimsellikten arındırılmış, bir önceki yılın aynı haftasına göre yüzde büyüme.

### Katman 3: İleri Analiz ve İçgörü Raporları
"Neden?" sorusunu cevaplamak için iki adet ikinci seviye analiz script'i içerir:

7.  **`rapor_anomaliler.csv` (Anomali Tespiti):**
    * `anomali_analizi.py` script'i tarafından üretilir.
    * Her sektörün "normal" büyüme koridorunu hesaplar ve bu koridorun dışına çıkan "Pozitif/Negatif Şok"ları (örn: 2018 kur krizi panik alımları) tarihleriyle birlikte listeler.

8.  **`rapor_korelasyon_...csv` (Korelasyon Analizi):**
    * `korelasyon_analizi.py` script'i tarafından üretilir.
    * **Pandemi Öncesi (2018-19)** ve **Yeni Normal (2022-25)** dönemleri için sektörler arası ilişki haritalarını çıkarır.
    * "Restoran vs Market" veya "Telekom vs E-ticaret" gibi sektörler arası ilişkilerin pandemiyle nasıl *kalıcı olarak* değiştiğini (ikame etkisi, davranışsal kırılmalar) ortaya koyar.

## Kullanılan Teknolojiler

* **Python 3.x**
* **Pandas:** Veri işleme, temizleme, analiz ve raporlama için ana kütüphane.

## Nasıl Kullanılır?

1.  **Sanal Ortamı Kurun:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

2.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Not: `requirements.txt` dosyanız yoksa `pip freeze > requirements.txt` komutuyla oluşturabilir veya manuel olarak `pip install pandas` yapabilirsiniz.)*

3.  **Veriyi İndirin:**
    * TCMB EVDS sitesine gidin.
    * 2018-01-01'den günümüze, haftalık frekansta, istediğiniz tüm `TP.KKHARTUT...` serilerini seçin.
    * Veriyi **CSV** formatında indirin.
    * İndirdiğiniz dosyanın adını `veri.csv` olarak değiştirin ve `/data` klasörünün içine taşıyın.

4.  **Ana Raporları Çalıştırın:**
    ```powershell
    .\.venv\Scripts\python.exe main.py
    ```
    *(Bu komut, `output/` klasöründeki ilk 6 raporu oluşturur.)*

5.  **İleri Analizleri Çalıştırın:**
    ```powerssh
    # Anomali Raporunu oluşturmak için:
    .\.venv\Scripts\python.exe anomali_analizi.py
    
    # Korelasyon Raporlarını oluşturmak için:
    .\.venv\Scripts\python.exe korelasyon_analizi.py
    ```

6.  **Sonuçları İnceleyin:**
    Tüm 8+ analitik raporunuz `output/` klasöründe hazır olacaktır.
