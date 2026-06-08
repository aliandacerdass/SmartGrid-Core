import heapq

class SmartGrid:
    def __init__(self):
        # O(1) Hash Map (Dictionary) representing the Subscriber Database
        # Key: Subscriber Name
        # Value: {priority: int, demand: float, distance: float, status: str, supplied_energy: float, loss: float}
        # Priority: 1 = Critical (Hospital), 2 = Normal (Residential), 3 = Low (Industrial)
        self.database = {}
        self._initialize_default_subscribers()

    def _initialize_default_subscribers(self):
        """Initializes the grid with default subscribers as per project specifications."""
        defaults = [
            # (Name, Priority, Demand in MW, Distance in km)
            ("Merkez Hastanesi", 1, 30.0, 2.0),
            ("Acil Durum İstasyonu", 1, 10.0, 1.5),
            ("A Mahallesi Konutları", 2, 25.0, 5.0),
            ("B Mahallesi Konutları", 2, 20.0, 8.0),
            ("Organize Sanayi Bölgesi", 3, 50.0, 12.0),
            ("Teknoloji Geliştirme Parkı", 3, 15.0, 6.0)
        ]
        for name, priority, demand, distance in defaults:
            self.add_subscriber(name, priority, demand, distance)

    def add_subscriber(self, name, priority, demand, distance):
        """Adds a subscriber to the O(1) Hash Map database."""
        self.database[name] = {
            "priority": priority,      # Priority Level (1: Highest, 3: Lowest)
            "demand": demand,          # Energy Demand in MW
            "distance": distance,      # Distance from source in km (used for loss calculation)
            "status": "Enerji Bekliyor",
            "supplied_energy": 0.0,
            "loss": 0.0
        }

    def remove_subscriber(self, name):
        """Removes a subscriber from the O(1) Hash Map database."""
        if name in self.database:
            del self.database[name]
            return True
        return False

    def update_subscriber_demand(self, name, new_demand):
        """Updates a subscriber's demand in O(1) time."""
        if name in self.database:
            self.database[name]["demand"] = new_demand
            return True
        return False

    def calculate_transmission_loss(self, demand, distance):
        """
        Calculates transmission loss based on distance.
        Formula: Loss = Demand * (Distance * LossCoefficient)
        Loss Coefficient is set to 1% per km (0.01) for this simulation.
        """
        loss_coefficient = 0.01
        return demand * (distance * loss_coefficient)

    def distribute_energy(self, total_power):
        """
        Distributes available power to subscribers using a Priority Queue and Greedy Allocation.
        
        Algorithmic Steps:
        1. Reset previous states.
        2. Build a Priority Queue (Min-Heap) using Python's heapq.
           Priority key is a tuple: (PriorityLevel, Distance, SubscriberName)
           - Primary Sort: Priority Level (1: Critical, 2: Normal, 3: Low)
           - Secondary Sort: Distance (Shorter distance = Less transmission loss = Greedy Choice)
        3. Allocate power greedily while total_power > 0.
        4. Update subscriber status in O(1) Hash Map.
        
        Returns:
            summary (dict): Statistics of the distribution.
        """
        # Reset states
        for name in self.database:
            self.database[name]["status"] = "Enerji Yok"
            self.database[name]["supplied_energy"] = 0.0
            self.database[name]["loss"] = 0.0

        # 1. Build the Priority Queue (Min-Heap)
        # Using heapq which is O(N log N) to build and process
        pq = []
        for name, info in self.database.items():
            # Heap elements are sorted by priority first, then by distance to minimize loss
            heapq.heappush(pq, (info["priority"], info["distance"], name))

        remaining_power = total_power
        total_supplied = 0.0
        total_loss = 0.0

        # 2. Greedy Allocation
        while pq and remaining_power > 0:
            priority, distance, name = heapq.heappop(pq)
            info = self.database[name]
            demand = info["demand"]
            
            # Loss for this path
            loss = self.calculate_transmission_loss(demand, distance)
            total_needed = demand + loss

            if remaining_power >= total_needed:
                # Fully supply the subscriber
                remaining_power -= total_needed
                self.database[name]["status"] = "Besleniyor (%100)"
                self.database[name]["supplied_energy"] = demand
                self.database[name]["loss"] = loss
                total_supplied += demand
                total_loss += loss
            elif remaining_power > 0:
                # Partially supply the subscriber
                # How much demand can we supply with the remaining power, accounting for loss ratio?
                # Formula: Supplied + Loss = Remaining => Supplied + Supplied * (Distance * 0.01) = Remaining
                # Supplied * (1 + Distance * 0.01) = Remaining
                # Supplied = Remaining / (1 + Distance * 0.01)
                supplied = remaining_power / (1 + (distance * 0.01))
                loss = remaining_power - supplied
                
                self.database[name]["status"] = f"Kısıtlı Besleniyor (%.2f MW)" % supplied
                self.database[name]["supplied_energy"] = supplied
                self.database[name]["loss"] = loss
                total_supplied += supplied
                total_loss += loss
                remaining_power = 0.0
            else:
                self.database[name]["status"] = "Enerji Kesildi (Yetersiz Kaynak)"

        # Mark any remaining unprocessed nodes in queue
        while pq:
            _, _, name = heapq.heappop(pq)
            self.database[name]["status"] = "Enerji Kesildi (Yetersiz Kaynak)"

        return {
            "input_power": total_power,
            "total_supplied": total_supplied,
            "total_loss": total_loss,
            "waste_power": remaining_power
        }
