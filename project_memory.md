# Project Memory - SmartGrid-Core

Bu dosya, **SmartGrid-Core: Öncelik Tabanlı Dinamik Enerji Dağıtım Algoritması** projesinin gelişimini, alınan kararları, teknik altyapıyı ve güncel durumunu takip etmek amacıyla oluşturulmuştur. Her dosya değişikliğinde güncellenecektir.

---

## 🚀 Proje Bilgileri
* **Proje Adı:** SmartGrid-Core: Öncelik Tabanlı Dinamik Enerji Dağıtım Algoritması
* **Ders:** Algoritmalar Analizi / Veri Yapıları
* **Konu:** Akıllı Enerji Şebekesi (Smart Grid) Balancing ve Dağıtım Ünitesi (Yenilenebilir kaynaklardan gelen elektriğin en az kayıpla ve dengeli dağıtılması)
* **Temel Amaç:** Dalgalı yenilenebilir enerji girdilerini (rüzgar/güneş), öncelikli tüketim noktalarına (hastane, ev, sanayi vb.) en adil ve kesintisiz şekilde dağıtmak, bu kararları anlık veri analizi ile hızlıca almak.

---

## 🛠️ Teknik Altyapı ve Veri Yapıları

### 1. Veri Tabanı Katmanı (Hash Map)
* **Veri Yapısı:** Python `dict` (Hash-Map) yapısı kullanılmaktadır.
* **Performans:** Arama ve güncelleme maliyeti $O(1)$'dir.
* **Depolanan Bilgiler:**
  * `Abone Adı` (Key) -> `{"oncelik": int, "talep": float, "durum": str, "saglanan_enerji": float}`

### 2. Dağıtım ve Optimizasyon Katmanı (Greedy + Priority Queue)
* **Öncelik Kuyruğu (Priority Queue):** Enerji dağıtımı yapılmadan önce aboneler öncelik derecesine göre sıralanır (Öncelik 1: Kritik, 2: Normal, 3: Düşük).
* **Açgözlü Yaklaşım (Greedy Approach):** Elimizdeki kısıtlı kaynağı (enerji), en yüksek öncelikli aboneden başlayarak talebini tam karşılayacak şekilde dağıtırız.
* **Kayıp Hesaplama (Loss Calculation):** Enerji dağıtımında basit şebeke hattı kayıpları simüle edilecek veya mesafe/direnç faktörüyle en verimli yollar seçilecektir.

### 3. Kullanıcı Arayüzü (CLI)
* Terminal üzerinden çalışan, renkli, emoji destekli ve etkileşimli bir simülasyon arayüzü.
* **Hazır Senaryolar:**
  * **Senaryo 1 (Yüksek Üretim):** Enerji fazlası durumunda tüm abonelerin tam beslenmesi.
  * **Senaryo 2 (Düşük Üretim):** Kritik (Hastane) öncelikli beslenirken, alt kategorilerin (Sanayi, Ev) kesilmesi veya kısıtlanması.
  * **Dinamik Senaryo:** Kullanıcının elle enerji girişi yapabildiği, yeni aboneler ekleyebildiği veya mevcut abonelerin durumunu değiştirebildiği interaktif mod.

---

## 📋 Yol Haritası ve Durum Tablosu

| Aşama | Görev Açıklaması | Durum |
| :--- | :--- | :--- |
| **Aşama 1** | Proje Hafızası (`project_memory.md`) Oluşturulması | 🟢 Tamamlandı |
| **Aşama 2** | Çekirdek Dağıtım Algoritması & Veri Yapısı Tasarımı (`smart_grid.py`) | 🟢 Tamamlandı |
| **Aşama 3** | CLI Simülasyon Arayüzü Geliştirilmesi (`main.py`) | 🟢 Tamamlandı |
| **Aşama 4** | Birim Testleri & Doğrulama (`test_smart_grid.py`) | 🟢 Tamamlandı |
| **Aşama 5** | Sunum Taslağı ve Akademik Savunma Rehberi (`presentation_guide.md`) | 🟢 Tamamlandı |

*Durum Göstergeleri: 🔴 Planlandı | 🟡 Devam Ediyor | 🟢 Tamamlandı*

---

## 🪵 Değişiklik Günlüğü (Change Log)

### [2026-06-08] - Projenin Tamamlanması
* **Değişiklik:** Çekirdek algoritma kütüphanesi `smart_grid.py` geliştirildi. Priority Queue (min-heap) ve iletim hatlarındaki kayıpları (transmission loss) minimize eden Greedy yaklaşım entegre edildi.
* **Değişiklik:** Etkileşimli CLI arayüzü `main.py` oluşturuldu. Hazır senaryolar, dinamik abone ekleme/güncelleme/silme ve hocaya sunulmak üzere detaylı akademik açıklama ekranı eklendi.
* **Değişiklik:** Birim test modülü `test_smart_grid.py` yazıldı, O(1) Hash Map işlemleri ve öncelikli/kısıtlı dağıtım kararları otomatik test edildi ve tüm testler başarıyla geçti.
* **Değişiklik:** `presentation_guide.md` sunum ve akademik savunma rehberi oluşturuldu. Olası jüri soruları ve cevapları detaylandırıldı.
* **Değişiklik:** `project_memory.md` güncellenerek tüm aşamaların tamamlandığı işaretlendi.
