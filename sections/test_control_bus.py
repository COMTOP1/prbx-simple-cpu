import unittest

from sections.control_bus import ControlBus, DATA_SEL, ADDR_SEL, IR_WR


class TestControlBus(unittest.TestCase):
    def setUp(self):
        self.control_bus = ControlBus()

    def test_add_control(self):
        self.control_bus.add_control(DATA_SEL)
        self.assertEqual(self.control_bus.read_control_bus(), DATA_SEL)

    def test_add_multiple_control(self):
        self.control_bus.add_control(ADDR_SEL)
        self.control_bus.add_control(IR_WR)
        self.assertEqual(self.control_bus.read_control_bus(), ADDR_SEL | IR_WR)

    def test_clear_control(self):
        self.control_bus.add_control(ADDR_SEL)
        self.control_bus.add_control(IR_WR)
        self.control_bus.clear()
        self.assertEqual(self.control_bus.read_control_bus(), 0)


if __name__ == '__main__':
    unittest.main()
