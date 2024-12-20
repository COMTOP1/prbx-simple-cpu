import unittest

from mux import Mux


class TestMUX(unittest.TestCase):
    def test_mux_8_bit_get_input_0(self):
        mux = Mux(8)
        mux.set_input_0(12)
        mux.set_input_1(50)
        mux.set_control(0)
        self.assertEqual(mux.get(), 12)

    def test_mux_8_bit_get_input_1(self):
        mux = Mux(8)
        mux.set_input_0(12)
        mux.set_input_1(50)
        mux.set_control(1)
        self.assertEqual(mux.get(), 50)

    def test_mux_8_bit_input_0_error(self):
        mux = Mux(8)
        with self.assertRaises(ValueError):
            mux.set_input_0(1232)

    def test_mux_8_bit_input_1_error(self):
        mux = Mux(8)
        with self.assertRaises(ValueError):
            mux.set_input_1(1232)

    def test_mux_control_error(self):
        mux = Mux(8)
        with self.assertRaises(ValueError):
            mux.set_control(2)

    def test_mux_16_bit_get_input_0(self):
        mux = Mux(16)
        mux.set_input_0(50211)
        mux.set_input_1(60147)
        mux.set_control(0)
        self.assertEqual(mux.get(), 50211)

    def test_mux_16_bit_get_input_1(self):
        mux = Mux(16)
        mux.set_input_0(50211)
        mux.set_input_1(60147)
        mux.set_control(1)
        self.assertEqual(mux.get(), 60147)

    def test_mux_init_error(self):
        with self.assertRaises(ValueError):
            Mux(7)

if __name__ == '__main__':
    unittest.main()
