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
| **Aşama 6** | Canlı İnteraktif Web Görselleştirme Arayüzü (`dashboard.html`) | 🟢 Tamamlandı |
| **Aşama 7** | Çoklu Jeneratör & Konumsal Kayıp Simülasyon Arayüzü (`dashboard.html`) | 🟢 Tamamlandı |

*Durum Göstergeleri: 🔴 Planlandı | 🟡 Devam Ediyor | 🟢 Tamamlandı*

---

## 🪵 Değişiklik Günlüğü (Change Log)

### [2026-06-08] - Cetvel Konumlandırma İyileştirmesi
- **Görsel İyileştirme:** Koordinat cetvellerinin (ruler) şebeke çizim alanını kısıtlamaması için konumları kenarlara çekildi.
  - Üst cetvel (X-Axis) Y = 10'dan Y = 3'e taşındı, yazıları çentiklerin altına (Y=13) hizalandı.
  - Sağ cetvel (Y-Axis) X = 790'dan X = 797'ye taşındı, yazıları sol tarafa (X=789) hizalandı.
  - Bu sayede jeneratör ve aboneler en üst ve en sağ sınırlara sürüklendiğinde, etiket ve kutular cetvellerle üst üste binmeyecek şekilde şebeke alanı ferahlatıldı.

### [2026-06-08] - Çoklu Jeneratör ve Uzamsal Simülasyon Güncellemesi
- **Geliştirme:** Şebekede tek enerji kaynağı yerine birden fazla jeneratör (💨 Rüzgar, ☀️ Güneş, 🔋 Batarya vb.) desteği eklendi.
- **Algoritmik Geliştirme:** Çok Kaynaklı Dengeleme Algoritması entegre edildi. Her abone en yüksek öncelikten başlayarak kendisine **en yakın (Euclidean distance)** ve boş kapasitesi olan jeneratör(ler)den beslenir.
- **Geliştirme (UI):** Jeneratörlerin kapasitelerini, X ve Y koordinatlarını anlık değiştirebileceğiniz sürgüler (sliders) eklendi. Jeneratörlerin konumları değiştikçe iletim hatları otomatik olarak hareket eder ve iletim hatlarındaki fiziksel mesafe kayıpları anlık yeniden hesaplanır.
- **Performans Optimizasyonu & Yeni Özellik:** Jeneratör sürgüleri kaydırılırken listedeki DOM elemanlarının sürekli baştan yaratılmasından ötürü oluşan tıkanma ve kasma (stuttering) sorunu giderildi. Arayüzün yeniden çizilme (rendering) mantığı güncellenerek değer güncellemeleri doğrudan in-place (yerinde) yapıldı ve sürgüler 60 FPS akıcılığa kavuşturuldu. Ayrıca her sürgünün yanına, kullanıcının tıklayıp doğrudan jeneratör değerlerini (Güç, X, Y) elle yazarak değiştirebileceği sayısal girdi kutuları (Numeric Inputs) entegre edildi.
- **Dinamik SVG Ölçekleme & Sınır Hizalama:** Şebekedeki jeneratör ve abone sayısı arttıkça SVG topoloji grafiğindeki simgelerin boyutlarını küçülten, azaldıkça ise büyüten (varsayılan olarak %30 daha büyük) dinamik bir ölçek çarpanı (Dynamic Scale Factor) eklendi. Ayrıca iletim hatlarının çizgilerinin ve ok işaretlerinin, düğüm yuvarlaklarının tam sınırında son bulmasını sağlayan vektörel hizalama matematiği uygulandı.
- **Mühendislik Cetvelleri (Coordinate Rulers):** Şebeke akış diyagramının üst sınırına X-ekseni (100-700 arası, 50'şer birimlik çentiklerle) ve sağ sınırına Y-ekseni (50-350 arası, 50'şer birimlik çentiklerle) CAD tarzı ince koordinat cetvelleri eklendi. Bu cetveller görsel şemayı kesmeden, yanlarda kılavuz görevi üstlenerek jeneratör ve abone konumlandırmasını kolaylaştırır.
- **Dokümantasyon Güncellemesi:** Projenin GitHub üzerindeki ana sayfası olan `README.md` dosyası sıfırdan yazılarak zenginleştirildi; algoritmik karmaşıklık analizleri, proje yapısı ve çalıştırma adımları profesyonel standartlarda belgelendi.
- **Değişiklik:** `project_memory.md` güncellendi ve yeni aşama tamamlandı olarak işaretlendi.

### [2026-06-08] - Görselleştirme ve Animasyon Güncellemesi
- **Geliştirme:** `main.py` terminal arayüzüne yükleme animasyonları (spinning loader), uyarı titreşim efektleri (pulse warning) ve dinamik olarak güncellenen ASCII topoloji grafiği (düğümler ve iletim yolları) eklendi.
- **Geliştirme:** `dashboard.html` etkileşimli web görselleştirme arayüzü sıfırdan inşa edildi.
- **Görsel Tasarım Güncellemesi (SCADA):** Kullanıcının talebiyle "yapay zeka / bilimkurgu" teması tamamen kaldırılarak, Siemens ve Tesla Utility panellerinden esinlenilen profesyonel bir **Endüstriyel SCADA / Enerji Kontrol Merkezi** tasarımı uygulandı. Degrade/neon mor renkler yerine mat gri/grafit tonlar, ince kontrol sınırları, teknik CAD ızgarası (grid blueprint) ve sade göstergeler entegre edildi.
- **Geliştirme (Yeni):** `dashboard.html` dosyasına doğrudan toplam enerji girdisini elle yazarak değiştirebileceğiniz bir sayısal girdi alanı (Numeric Input) eklendi ve slider ile senkronize edildi. Ayrıca abone eklerken emoji simgesi seçmeyi sağlayan "İkon/Simge Seçici" özelliği getirildi.
- **Hata Giderimi:** Şebeke topoloji grafiğindeki düğümlerin farklı ekran çözünürlüklerinde yana kayarak kesilmesi problemi giderildi. SVG elementine responsive `viewBox="0 0 800 400"` ve `preserveAspectRatio` tanımlandı; düğüm koordinatları bu sanal düzleme göre mükemmel şekilde ortalandı.
- **Değişiklik:** `project_memory.md` güncellendi ve yeni aşama tamamlandı olarak işaretlendi.

### [2026-06-08] - Projenin Tamamlanması
* **Değişiklik:** Çekirdek algoritma kütüphanesi `smart_grid.py` geliştirildi. Priority Queue (min-heap) ve iletim hatlarındaki kayıpları (transmission loss) minimize eden Greedy yaklaşım entegre edildi.
* **Değişiklik:** Etkileşimli CLI arayüzü `main.py` oluşturuldu. Hazır senaryolar, dinamik abone ekleme/güncelleme/silme ve hocaya sunulmak üzere detaylı akademik açıklama ekranı eklendi.
* **Değişiklik:** Birim test modülü `test_smart_grid.py` yazıldı, O(1) Hash Map işlemleri ve öncelikli/kısıtlı dağıtım kararları otomatik test edildi ve tüm testler başarıyla geçti.
* **Değişiklik:** `presentation_guide.md` sunum ve akademik savunma rehberi oluşturuldu. Olası jüri soruları ve cevapları detaylandırıldı.
* **Değişiklik:** `project_memory.md` güncellenerek tüm aşamaların tamamlandığı işaretlendi.
