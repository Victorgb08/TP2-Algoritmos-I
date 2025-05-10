import unittest
from tp1 import solve  # Certifique-se de que o nome do arquivo principal seja "tp1.py"

class TestDefesaCapital(unittest.TestCase):
    def test_exemplo_1(self):
        input_data = """5 7
9 1 1 1 9 9 9
9 0 9 1 1 1 9
9 0 9 50 9 1 9
9 1 1 1 9 1 9
9 9 9 1 9 9 9
3 4"""
        self.assertEqual(solve(input_data), 13)

    def test_exemplo_2(self):
        input_data = """5 7
1 1 1 1 1 1 0
1 0 4 4 4 1 0
1 0 4 20 4 1 0
1 1 4 4 4 1 0
1 1 1 1 1 1 0
3 4"""
        self.assertEqual(solve(input_data), 9)

    def test_exemplo_3(self):
        input_data = """9 4
1 1 1 1
1 2 1 1
1 0 1 1
1 1 1 1
1 1 1 1
1 1 1 1
0 0 1 1
1 1 1 1
1 1 1 1
2 2"""
        self.assertEqual(solve(input_data), 2)

if __name__ == "__main__":
    unittest.main()