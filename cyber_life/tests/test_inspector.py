import unittest

from cyber_life.computer_info.inspector_cpu import InspectorCpu


class TestInspectorCpu(unittest.TestCase):
    def setUp(self):
        self.inspector = InspectorCpu()

    def test_get_cpu_info(self):
        pass


if __name__ == '__main__':
    unittest.main()
