"""
This is the base test method
"""
import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('.', pattern = "test_*.py")
    unittest.TextTestRunner(verbosity=2).run(suite)
