import unittest
from smart_grid import SmartGrid

class TestSmartGrid(unittest.TestCase):
    def setUp(self):
        self.grid = SmartGrid()

    def test_database_operations(self):
        # Test addition (O(1) Hash Map)
        self.grid.add_subscriber("Test Abone", 2, 15.0, 4.0)
        self.assertIn("Test Abone", self.grid.database)
        self.assertEqual(self.grid.database["Test Abone"]["priority"], 2)
        self.assertEqual(self.grid.database["Test Abone"]["demand"], 15.0)

        # Test update (O(1) Hash Map)
        self.grid.update_subscriber_demand("Test Abone", 20.0)
        self.assertEqual(self.grid.database["Test Abone"]["demand"], 20.0)

        # Test removal (O(1) Hash Map)
        self.grid.remove_subscriber("Test Abone")
        self.assertNotIn("Test Abone", self.grid.database)

    def test_high_energy_distribution(self):
        # 170 MW is enough to supply everyone including transmission losses (total needed is ~160.5 MW)
        summary = self.grid.distribute_energy(170.0)
        
        # All default subscribers should be fully supplied
        self.assertEqual(self.grid.database["Merkez Hastanesi"]["status"], "Besleniyor (%100)")
        self.assertEqual(self.grid.database["Acil Durum İstasyonu"]["status"], "Besleniyor (%100)")
        self.assertEqual(self.grid.database["A Mahallesi Konutları"]["status"], "Besleniyor (%100)")
        self.assertEqual(self.grid.database["Organize Sanayi Bölgesi"]["status"], "Besleniyor (%100)")
        
        # Verify total supplied matches sum of demands
        expected_demand = sum(info["demand"] for info in self.grid.database.values())
        self.assertAlmostEqual(summary["total_supplied"], expected_demand)

    def test_priority_based_distribution(self):
        # 45 MW should only supply critical nodes and maybe part of the next level
        # Priority 1:
        # Merkez Hastanesi: Demand 30, Distance 2. Loss = 30 * (2 * 0.01) = 0.6. Total needed = 30.6
        # Acil Durum İstasyonu: Demand 10, Distance 1.5. Loss = 10 * (1.5 * 0.01) = 0.15. Total needed = 10.15
        # Total Priority 1 needed = 40.75 MW.
        # This leaves 45 - 40.75 = 4.25 MW for Priority 2.
        summary = self.grid.distribute_energy(45.0)
        
        # Critical nodes should be fully supplied
        self.assertEqual(self.grid.database["Merkez Hastanesi"]["status"], "Besleniyor (%100)")
        self.assertEqual(self.grid.database["Acil Durum İstasyonu"]["status"], "Besleniyor (%100)")
        
        # Normal nodes (priority 2) should either be partially supplied or cut off
        # A Mahallesi Konutları (Priority 2, Distance 5) and B Mahallesi Konutları (Priority 2, Distance 8)
        # Since A Mahallesi is closer (5km vs 8km), the greedy algorithm prioritizes A Mahallesi Konutları for the remaining 4.25 MW.
        # Let's verify that A Mahallesi receives the remaining power (partially supplied) and B Mahallesi is cut off.
        self.assertTrue("Kısıtlı" in self.grid.database["A Mahallesi Konutları"]["status"])
        self.assertEqual(self.grid.database["B Mahallesi Konutları"]["status"], "Enerji Kesildi (Yetersiz Kaynak)")
        
        # Priority 3 should be completely cut off
        self.assertEqual(self.grid.database["Organize Sanayi Bölgesi"]["status"], "Enerji Kesildi (Yetersiz Kaynak)")

if __name__ == '__main__':
    unittest.main()
