import unittest
from unittest.mock import patch, Mock, MagicMock
from app import Application, MailSystem


class ApplicationTest(unittest.TestCase):
    
    def setUp(self):
        # stub
        Application.__init__ = MagicMock(return_value=None)
        self.app = Application()
        self.app.people = ["William", "Oliver", "Henry", "Liam"]
        self.app.selected = ["William", "Oliver", "Henry"]
        # self.app.selected = []        
        
    @patch.object(Application, 'get_random_person', side_effect=["William", "Oliver", "Henry", "Liam"])
    def test_app(self, mock_app):
        # mock 
        person = self.app.select_next_person()
        self.assertEqual(person, "Liam")
        print("{} selected".format(person))
        
        # spy
        self.app.mailSystem.write = MagicMock(side_effect = lambda x: 'Congrats, ' + x + '!')
        self.app.mailSystem.send = MagicMock()
        self.app.notify_selected()
        for name in self.app.selected:
            print(f"Congrats, {name}!")
        print("\n")
        print(self.app.mailSystem.write.call_args_list)
        print(self.app.mailSystem.send.call_args_list)

if __name__ == "__main__": 
    unittest.main(verbosity=2)