from unittest import TestCase, main
from tools.singleton import SingletonMeta


class MyClass(metaclass=SingletonMeta):
    def __init__(self, x):
        self.x = x


class TestSingleton(TestCase):
    def test_singleton(self):
        obj1 = MyClass(1)
        obj2 = MyClass(2)
        self.assertEqual(obj1, obj2)
        self.assertEqual(id(obj1), id(obj2))
        self.assertEqual(obj1.x, 1)
        self.assertEqual(obj2.x, 1)
        self.assertIs(obj1, obj2)

        self.assertIs(obj1.__class__, obj2.__class__)

        self.assertIs(obj1.__class__, MyClass)

        self.assertIs(obj2.__class__, MyClass)


if __name__ == '__main__':
    main()
