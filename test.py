import os
import unittest
import confg

class TestClass(unittest.TestCase):

    def test_conf(self):
        assert confg.DESTINATION_FOLDER is not None
        assert confg.STAGE_FOLDER is not None
        assert confg.SOURCE_FOLDERS is not None
        self.assertNotEqual(confg.DESTINATION_FOLDER, '')
        self.assertNotEqual(confg.STAGE_FOLDER, '')
        self.assertNotEqual(confg.SOURCE_FOLDERS, '')

        for fld in confg.SOURCE_FOLDERS.split('|'):
            self.assertTrue(os.path.exists(fld))
        for fld in confg.DESTINATION_FOLDER.split('|'):
            self.assertTrue(os.path.exists(fld))
        
        self.assertTrue(os.path.exists(confg.STAGE_FOLDER))

    def test_match(self):
        

if __name__ == "__main__":
    unittest.main()