import unittest

from alu import ALU


class TestALU(unittest.TestCase):
    def test_alu_init_invalid(self):
        with self.assertRaises(ValueError):
            ALU(11)

    def test_alu_8_bit_input_a_invalid(self):
        alu = ALU(8)
        with self.assertRaises(ValueError):
            alu.set_input_a(256)

    def test_alu_8_bit_input_b_invalid(self):
        alu = ALU(8)
        with self.assertRaises(ValueError):
            alu.set_input_b(256)

    def test_alu_16_bit_input_a_invalid(self):
        alu = ALU(16)
        with self.assertRaises(ValueError):
            alu.set_input_a(70000)

    def test_alu_16_bit_input_b_invalid(self):
        alu = ALU(16)
        with self.assertRaises(ValueError):
            alu.set_input_b(70000)

    def test_alu_control_valid(self):
        alu = ALU(8)
        alu.set_control(2)

    def test_alu_control_invalid(self):
        alu = ALU(8)
        with self.assertRaises(ValueError):
            alu.set_control(8)


if __name__ == '__main__':
    unittest.main()
