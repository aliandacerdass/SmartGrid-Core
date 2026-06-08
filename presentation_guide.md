# Sunum ve Akademik Savunma Rehberi 🎓

Bu rehber, **SmartGrid-Core** projesini ders kapsamında hocaya sunarken ve projeyi savunurken kullanabileceğin slayt taslaklarını, konuşma metinlerini ve gelebilecek olası sorulara karşı hazır cevapları içerir.

---

## 📽️ Slayt-by-Slayt Sunum Planı

### Slayt 1: Giriş ve Proje Tanımı
* **Başlık:** SmartGrid-Core: Öncelik Tabanlı Dinamik Enerji Dağıtım Algoritması
* **Alt Başlık:** Yenilenebilir Enerji Şebekelerinde Kaynak Optimizasyonu ve Dağıtım Ünitesi Simülasyonu
* **Görsel/Şema:** Güneş paneli ve rüzgar gülünden şehre giden enerji hatlarını temsil eden basit bir ikon/diyagram.
* **Ne Söyleyeceksin?**
  > "Hocam merhaba. Projemizin adı SmartGrid-Core. Temel amacımız, rüzgar ve güneş gibi yenilenebilir enerji kaynaklarından gelen dalgalı ve kararsız enerjiyi, şehirdeki abonelere en yüksek verimlilikle (minimum iletim kaybı) ve adil bir önceliklendirme sırasıyla dağıtan dinamik bir simülasyon yapmaktır."

### Slayt 2: Problem Tanımı (Neden Bu Konu?)
* **Başlık:** Şebeke Dengeleme (Balancing) Problemi
* **Maddeler:**
  * Yenilenebilir kaynakların kararsızlığı (güneş batınca veya rüzgar durunca üretimin düşmesi).
  * Enerjinin üretildiği an tüketilmesi gerekliliği.
  * Kritik kurumların (Hastaneler, Acil Durum Merkezleri) kesintisiz enerji ihtiyacı.
  * Kablo mesafelerinden kaynaklanan fiziksel güç kayıpları.
* **Ne Söyleyeceksin?**
  > "Geleneksel şebekelerde üretim sabittir. Ancak yeşil enerjide hava durumuna göre üretim anlık dalgalanır. Eğer bulut gelirse üretim 100 MW'tan 30 MW'a düşebilir. Bu durumda tüm şehre elektrik vermeye çalışırsak sistem çöker (Blackout). Bizim yazılımımız, kısıtlı kaynağı akıllıca yöneterek kritik yerleri korur ve iletim hatlarındaki kayıpları optimize eder."

### Slayt 3: Algoritmik Altyapı ve Veri Yapıları
* **Başlık:** O(1) Hash Map & Priority Queue Uyumlaşması
* **Maddeler:**
  * **Anlık Durum Veri Tabanı:** Veri erişimi ve güncellemeler için **Hash Map (Dictionary)** -> Zaman Karmaşıklığı: $O(1)$.
  * **Öncelik Kuyruğu:** Kritiklik derecesine göre aboneleri dizmek için **Priority Queue (Min-Heap / heapq)** -> Zaman Karmaşıklığı: $O(N \log N)$.
  * **Karar Mekanizması:** Açgözlü Yaklaşım (Greedy Algorithm).
* **Ne Söyleyeceksin?**
  > "Hocam, projemizde gerçek zamanlı bir akıllı şebekeyi simüle etmek için veri yapılarının performansına odaklandık. Abone bilgilerini aramak, silmek veya anlık taleplerini güncellemek için Hash Map kullandık; böylece bu işlemler $O(1)$ sürede tamamlanıyor. Enerji dağıtım anında ise aboneleri önem derecesine göre öncelik kuyruğuna (Priority Queue) alıyoruz. Kuyruktan en kritik aboneyi $O(\log N)$ sürede çekip enerjiyi dağıtıyoruz."

### Slayt 4: Kayıp Optimizasyonu ve Greedy Seçim
* **Başlık:** En Az Kayıpla Dağıtım (Greedy Choice)
* **Maddeler:**
  * Hat direnç kaybı formülü: $Kayıp = Talep \times (Mesafe \times 0.01)$
  * Aynı öncelik grubundaki (örn. evler) aboneler arasında mesafesi en kısa olana öncelik verilmesi.
  * Bu sayede toplam iletim kaybının minimize edilmesi.
* **Ne Söyleyeceksin?**
  > "Algoritmamız sadece önceliğe bakmıyor; aynı zamanda enerji kaybını da azaltıyor. Eğer iki mahallenin de önceliği aynıysa, kaynağa daha yakın olan aboneye öncelik veriyoruz. Çünkü uzak aboneye elektrik göndermek hatlardaki direnç nedeniyle daha fazla kayba yol açacaktır. Bu yaklaşım, bilgisayar bilimlerindeki klasik Açgözlü (Greedy) yaklaşımın tam bir uygulamasıdır."

### Slayt 5: Canlı Demo ve Senaryolar
* **Başlık:** CLI Simülasyon Ekranı
* **İçerik:**
  * Senaryo 1: Bol Enerji (100 MW+) -> Herkes besleniyor, şebeke stabil.
  * Senaryo 2: Kritik Kısıt (30 MW) -> Sanayi ve evler kesildi, hastane beslendi.
  * Dinamik Abone ve Talep yönetimi.
* **Ne Söyleyeceksin?**
  > "Şimdi sistemi canlı olarak terminal üzerinde çalıştıralım. Varsayılan olarak şebekemizde hastaneler, evler ve sanayi bölgeleri tanımlı. Yüksek üretim senaryosunda 100 MW enerji verdiğimizde herkesin beslendiğini görüyoruz. Ancak gece olup rüzgar durduğunda sisteme 30 MW girdiğimizde, öncelik kuyruğu devreye giriyor; sanayi ve evlerin elektriğini keserek eldeki kısıtlı gücü sadece hastaneye yönlendiriyor."

---

## 💬 Hocadan Gelebilecek Zor Sorular ve Cevapları

### Soru 1: "Neden veri tabanı için SQL yerine Hash Map (Dictionary) kullandınız?"
* **Cevap:**
  > "Hocam, gerçek zamanlı Smart Grid sistemlerinde milisaniyeler bile önemlidir. Disk tabanlı SQL sorguları gecikmeye (I/O latency) sebep olur. Biz bu simülasyonda veriyi bellekte (in-memory) tuttuk. Arama, güncelleme ve erişim maliyetini teorik olarak en hızlı seviye olan $O(1)$ yani sabit zamanda gerçekleştirmek için Hash Map yapısını tercih ettik."

### Soru 2: "Priority Queue kullanmak yerine sadece standart sort (sıralama) kullansak olmaz mıydı? Ne farkı var?"
* **Cevap:**
  > "Eğer tüm listeyi her seferinde yeniden sıralasaydık (örneğin Timsort kullanarak) ortalama $O(N \log N)$ işlem yapardık ve tüm listeyi sıralı tutmak zorunda kalırdık. Oysa Priority Queue (Heap) kullanarak dinamik olarak en yüksek öncelikli elemanı $O(\log N)$ sürede çekebiliyoruz. Özellikle şebekeye sürekli yeni abonelerin anlık girip çıktığı dinamik sistemlerde Heap veri yapısı bellek ve işlemci açısından çok daha verimlidir."

### Soru 3: "Buradaki Greedy (Açgözlü) yaklaşımın zayıf yönü nedir? Kesin optimizasyon (Global Optimum) sağlar mı?"
* **Cevap:**
  > "Greedy yaklaşım o anki en iyi seçimi (en yüksek öncelik ve en yakın mesafe) seçer. Çoğu durumda şebeke güvenliği için bu lokal kararlar doğrudur. Ancak Knapsack probleminde olduğu gibi, bazen kısıtlı enerjiyi tam ucu ucuna bölüştürerek toplam memnuniyeti artırmak için Dinamik Programlama (Dynamic Programming) veya Genetik Algoritmalar gerekebilir. Fakat gerçek zamanlı hızlı karar verme gereksinimi ve kritik kurumların kesin önceliği nedeniyle Greedy yaklaşım bu problem için en pratik ve hızlı çalışan çözümdür."

---

## 🏃‍♂️ Projeyi Çalıştırma Adımları
Projeyi hocaya sunarken terminalden şu komutla başlatabilirsin:
```bash
python3 main.py
```

Birim testlerin (Unit Tests) çalıştığını göstermek için:
```bash
python3 -m unittest test_smart_grid.py
```
Bu test çıktısı hocaya projenizin yazılım mühendisliği standartlarına uygun yazıldığını kanıtlayacaktır!
