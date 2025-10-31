# tcmb_analyzer.py
import pandas as pd
import os

class TCMBKrediKartiAnalizoru:
    """
    'data/veri.csv' dosyasını okuyan, HAFTALIK, AYLIK raporlar üreten
    ve BÜYÜME İSTATİSTİKLERİ çıkaran sınıf.
    (Versiyon 7 - Aylık Paylar Raporu Eklendi)
    """
    
    def __init__(self, input_file, output_dir="output"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.data_ham = None      # Ham veriyi tutar
        self.data_islenmis = None # İşlenmiş haftalık veriyi tutar
        self.data_aylik = None    # İşlenmiş aylık veriyi tutar
        self.sektor_sutunlari = [] # Tespit edilen sektör sütunlarını tutar
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _veriyi_dosyadan_oku(self):
        """
        'data/veri.csv' dosyasını dinamik olarak okur.
        """
        print(f"'{self.input_file}' dosyası okunuyor...")
        try:
            # 1. Başlıkları 6. satırdan oku
            header_row = pd.read_csv(
                self.input_file, header=None, skiprows=5, nrows=1,
                encoding='ISO-8859-9', delimiter=','
            ).iloc[0]
            
            # 2. Veriyi 7. satırdan itibaren oku
            self.data_ham = pd.read_csv(
                self.input_file, header=None, skiprows=6,
                encoding='ISO-8859-9', delimiter=',', na_values=['-', '...']
            )
            
            # 3. Sütun haritasını dinamik oluştur
            sutun_haritasi = {0: 'Tarih', 1: 'Yil'} 
            for i, header_name in enumerate(header_row):
                sutun_haritasi[i + 2] = str(header_name).strip()
                
            self.data_ham.rename(columns=sutun_haritasi, inplace=True)
            return True
            
        except FileNotFoundError:
            print(f"HATA: '{self.input_file}' dosyası bulunamadı.")
            return False
        except Exception as e:
            print(f"CSV okuma hatası: {e}")
            return False

    def _veri_isle(self):
        """
        Ham veriyi işler ve analiz için hazırlar.
        """
        if self.data_ham is None: return False
        print("Veriler işleniyor...")
        
        try:
            self.sektor_sutunlari = [col for col in self.data_ham.columns if str(col).startswith('TP_')]
            if not self.sektor_sutunlari:
                print("HATA: 'TP_' ile başlayan hiçbir sektör sütunu bulunamadı.")
                return False
            print(f"Tespit edilen {len(self.sektor_sutunlari)} adet sektör verisi işlenecek.")
            
            self.data_islenmis = self.data_ham[['Tarih'] + self.sektor_sutunlari].copy()
            
            self.data_islenmis['Tarih'] = pd.to_datetime(self.data_islenmis['Tarih'], dayfirst=True, errors='coerce')
            self.data_islenmis.dropna(subset=['Tarih'], inplace=True)
            self.data_islenmis.set_index('Tarih', inplace=True)
            
            for col in self.sektor_sutunlari:
                self.data_islenmis[col] = pd.to_numeric(self.data_islenmis[col], errors='coerce')
            
            self.data_islenmis.fillna(0, inplace=True)
            print("Veri işleme tamamlandı.")
            return True
        except Exception as e:
            print(f"Veri işleme sırasında hata: {e}")
            return False

    # --- HAFTALIK RAPORLAR ---

    def rapor_haftalik_toplamlar(self):
        if self.data_islenmis is None: return
        print("Rapor 1: Haftalık toplamlar oluşturuluyor...")
        haftalik_toplamlar = self.data_islenmis.copy()
        haftalik_toplamlar['Haftalik_Toplam_Harcama'] = haftalik_toplamlar.sum(axis=1)
        kayit_yolu = os.path.join(self.output_dir, "rapor_haftalik_toplamlar.csv")
        haftalik_toplamlar.to_csv(kayit_yolu, encoding='utf-8-sig')
        print(f"Rapor kaydedildi: {kayit_yolu}")

    def rapor_haftalik_paylar(self):
        if self.data_islenmis is None: return
        print("Rapor 2: Haftalık paylar oluşturuluyor...")
        haftalik_veriler = self.data_islenmis.copy()
        toplam_harcama_haftalik = haftalik_veriler.sum(axis=1)
        toplam_harcama_haftalik[toplam_harcama_haftalik == 0] = pd.NA
        haftalik_paylar = haftalik_veriler.div(toplam_harcama_haftalik, axis=0) * 100
        haftalik_paylar = haftalik_paylar.round(2)
        kayit_yolu = os.path.join(self.output_dir, "rapor_haftalik_paylar.csv")
        haftalik_paylar.to_csv(kayit_yolu, encoding='utf-8-sig')
        print(f"Rapor kaydedildi: {kayit_yolu}")

    def rapor_yillik_buyume_haftalik(self):
        if self.data_islenmis is None: return
        print("Rapor 3: Haftalık yıllık büyüme oranları oluşturuluyor...")
        yillik_degisim = self.data_islenmis.pct_change(periods=52) * 100
        yillik_degisim_rapor = yillik_degisim.dropna()
        kayit_yolu = os.path.join(self.output_dir, "rapor_haftalik_yillik_buyume.csv")
        yillik_degisim_rapor.to_csv(kayit_yolu, encoding='utf-8-sig')
        print(f"Rapor kaydedildi: {kayit_yolu}")

    # --- AYLIK VE İSTATİSTİK RAPORLARI ---

    def rapor_aylik_toplamlar_olustur(self):
        """
        (RAPOR 4) Haftalık veriyi aylık toplamlara çevirir ve kaydeder.
        """
        if self.data_islenmis is None: return False
        print("Rapor 4: Aylık toplamlar oluşturuluyor...")
        
        aylik_toplamlar = self.data_islenmis.resample('ME').sum()
        aylik_toplamlar = aylik_toplamlar.loc[aylik_toplamlar.sum(axis=1) > 0]
        aylik_toplamlar['Aylik_Toplam_Harcama'] = aylik_toplamlar.sum(axis=1)
        
        kayit_yolu = os.path.join(self.output_dir, "rapor_aylik_toplamlar.csv")
        aylik_toplamlar.to_csv(kayit_yolu, encoding='utf-8-sig')
        print(f"Rapor kaydedildi: {kayit_yolu}")
        
        self.data_aylik = aylik_toplamlar 
        return True

    def rapor_buyume_istatistikleri(self):
        """
        (RAPOR 5) Aylık veriden genel büyüme istatistiklerini hesaplar.
        """
        if self.data_aylik is None: 
            print("İstatistik raporu için önce aylık verinin oluşturulması gerekiyor.")
            return

        print("Rapor 5: Büyüme istatistikleri oluşturuluyor...")
        
        aylik_sektor_verisi = self.data_aylik[self.sektor_sutunlari]
        ilk_ay_verisi = aylik_sektor_verisi.iloc[0]
        son_ay_verisi = aylik_sektor_verisi.iloc[-1]
        ilk_ay_verisi_safe = ilk_ay_verisi.replace(0, pd.NA)
        
        mutlak_artis = son_ay_verisi - ilk_ay_verisi
        yuzdesel_artis = ((son_ay_verisi - ilk_ay_verisi_safe) / ilk_ay_verisi_safe) * 100
        volatilite = (aylik_sektor_verisi.std() / aylik_sektor_verisi.mean()).round(3)
        
        analiz_df = pd.DataFrame({
            'Ilk_Ay_Tutar (2018)': ilk_ay_verisi,
            'Son_Ay_Tutar (2025)': son_ay_verisi,
            'Mutlak_Artis (Bin TL)': mutlak_artis,
            'Yuzdesel_Artis (%)': yuzdesel_artis.round(2),
            'Volatilite_Index (Dalgalanma)': volatilite
        })
        analiz_df.index.name = 'Sektor_Kodu'
        
        kayit_yolu = os.path.join(self.output_dir, "rapor_buyume_istatistikleri.csv")
        analiz_df.to_csv(kayit_yolu, encoding='utf-8-sig')
        print(f"Rapor kaydedildi: {kayit_yolu}")
        
    def rapor_aylik_paylar(self):
        """
        (YENİ RAPOR 6) Aylık toplam harcamalar içindeki sektörel payları hesaplar.
        """
        if self.data_aylik is None: 
            print("Aylık pay raporu için önce aylık verinin oluşturulması gerekiyor.")
            return

        print("Rapor 6: Aylık sektörel paylar oluşturuluyor...")
        
        # Sadece sektör verilerini al
        aylik_sektor_verileri = self.data_aylik[self.sektor_sutunlari].copy()
        # Aylık toplam harcamayı al
        aylik_toplam_harcama = self.data_aylik['Aylik_Toplam_Harcama']
        
        # Her bir sektörü, o ayın toplam harcamasına böl
        aylik_paylar = aylik_sektor_verileri.div(aylik_toplam_harcama, axis=0) * 100
        aylik_paylar = aylik_paylar.round(2) # Yüzdeleri yuvarla
        
        kayit_yolu = os.path.join(self.output_dir, "rapor_aylik_paylar.csv")
        aylik_paylar.to_csv(kayit_yolu, encoding='utf-8-sig')
        print(f"Rapor kaydedildi: {kayit_yolu}")


    def calistir(self):
        """ 
        Tüm analiz sürecini başlatan ana metot. 
        """
        if self._veriyi_dosyadan_oku():
            if self._veri_isle():
                # 1. Önce Aylık raporları oluştur (diğerleri buna bağlı)
                if self.rapor_aylik_toplamlar_olustur():
                    # 2. Aylık veriden istatistikleri ve YENİ AYLIK PAYLARI hesapla
                    self.rapor_buyume_istatistikleri()
                    self.rapor_aylik_paylar() # <-- YENİ EKLENEN ÇAĞRI
                
                # 3. Haftalık raporları da oluştur
                self.rapor_haftalik_toplamlar()
                self.rapor_haftalik_paylar()
                self.rapor_yillik_buyume_haftalik()
                
                print(f"\nAnaliz tamamlandı. 6 Rapor '{self.output_dir}' klasörüne kaydedildi.")