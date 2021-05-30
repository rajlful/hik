import unittest
import hikisapi

class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      test_get = Hikvision('172.16.13.70', 'admin', 'Admin321678')
      self.assertFalse(test_get.get_model_name(), isinstance(test_get.get_model_name(), str))
      print(test_get.get_model_name())

if __name__ == '__main__':
    unittest.main()