import subprocess
import sys
import os

def run_tests():
    try:
        # Проверка, есть ли тестовые файлы
        if not os.path.exists("test_example.py"):
            with open("test_example.py", "w") as f:
                f.write('''
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    
    def test_positive_numbers(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(3, 4), 7)

    def test_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
                ''')
        
        # Запуск тестов с использованием coverage
        result = subprocess.run(["coverage", "run", "-m", "unittest", "discover"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def generate_coverage_report():
    subprocess.run(["coverage", "report"])
    subprocess.run(["coverage", "html"])

def run_game():
    import flet as ft
    from game import Game

    ft.app(target=Game)

if __name__ == "__main__":
    if run_tests():
        generate_coverage_report()
        print("Все тесты прошли успешно! Запуск игры...")
        run_game()
    else:
        generate_coverage_report()
        print("Некоторые тесты не прошли. Проверьте отчеты и исправьте ошибки перед запуском игры.")
        sys.exit(1)
