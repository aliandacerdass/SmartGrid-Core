import os
import sys
import time
from smart_grid import SmartGrid

# ANSI Escape Sequences for terminal styling
class Styles:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    title = f"""
{Styles.BOLD}{Styles.CYAN}======================================================================
  ⚡ SmartGrid-Core: Öncelik Tabanlı Dinamik Enerji Dağıtım Algoritması ⚡
======================================================================{Styles.RESET}
    """
    print(title)

def print_subscriber_table(grid):
    """Prints subscribers stored in the O(1) Hash Map database."""
    print(f"\n{Styles.BOLD}{Styles.UNDERLINE}ŞEBEKE VERİ TABANI GÜNCEL ANLIK DURUMU (Hash-Map O(1)){Styles.RESET}")
    print("-" * 105)
    print(f"{'Abone Adı (Key)':<30} | {'Öncelik':<12} | {'Talep (MW)':<12} | {'Mesafe (km)':<12} | {'Durum':<20} | {'Kaybı (MW)':<10}")
    print("-" * 105)
    
    # Priority color mapping
    priority_map = {
        1: f"{Styles.RED}1 (Kritik){Styles.RESET}",
        2: f"{Styles.YELLOW}2 (Normal){Styles.RESET}",
        3: f"{Styles.BLUE}3 (Düşük){Styles.RESET}"
    }

    # Status color mapping
    for name, info in grid.database.items():
        priority_str = priority_map.get(info['priority'], str(info['priority']))
        status_raw = info['status']
        
        if "Besleniyor (%100)" in status_raw:
            status_str = f"{Styles.GREEN}{status_raw}{Styles.RESET}"
        elif "Kısıtlı" in status_raw:
            status_str = f"{Styles.YELLOW}{status_raw}{Styles.RESET}"
        elif "Kesildi" in status_raw or "Yok" in status_raw:
            status_str = f"{Styles.RED}{status_raw}{Styles.RESET}"
        else:
            status_str = status_raw
            
        print(f"{name:<30} | {priority_str:<21} | {info['demand']:<12.2f} | {info['distance']:<12.1f} | {status_str:<29} | {info['loss']:<10.2f}")
    print("-" * 105)

def print_distribution_summary(summary):
    """Prints the distribution simulation result statistics."""
    print(f"\n{Styles.BOLD}{Styles.GREEN}📈 Dağıtım Simülasyon Raporu:{Styles.RESET}")
    print(f"  ▪ Giriş Enerjisi (Yenilenebilir) : {Styles.BOLD}{summary['input_power']:.2f} MW{Styles.RESET}")
    print(f"  ▪ Tüketicilere Ulaşan Toplam Güç : {Styles.GREEN}{summary['total_supplied']:.2f} MW{Styles.RESET}")
    print(f"  ▪ Şebeke Hattı Kayıpları        : {Styles.RED}{summary['total_loss']:.2f} MW{Styles.RESET}")
    print(f"  ▪ Boşa Giden / Atıl Kalan Güç   : {Styles.YELLOW}{summary['waste_power']:.2f} MW{Styles.RESET}")
    
    total_needed_from_source = summary['total_supplied'] + summary['total_loss']
    if total_needed_from_source > 0:
        efficiency = (summary['total_supplied'] / total_needed_from_source) * 100
        print(f"  ▪ Şebeke Dağıtım Verimliliği   : {Styles.BOLD}{Styles.CYAN}{efficiency:.2f}%{Styles.RESET}")

def print_academic_explanation():
    clear_screen()
    print_header()
    explanation = f"""
{Styles.BOLD}{Styles.YELLOW}🎓 HOCAYA SUNUM İÇİN ALGORİTMİK AÇIKLAMA VE BİLGİSAYAR BİLİMLERİ İLİŞKİSİ{Styles.RESET}

Bu proje, bilgisayar bilimlerindeki en temel optimizasyon ve kaynak tahsisi
(Resource Allocation) problemlerini çözmek amacıyla tasarlanmıştır.

{Styles.BOLD}1. Veri Yapısı Seçimi (Hash Map / O(1) Zaman Karmaşıklığı):{Styles.RESET}
   Şebekedeki tüm aboneler bir Python Sözlüğü (Dictionary / Hash Map) üzerinde
   tutulmaktadır. Bu sayede:
   - Yeni abone ekleme, silme ve talep güncellemeleri {Styles.GREEN}O(1) (Sabit Zaman){Styles.RESET} ile yapılır.
   - Şebekede binlerce abone olsa bile arama ve veri çekme maliyeti sıfıra yakındır.

{Styles.BOLD}2. Sıralama ve Önceliklendirme (Priority Queue / heap-sort):{Styles.RESET}
   Enerji dağıtım anında, kaynakların kime verileceği kararı {Styles.CYAN}Priority Queue{Styles.RESET} mantığıyla
   yürütülür. Python'ın `heapq` modülü (min-heap) kullanılarak:
   - Aboneler önce öncelik derecesine (1: En Kritik, 3: En Düşük) göre sıralanır.
   - Aynı öncelik derecesindekiler ise {Styles.BOLD} Greedy (Açgözlü) Yaklaşımla{Styles.RESET} kaynağa en yakın
     olan (en az kablo/hat kaybına sebep olacak) mesafeye göre ikincil sıralamaya sokulur.
   - Bu kuyruk yapısı {Styles.GREEN}O(N log N){Styles.RESET} sürede inşa edilir ve işlenir.

{Styles.BOLD}3. Açgözlü Yaklaşım (Greedy Algorithm) & Enerji Dengeleme (Balancing):{Styles.RESET}
   Sınırlı yenilenebilir enerji kaynağını, en kritik aboneden başlayarak açgözlü
   (greedy) bir şekilde tam veya kısmi olarak dağıtırız. Enerji bittiği anda
   alt seviyedeki aboneler kesintiye uğrar, böylece kritik altyapılar (Hastaneler vb.)
   asla enerjisiz kalmaz.

{Styles.BOLD}4. Şebeke İletim Kayıpları Optimizasyonu (Network Loss):{Styles.RESET}
   Şebekede mesafe ile doğru orantılı bir hat direnç kaybı simüle edilmiştir. Aynı
   önceliğe sahip aboneler arasında mesafe bazlı Greedy seçim yapılması, toplam hat
   kayıplarını minimize eder.
    """
    print(explanation)
    input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")

def main():
    grid = SmartGrid()
    
    # Initial system boot display
    clear_screen()
    print_header()
    print(f"\n{Styles.BOLD}{Styles.GREEN}⚙️ SmartGrid-Core Şebeke Sistemi Başlatılıyor...{Styles.RESET}")
    time.sleep(1)
    print_subscriber_table(grid)
    print(f"\n⚡ {Styles.YELLOW}Sistem Hazır! Simülasyonu başlatmak için bir senaryo seçin.{Styles.RESET}")
    input("\nDevam etmek için Enter tuşuna basın...")

    while True:
        clear_screen()
        print_header()
        
        print(f"{Styles.BOLD}⚡ LÜTFEN BİR İŞLEM / SENARYO SEÇİN:{Styles.RESET}\n")
        print(f" [{Styles.BOLD}1{Styles.RESET}] Şebeke Durumunu Görüntüle")
        print(f" [{Styles.BOLD}2{Styles.RESET}] Senaryo 1: Yüksek Üretim (Güneşli Gün - 100 MW Güç)")
        print(f" [{Styles.BOLD}3{Styles.RESET}] Senaryo 2: Düşük Üretim (Bulutlu/Rüzgarsız Gün - 30 MW Güç)")
        print(f" [{Styles.BOLD}4{Styles.RESET}] Dinamik Senaryo: Toplam Güç Değerini Sen Belirle")
        print(f" [{Styles.BOLD}5{Styles.RESET}] Abone Yönetimi (Ekle / Güncelle / Sil)")
        print(f" [{Styles.BOLD}6{Styles.RESET}] Akademik Rapor / Projenin Algoritma Dersiyle İlişkisi")
        print(f" [{Styles.BOLD}0{Styles.RESET}] Programdan Çıkış")
        
        choice = input(f"\n👉 {Styles.BOLD}Seçiminiz: {Styles.RESET}").strip()
        
        if choice == '1':
            clear_screen()
            print_header()
            print_subscriber_table(grid)
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '2':
            clear_screen()
            print_header()
            print(f"{Styles.BOLD}{Styles.YELLOW}🌞 SENARYO 1 BAŞLATILIYOR: Yüksek Üretim (100 MW Giriş Gücü)...{Styles.RESET}\n")
            summary = grid.distribute_energy(100.0)
            print_subscriber_table(grid)
            print_distribution_summary(summary)
            print(f"\n{Styles.BOLD}{Styles.GREEN}✔️ DURUM ANALİZİ: Enerji üretimi yüksek, tüm abonelerin talepleri başarıyla karşılandı.{Styles.RESET}")
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '3':
            clear_screen()
            print_header()
            print(f"{Styles.BOLD}{Styles.YELLOW}☁️ SENARYO 2 BAŞLATILIYOR: Düşük Üretim / Gece Modu (30 MW Giriş Gücü)...{Styles.RESET}\n")
            summary = grid.distribute_energy(30.0)
            print_subscriber_table(grid)
            print_distribution_summary(summary)
            print(f"\n{Styles.BOLD}{Styles.RED}🚨 KRİZ RAPORU: Enerji yetersiz! Öncelik kuyruğu işletilerek düşük öncelikli sanayi ve normal konutların enerjisi kısıldı/kesildi. Kritik konumlar (Hastane, Acil Durum) kesintisiz beslendi.{Styles.RESET}")
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '4':
            clear_screen()
            print_header()
            print(f"{Styles.BOLD}🔋 DİNAMİK ENERJİ DAĞITIM MODU{Styles.RESET}")
            try:
                power_in = float(input("\nSisteme verilecek anlık yenilenebilir enerji miktarını girin (MW): "))
                if power_in < 0:
                    print(f"{Styles.RED}Hata: Enerji miktarı negatif olamaz.{Styles.RESET}")
                    time.sleep(1.5)
                    continue
                
                print(f"\n{Styles.YELLOW}⚡ {power_in} MW Güç Dağıtılıyor...{Styles.RESET}\n")
                summary = grid.distribute_energy(power_in)
                print_subscriber_table(grid)
                print_distribution_summary(summary)
            except ValueError:
                print(f"{Styles.RED}Hata: Lütfen geçerli bir sayısal değer girin.{Styles.RESET}")
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '5':
            while True:
                clear_screen()
                print_header()
                print(f"{Styles.BOLD}👥 ABONE YÖNETİM MENÜSÜ{Styles.RESET}\n")
                print(" [1] Yeni Abone Ekle")
                print(" [2] Abone Talebini Güncelle")
                print(" [3] Abone Sil")
                print(" [4] Geri Dön")
                
                sub_choice = input(f"\n👉 {Styles.BOLD}Seçiminiz: {Styles.RESET}").strip()
                
                if sub_choice == '1':
                    print(f"\n{Styles.BOLD}--- Yeni Abone Ekleme ---{Styles.RESET}")
                    name = input("Abone Adı: ").strip()
                    if not name:
                        print(f"{Styles.RED}Abone adı boş olamaz!{Styles.RESET}")
                        time.sleep(1.5)
                        continue
                    try:
                        priority = int(input("Öncelik Derecesi (1: Kritik, 2: Normal, 3: Düşük): "))
                        if priority not in [1, 2, 3]:
                            raise ValueError
                        demand = float(input("Enerji Talebi (MW): "))
                        distance = float(input("Enerji Kaynağına Mesafe (km): "))
                        
                        grid.add_subscriber(name, priority, demand, distance)
                        print(f"\n{Styles.GREEN}✔️ {name} başarıyla veri tabanına O(1) hızında eklendi.{Styles.RESET}")
                    except ValueError:
                        print(f"{Styles.RED}Geçersiz giriş! Öncelik 1,2,3 ve talep/mesafe sayı olmalıdır.{Styles.RESET}")
                    time.sleep(2)
                    
                elif sub_choice == '2':
                    print(f"\n{Styles.BOLD}--- Abone Talep Güncelleme ---{Styles.RESET}")
                    name = input("Talebi güncellenecek abone adı: ").strip()
                    if name in grid.database:
                        try:
                            new_demand = float(input(f"Mevcut talep: {grid.database[name]['demand']} MW. Yeni talep (MW): "))
                            grid.update_subscriber_demand(name, new_demand)
                            print(f"\n{Styles.GREEN}✔️ {name} abonesinin talebi O(1) hızında güncellendi.{Styles.RESET}")
                        except ValueError:
                            print(f"{Styles.RED}Geçersiz sayısal değer!{Styles.RESET}")
                    else:
                        print(f"{Styles.RED}Sistemde '{name}' isimli bir abone bulunamadı.{Styles.RESET}")
                    time.sleep(2)
                    
                elif sub_choice == '3':
                    print(f"\n{Styles.BOLD}--- Abone Silme ---{Styles.RESET}")
                    name = input("Silinecek abone adı: ").strip()
                    if grid.remove_subscriber(name):
                        print(f"\n{Styles.GREEN}✔️ {name} abonesi O(1) hızında sistemden silindi.{Styles.RESET}")
                    else:
                        print(f"{Styles.RED}Sistemde '{name}' isimli bir abone bulunamadı.{Styles.RESET}")
                    time.sleep(2)
                    
                elif sub_choice == '4':
                    break
                    
        elif choice == '6':
            print_academic_explanation()
            
        elif choice == '0':
            print(f"\n{Styles.CYAN}SmartGrid-Core Simülasyonu sonlandırılıyor. İyi sunumlar! 🚀{Styles.RESET}\n")
            sys.exit(0)
            
        else:
            print(f"{Styles.RED}Geçersiz seçim! Lütfen menüdeki seçeneklerden birini girin.{Styles.RESET}")
            time.sleep(1.5)

if __name__ == '__main__':
    main()
