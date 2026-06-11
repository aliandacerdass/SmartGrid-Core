# ⚡ SmartGrid-Core: Öncelik Tabanlı Çok Kaynaklı Dinamik Enerji Dağıtım Algoritması

Bu proje, yenilenebilir enerji kaynaklarından (rüzgar, güneş, batarya vb.) gelen anlık dalgalı enerji miktarını, bir şehir şebkesindeki tüketicilere (hastane, acil durum istasyonları, evler, sanayi bölgeleri) en adil ve kesintisiz şekilde dağıtan **akıllı şebeke dengeleme (balancing) ve kaynak optimizasyon** simülatörüdür.

Proje, hem gelişmiş bir **Terminal (CLI) Simülatörü** hem de Siemens/Tesla Grid panellerinden esinlenen modern bir **Endüstriyel SCADA Web Dashboard** arayüzü sunar.

---

## 🎓 Akademik Altyapı ve Algoritmik Analiz

Bu proje, bilgisayar bilimlerindeki en temel kaynak tahsisi (Resource Allocation) ve optimizasyon problemlerini çözmek amacıyla tasarlanmıştır. Sunum esnasında savunulabilecek teknik detaylar şunlardır:

### 1. Veri Tabanı Katmanı: Hash Map [$O(1)$ Zaman Karmaşıklığı]
* Şebekedeki tüm abonelerin anlık durumları ve telemetri verileri bellekte bir **Hash Map (Python Dictionary / JS Object)** üzerinde tutulur.
* Bu sayede yeni abone ekleme, silme, sorgulama ve talep güncellemeleri eleman sayısından bağımsız olarak her zaman sabit zaman alan **$O(1)$** maliyetle gerçekleştirilir.

### 2. Sıralama ve Dağıtım Katmanı: Priority Queue [$O(N \log N)$ Zaman Karmaşıklığı]
* Kaynak tahsisi yapılmadan önce aboneler anlık olarak bir **Min-Heap / Priority Queue** (Python'da `heapq`) yapısına eklenir.
* Sıralama anahtarı şudur: `(Öncelik Derecesi, İletim Mesafesi, Abone Adı)`
  * **Birincil Öncelik:** Kritiklik (1: Hastane/Acil Durum, 2: Konut, 3: Sanayi).
  * **İkincil Öncelik (Greedy Choice):** Fiziksel mesafe (aynı öncelik grubunda kaynağa en yakın olan önce beslenir).

### 3. Çok Kaynaklı Dengeleme (Multi-Source Greedy Allocation)
* Şebekeye birden fazla jeneratör eklenebilir. Her jeneratörün konumu ($X, Y$ koordinatları) ve anlık üretim gücü (MW) dinamiktir.
* Her abone, **Greedy** yaklaşımla kendisine *en yakın olan ve boş kapasitesi bulunan* jeneratörden beslenir. İletim hattındaki güç kaybı, ekrandaki Öklid mesafesi üzerinden dinamik hesaplanır. Jeneratör aboneye yaklaştıkça hat kaybı düşer ve verimlilik artar.

---

## 📁 Proje Yapısı

* **[smart_grid.py](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/smart_grid.py)**: Dengeleme algoritmasının ve veritabanı işlemlerinin Python üzerindeki çekirdek kütüphanesi.
* **[main.py](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/main.py)**: Terminal (CLI) üzerinde çalışan, loading animasyonlu, topoloji grafiği çizen etkileşimli simülatör.
* **[dashboard.html](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/dashboard.html)**: Tarayıcıda doğrudan açılabilen, dinamik sürgülü ve sayı girdili, SVG animasyonlu SCADA kontrol paneli.
* **[test_smart_grid.py](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/test_smart_grid.py)**: Algoritmanın ve Hash Map işlemlerinin doğruluğunu test eden unittest modülü.
* **[presentation_guide.md](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/presentation_guide.md)**: Slayt şablonları ve hocadan gelebilecek jüri sorularının cevaplarını içeren sunum rehberi.
* **[project_memory.md](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/project_memory.md)**: Proje geliştirme aşamalarını ve Change Log geçmişini tutan hafıza dosyası.
* **[gorev_dagilimi.md](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/gorev_dagilimi.md)**: Proje ekibinin görev dağılımını ve iş paketleri sorumluluklarını belgeleyen dosya.

---

## 🚀 Kurulum ve Çalıştırma

Proje harici hiçbir kütüphane bağımlılığı (dependency) gerektirmez. Python standart kütüphaneleriyle sıfır kurulumla anında çalışır.

### 1. Terminal (CLI) Arayüzünü Çalıştırma
Terminalde proje dizinine gidin ve şu komutu çalıştırın:
```bash
python3 main.py
```
*Açılan menüde hazır senaryoları çalıştırabilir, abone ekleyip silebilir ve hocaya sunabileceğiniz teorik açıklama ekranını görüntüleyebilirsiniz.*

### 2. SCADA Web Dashboard Arayüzünü Açma
Tarayıcınızda (Chrome, Safari, Firefox vb.) **`dashboard.html`** dosyasını doğrudan açmanız yeterlidir:
* Jeneratörlerin Güç, X ve Y sürgülerini kaydırabilir veya yanındaki sayı kutularına tıklayıp doğrudan yeni değerler yazabilirsiniz.
* Değerleri değiştirdiğinizde SVG topolojisindeki akış çizgilerinin yönü ve kalınlığı anlık olarak 60 FPS akıcılıkla güncellenir.
* Yeni jeneratörler veya aboneler ekleyerek şebekenin kriz anındaki kararlarını izleyebilirsiniz.

### 3. Birim Testlerini Çalıştırma (Unittest)
Projedeki algoritmaların doğruluğunu kanıtlamak için testleri şu komutla koşturabilirsiniz:
```bash
python3 -m unittest test_smart_grid.py
```

---

## 📈 Örnek Simülasyon Senaryoları

* **Senaryo 1 (Yüksek Üretim - Güneşli Gün):** Şebekeye 100 MW+ güç verilir. Algoritma çalışır, tüm aboneler tam beslenir (`Besleniyor %100`), şebeke verimliliği en üst düzeye çıkar.
* **Senaryo 2 (Düşük Üretim - Gece / Rüzgarsız Gün):** Güç girdisi 30 MW'a düşürülür. Öncelik kuyruğu devreye girerek sanayi ve evlerin enerjisini keser, kısıtlı gücü doğrudan kritik konumdaki Hastane ve Acil Durum İstasyonuna yönlendirir.

---

---

## 👥 Ekip Üyeleri (Team Members)

Bu proje, aşağıdaki ekip üyeleri tarafından ortaklaşa geliştirilmiştir:
1. **Andaç** (Proje Koordinatörü & Algoritma Tasarımcısı)
2. **Seda** (Arayüz Geliştirici & UI/UX Tasarımcısı)
3. **Ayberk** (Frontend Mantığı & Optimizasyon)
4. **Enes** (CLI Uygulaması & Teknik Yazar)

Detaylı iş paketleri, modül bazlı kod sorumlulukları ve iş zaman çizelgesi şeması için **[gorev_dagilimi.md](file:///Users/aliandacerdass/GitHubRepos/SmartGrid-Core/gorev_dagilimi.md)** belgesini inceleyebilirsiniz.

---

## 📝 Lisans

Bu proje akademik kullanım ve eğitim amaçlı MIT Lisansı ile korunmaktadır.

