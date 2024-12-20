import unittest

from sections.alu import ALU


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

    def test_alu_8_bit_add(self):
        alu = ALU(8)
        alu.set_control(0)
        alu.set_input_a(12)
        alu.set_input_b(14)
        self.assertEqual(alu.get(), 26)

    def test_alu_8_bit_add_overflow(self):
        alu = ALU(8)
        alu.set_control(0)
        alu.set_input_a(123)
        alu.set_input_b(141)
        self.assertEqual(alu.get(), 8)

    def test_alu_8_bit_sub(self):
        alu = ALU(8)
        alu.set_control(1)
        alu.set_input_a(12)
        alu.set_input_b(6)
        self.assertEqual(alu.get(), 6)

    def test_alu_8_bit_sub_underflow(self):
        alu = ALU(8)
        alu.set_control(1)
        alu.set_input_a(123)
        alu.set_input_b(141)
        self.assertEqual(alu.get(), 18)

    def test_alu_8_bit_and(self):
        alu = ALU(8)
        alu.set_control(2)
        alu.set_input_a(123)
        alu.set_input_b(141)
        self.assertEqual(alu.get(), 9)

    def test_alu_8_bit_pass(self):
        alu = ALU(8)
        alu.set_control(4)
        alu.set_input_a(123)
        alu.set_input_b(141)
        self.assertEqual(alu.get(), 141)

    def test_alu_8_bit_nu(self):
        alu = ALU(8)
        alu.set_control(5)
        alu.set_input_a(123)
        alu.set_input_b(141)
        self.assertEqual(alu.get(), 0)


if __name__ == '__main__':
    unittest.main()
