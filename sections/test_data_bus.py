import unittest

from data_bus import DataBus


class TestDataBus(unittest.TestCase):
    def test_bus_8_bit_valid(self):
        bus = DataBus(8)
        bus.write(212)
        self.assertEqual(bus.read(), 212)

    def test_bus_8_bit_valid_multiple(self):
        bus = DataBus(8)
        bus.write(212)
        bus.write(4)
        self.assertEqual(bus.read(), 212)

    def test_bus_8_bit_invalid(self):
        bus = DataBus(8)
        with self.assertRaises(ValueError):
            bus.write(256)

    def test_bus_10_bit_valid(self):
        bus = DataBus(10)
        bus.write(567)
        self.assertEqual(bus.read(), 567)

    def test_bus_10_bit_invalid(self):
        bus = DataBus(10)
        with self.assertRaises(ValueError):
            bus.write(1100)

    def test_bus_16_bit_valid(self):
        bus = DataBus(16)
        bus.write(2110)
        self.assertEqual(bus.read(), 2110)

    def test_bus_16_bit_invalid(self):
        bus = DataBus(16)
        with self.assertRaises(ValueError):
            bus.write(70000)

    def test_bus_clear(self):
        bus = DataBus(8)
        bus.write(212)
        bus.clear()
        self.assertEqual(bus.read(), 0)

    def test_bus_init_error(self):
        with self.assertRaises(ValueError):
            DataBus(7)


if __name__ == '__main__':
    unittest.main()
