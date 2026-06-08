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

def animate_loading(duration=1.0, text="Sistem yükleniyor"):
    """Displays a spinning loader animation in the terminal."""
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    sys.stdout.write(" ")
    while time.time() < end_time:
        sys.stdout.write(f"\r {Styles.BOLD}{Styles.CYAN}{chars[i % len(chars)]}{Styles.RESET} {text}...")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
    sys.stdout.flush()

def animate_pulse(text, pulses=3):
    """Flashes a warning or status text to grab attention."""
    for _ in range(pulses):
        sys.stdout.write(f"\r {Styles.BOLD}{Styles.YELLOW}{text}{Styles.RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write(f"\r {' ' * (len(text) + 2)}")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write(f"\r {Styles.BOLD}{Styles.GREEN}{text}{Styles.RESET}\n")
    sys.stdout.flush()

def print_header():
    title = f"""
{Styles.BOLD}{Styles.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║   ⚡ SmartGrid-Core: Öncelik Tabanlı Dinamik Enerji Dağıtımı ⚡       ║
║        [ O(1) Veri Tabanı + Priority Queue + Greedy Dağıtım ]        ║
╚══════════════════════════════════════════════════════════════════════╝{Styles.RESET}"""
    print(title)

def print_grid_graph(grid, input_power=None):
    """Draws an animated visual ASCII node-link diagram representing the grid."""
    print(f"\n{Styles.BOLD}{Styles.CYAN}🌐 ŞEBEKE TOPOLOJİSİ VE ANLIK ENERJİ AKIŞ DİYAGRAMI{Styles.RESET}")
    print("=" * 80)
    
    if input_power is not None:
        print(f" 🔌 [ KAYNAK: Yenilenebilir Enerji Girişi ] ➔ {Styles.BOLD}{Styles.GREEN}{input_power:.2f} MW{Styles.RESET}")
    else:
        print(" 🔌 [ KAYNAK: Yenilenebilir Enerji Girişi ]")
    print("                      │")
    
    # Sort subscribers by priority then distance (just like the heapq algorithm sorts them)
    # so they appear in distribution preference order
    subscribers = sorted(grid.database.items(), key=lambda x: (x[1]["priority"], x[1]["distance"]))
    
    for i, (name, info) in enumerate(subscribers):
        is_last = (i == len(subscribers) - 1)
        branch = " └──" if is_last else " ├──"
        
        status = info["status"]
        dist_str = f"{info['distance']:.1f} km"
        
        # Icon select based on priority/name
        if info["priority"] == 1:
            icon = "🏥"
            p_label = "Kritik"
        elif info["priority"] == 2:
            icon = "🏠"
            p_label = "Normal"
        else:
            icon = "🏭"
            p_label = "Düşük "

        # Color-coded arrow and statuses
        if "Besleniyor (%100)" in status:
            arrow = f"{Styles.GREEN}═══({dist_str})═══▶{Styles.RESET}"
            node_box = f"{Styles.BOLD}{Styles.GREEN}[{icon} {name}]{Styles.RESET}"
            status_box = f"{Styles.GREEN}● Besleniyor (100%){Styles.RESET} [Yük: {info['supplied_energy']:.1f} MW]"
        elif "Kısıtlı" in status:
            arrow = f"{Styles.YELLOW}───({dist_str})───▶{Styles.RESET}"
            node_box = f"{Styles.YELLOW}[{icon} {name}]{Styles.RESET}"
            status_box = f"{Styles.YELLOW}◑ {status}{Styles.RESET} [Kaybı: {info['loss']:.2f} MW]"
        else:
            arrow = f"{Styles.RED}───({dist_str})───✖{Styles.RESET}"
            node_box = f"{Styles.RED}[{icon} {name}]{Styles.RESET}"
            status_box = f"{Styles.RED}○ Enerji Kesildi{Styles.RESET}"
            
        print(f"{branch} {arrow} {node_box:<42} {status_box}")
        if not is_last:
            print(" │")
    print("=" * 80)

def print_subscriber_table(grid):
    """Prints subscribers stored in the O(1) Hash Map database."""
    print(f"\n{Styles.BOLD}{Styles.UNDERLINE}📊 ANLIK DURUM SÖZLÜĞÜ (O(1) Hash-Map Database){Styles.RESET}")
    print("-" * 110)
    print(f"{'Abone Anahtarı (Key)':<30} | {'Öncelik Derecesi':<18} | {'Talep (MW)':<12} | {'Mesafe (km)':<12} | {'Sistem Durumu':<24}")
    print("-" * 110)
    
    priority_map = {
        1: f"{Styles.RED}1: Kritik (Hastane vb){Styles.RESET}",
        2: f"{Styles.YELLOW}2: Normal (Konutlar){Styles.RESET}",
        3: f"{Styles.BLUE}3: Düşük (Sanayi vb){Styles.RESET}"
    }

    for name, info in grid.database.items():
        priority_str = priority_map.get(info['priority'], str(info['priority']))
        status_raw = info['status']
        
        if "Besleniyor (%100)" in status_raw:
            status_str = f"{Styles.GREEN}{status_raw}{Styles.RESET}"
        elif "Kısıtlı" in status_raw:
            status_str = f"{Styles.YELLOW}{status_raw}{Styles.RESET}"
        else:
            status_str = f"{Styles.RED}{status_raw}{Styles.RESET}"
            
        print(f"{name:<30} | {priority_str:<29} | {info['demand']:<12.2f} | {info['distance']:<12.1f} | {status_str:<33}")
    print("-" * 110)

def print_distribution_summary(summary):
    """Prints the distribution simulation result statistics."""
    print(f"\n{Styles.BOLD}{Styles.CYAN}📈 ENERJİ DENGELEME VE TÜKETİM ANALİZ RAPORU{Styles.RESET}")
    print("─" * 50)
    print(f"  ⚡ Üretilen Toplam Güç           : {Styles.BOLD}{summary['input_power']:.2f} MW{Styles.RESET}")
    print(f"  🟢 Tüketicilere Ulaşan Güç       : {Styles.GREEN}{summary['total_supplied']:.2f} MW{Styles.RESET}")
    print(f"  🔴 Hat Üzerinde Kaybolan Güç     : {Styles.RED}{summary['total_loss']:.2f} MW{Styles.RESET}")
    print(f"  🟡 Boşa Giden / Atıl Kalan Güç   : {Styles.YELLOW}{summary['waste_power']:.2f} MW{Styles.RESET}")
    
    total_needed = summary['total_supplied'] + summary['total_loss']
    if total_needed > 0:
        efficiency = (summary['total_supplied'] / total_needed) * 100
        print(f"  🏆 Şebeke Dağıtım Verimliliği   : {Styles.BOLD}{Styles.CYAN}{efficiency:.2f}%{Styles.RESET}")
    print("─" * 50)

def print_academic_explanation():
    clear_screen()
    print_header()
    explanation = f"""
{Styles.BOLD}{Styles.YELLOW}🎓 HOCAYA SUNUM İÇİN TEORİK ALTYAPI VE ANALİZ{Styles.RESET}

Bu proje, yenilenebilir enerji kaynaklarının dağıtımını bilgisayar mühendisliği
optimizasyon algoritmaları ve veri yapıları aracılığıyla simüle eder.

{Styles.BOLD}1. Veri Tabanı Katmanı - Hash Map {Styles.GREEN}[ Zaman Karmaşıklığı: O(1) ]{Styles.RESET}
   - Şebekedeki tüm aboneler ve durumları bellekte bir Hash Map (Python `dict`) olarak tutulur.
   - Bu sayede aboneye erişim, talep güncellemesi ve abone silme/ekleme maliyetleri
     şebekedeki eleman sayısından bağımsız olarak her zaman {Styles.BOLD}sabit zaman {Styles.GREEN}O(1){Styles.RESET}'dir.

{Styles.BOLD}2. Dağıtım Sırası - Priority Queue (Öncelikli Kuyruk) {Styles.GREEN}[ Zaman Karmaşıklığı: O(N log N) ]{Styles.RESET}
   - Enerjinin paylaştırılması gerektiğinde aboneler anlık olarak bir Min-Heap (`heapq`)
     veri yapısına eklenir.
   - Önceliklendirme anahtarı: {Styles.BOLD}(Öncelik Seviyesi, Mesafe, İsim){Styles.RESET}'dir.
   - Burada birincil öncelik kritikliktir (1: Kritik, 3: Düşük).
   - İkincil öncelik ise {Styles.CYAN}Greedy (Açgözlü){Styles.RESET} mesafe seçimidir.

{Styles.BOLD}3. En Az Kayıpla Dağıtım - Greedy (Açgözlü) Yaklaşım:{Styles.RESET}
   - Fiziksel iletim hattındaki direnç ve kayıplar mesafe ile doğru orantılıdır.
   - Aynı öncelik grubunda olan abonelerden, kaynağa {Styles.UNDERLINE}en yakın{Styles.RESET} olana öncelik verilir.
   - Bu sayede hatlardaki elektrik iletim kaybı matematiksel olarak en aza indirilir.
    """
    print(explanation)
    input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")

def main():
    grid = SmartGrid()
    
    clear_screen()
    print_header()
    print(f"\n⚡ {Styles.YELLOW}SmartGrid-Core Simülasyon Arayüzü Başlatılıyor...{Styles.RESET}")
    animate_loading(1.5, "Veri tabanı in-memory olarak başlatılıyor")
    animate_loading(1.0, "Şebeke hatları ve topoloji taranıyor")
    
    print(f"\n{Styles.BOLD}{Styles.GREEN}✔️ SİSTEM BAŞARIYLA AYAKTA!{Styles.RESET}")
    time.sleep(0.5)
    
    # Show initial grid
    clear_screen()
    print_header()
    print_subscriber_table(grid)
    print_grid_graph(grid)
    input(f"\n👉 {Styles.BOLD}Simülasyon ana menüsüne geçmek için Enter'a basın...{Styles.RESET}")

    while True:
        clear_screen()
        print_header()
        
        print(f"{Styles.BOLD}⚡ LÜTFEN BİR İŞLEM / SENARYO SEÇİN:{Styles.RESET}\n")
        print(f" [{Styles.BOLD}1{Styles.RESET}] 📊 Şebeke Durum Tablosunu Görüntüle")
        print(f" [{Styles.BOLD}2{Styles.RESET}] 🌐 Şebeke Topolojisini ve Akışı Görüntüle")
        print(f" [{Styles.BOLD}3{Styles.RESET}] 🌞 Senaryo 1: Yüksek Üretim (Güneşli Gün - 100.00 MW)")
        print(f" [{Styles.BOLD}4{Styles.RESET}] ☁️ Senaryo 2: Düşük Üretim (Rüzgarsız Gece - 30.00 MW)")
        print(f" [{Styles.BOLD}5{Styles.RESET}] 🔌 Dinamik Mod: Toplam Giriş Gücünü Kendin Gir")
        print(f" [{Styles.BOLD}6{Styles.RESET}] 👥 Abone Yönetim Paneli (Ekle/Güncelle/Sil)")
        print(f" [{Styles.BOLD}7{Styles.RESET}] 🎓 Akademik Altyapı Açıklaması (Hocaya Sunum)")
        print(f" [{Styles.BOLD}0{Styles.RESET}] 🚪 Çıkış")
        
        choice = input(f"\n👉 {Styles.BOLD}Seçiminiz: {Styles.RESET}").strip()
        
        if choice == '1':
            clear_screen()
            print_header()
            print_subscriber_table(grid)
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '2':
            clear_screen()
            print_header()
            print_grid_graph(grid)
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '3':
            clear_screen()
            print_header()
            print(f"{Styles.BOLD}{Styles.YELLOW}🌞 SENARYO 1 BAŞLATILIYOR: Yüksek Enerji Girişi (100.00 MW)...{Styles.RESET}")
            animate_loading(1.5, "Algoritma çalıştırılıyor ve öncelik kuyruğu işletiliyor")
            summary = grid.distribute_energy(100.0)
            
            print_subscriber_table(grid)
            print_grid_graph(grid, 100.0)
            print_distribution_summary(summary)
            
            animate_pulse("✔️ TÜM ABONELER BAŞARIYLA BESLENİYOR!", 2)
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '4':
            clear_screen()
            print_header()
            print(f"{Styles.BOLD}{Styles.YELLOW}☁️ SENARYO 2 BAŞLATILIYOR: Kısıtlı Enerji Girişi (30.00 MW)...{Styles.RESET}")
            animate_loading(1.5, "Öncelik kuyruğu taranıyor ve düşük öncelikliler kesiliyor")
            summary = grid.distribute_energy(30.0)
            
            print_subscriber_table(grid)
            print_grid_graph(grid, 30.0)
            print_distribution_summary(summary)
            
            animate_pulse("🚨 ŞEBEKE KRİZ MODUNDA! DÜŞÜK ÖNCELİKLER KESİLDİ, KRİTİKLER KORUNDU.", 3)
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '5':
            clear_screen()
            print_header()
            print(f"{Styles.BOLD}🔋 DİNAMİK ENERJİ GİRİŞ MODU{Styles.RESET}")
            try:
                power_in = float(input("\nŞebekeye verilecek yenilenebilir güç miktarını girin (MW): "))
                if power_in < 0:
                    print(f"{Styles.RED}Hata: Negatif güç girişi yapılamaz.{Styles.RESET}")
                    time.sleep(1.5)
                    continue
                
                clear_screen()
                print_header()
                print(f"{Styles.YELLOW}⚡ {power_in:.2f} MW Güç Şebekeye Veriliyor...{Styles.RESET}")
                animate_loading(1.2, "Greedy algoritma çalıştırılıyor")
                
                summary = grid.distribute_energy(power_in)
                print_subscriber_table(grid)
                print_grid_graph(grid, power_in)
                print_distribution_summary(summary)
                
            except ValueError:
                print(f"{Styles.RED}Hata: Lütfen geçerli bir sayı girin.{Styles.RESET}")
            input(f"\n{Styles.BOLD}Menüye dönmek için Enter tuşuna basın...{Styles.RESET}")
            
        elif choice == '6':
            while True:
                clear_screen()
                print_header()
                print(f"{Styles.BOLD}👥 ABONE YÖNETİM PANELİ (O(1) Hash Map İşlemleri){Styles.RESET}\n")
                print(" [1] Yeni Abone Ekle (Add)")
                print(" [2] Abone Talebini Güncelle (Update)")
                print(" [3] Abone Sil (Delete)")
                print(" [4] Geri Dön")
                
                sub_choice = input(f"\n👉 {Styles.BOLD}Seçiminiz: {Styles.RESET}").strip()
                
                if sub_choice == '1':
                    print(f"\n{Styles.BOLD}--- Abone Ekleme ---{Styles.RESET}")
                    name = input("Abone Adı (Örn: C Mahallesi Konutları): ").strip()
                    if not name:
                        print(f"{Styles.RED}Abone adı boş kalamaz!{Styles.RESET}")
                        time.sleep(1.5)
                        continue
                    try:
                        priority = int(input("Öncelik (1: Kritik, 2: Normal, 3: Düşük): "))
                        if priority not in [1, 2, 3]:
                            raise ValueError
                        demand = float(input("Enerji Talebi (MW): "))
                        distance = float(input("Enerji Kaynağına Mesafe (km): "))
                        
                        animate_loading(0.8, "Veri tabanında yer ayrılıyor")
                        grid.add_subscriber(name, priority, demand, distance)
                        print(f"\n{Styles.GREEN}✔️ {name} abonesi O(1) hızda Hash Map'e başarıyla eklendi!{Styles.RESET}")
                    except ValueError:
                        print(f"{Styles.RED}Hatalı giriş! Lütfen sayısal verileri kontrol edin.{Styles.RESET}")
                    time.sleep(2)
                    
                elif sub_choice == '2':
                    print(f"\n{Styles.BOLD}--- Abone Güncelleme ---{Styles.RESET}")
                    name = input("Güncellenecek Abone Adı: ").strip()
                    if name in grid.database:
                        try:
                            new_demand = float(input(f"Mevcut talep {grid.database[name]['demand']} MW. Yeni Talep (MW): "))
                            animate_loading(0.6, "Hash-Map verisi güncelleniyor")
                            grid.update_subscriber_demand(name, new_demand)
                            print(f"\n{Styles.GREEN}✔️ {name} abonesinin talebi O(1) hızında güncellendi!{Styles.RESET}")
                        except ValueError:
                            print(f"{Styles.RED}Hata: Geçersiz değer.{Styles.RESET}")
                    else:
                        print(f"{Styles.RED}Hata: Abone bulunamadı.{Styles.RESET}")
                    time.sleep(2)
                    
                elif sub_choice == '3':
                    print(f"\n{Styles.BOLD}--- Abone Silme ---{Styles.RESET}")
                    name = input("Silinecek Abone Adı: ").strip()
                    animate_loading(0.6, "Veri tabanından siliniyor")
                    if grid.remove_subscriber(name):
                        print(f"\n{Styles.GREEN}✔️ {name} abonesi O(1) hızında Hash Map'ten silindi.{Styles.RESET}")
                    else:
                        print(f"{Styles.RED}Hata: Abone bulunamadı.{Styles.RESET}")
                    time.sleep(2)
                    
                elif sub_choice == '4':
                    break
                    
        elif choice == '7':
            print_academic_explanation()
            
        elif choice == '0':
            print(f"\n{Styles.CYAN}SmartGrid-Core Simülasyonu Sonlandırıldı. İyi Sunumlar dileriz! 🚀{Styles.RESET}\n")
            sys.exit(0)
            
        else:
            print(f"{Styles.RED}Hata: Geçersiz menü seçimi.{Styles.RESET}")
            time.sleep(1.2)

if __name__ == '__main__':
    main()
