import cpu_stats
import unittest


class TestCPUStats(unittest.TestCase):
    def test_is_cpu(self):
        self.assertTrue(cpu_stats.is_cpu("cpu123"))
        self.assertFalse(cpu_stats.is_cpu("abc"))
        self.assertFalse(cpu_stats.is_cpu("cpuabc"))

    def test_is_rapl(self):
        self.assertTrue(cpu_stats.is_rapl("intel-rapl:0:0"))
        self.assertFalse(cpu_stats.is_rapl("abc"))
        self.assertFalse(cpu_stats.is_rapl("intel-rapl:X:Y"))


if __name__ == "__main__":
    unittest.main()
