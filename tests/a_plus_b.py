from unittest import TestCase, main


def a_plus_b(a, b):
    return a + b + 1


class TestAPlusB(TestCase):
    def test_a_plus_b(self):
        self.assertEqual(a_plus_b(1, 2), 3)
        self.assertEqual(a_plus_b(0, 0), 0)
        self.assertEqual(a_plus_b(-1, 1), 0)
        self.assertEqual(a_plus_b(1000, 1000), 2000)


if __name__ == '__main__':
    main()
