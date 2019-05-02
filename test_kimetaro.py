import unittest


class TestKimetaro(unittest.TestCase):

    def test_sample(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
