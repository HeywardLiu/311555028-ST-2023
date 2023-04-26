import unittest
from unittest.mock import patch, Mock, MagicMock
from course_scheduling_system import CSS

class CSSTest(unittest.TestCase):
    
    def test_q1_1(self):
        # stub
        css = CSS()
        css.check_course_exist = MagicMock(return_value=True)
        self.assertTrue(css.add_course(('Algorithms', 'Monday', 3, 4)))
        self.assertEqual(css.get_course_list(), [('Algorithms', 'Monday', 3, 4)])
        
    def test_q1_2(self):
        css = CSS()
        css.check_course_exist = MagicMock(return_value=True)
        css.add_course(('Algorithms', 'Monday', 3, 4))
        self.assertFalse(css.add_course(('Probability', 'Monday', 4, 5)))
        
    def test_q1_3(self):
        css = CSS()
        css.check_course_exist = MagicMock(return_value=False)
        css.add_course(('Algorithms', 'Monday', 3, 4))
        self.assertFalse(css.add_course(('Algorithms', 'Monday', 3, 4)))
    
    def test_q1_4(self):
        css = CSS()
        css.check_course_exist = MagicMock(return_value=True)
        with self.assertRaises(TypeError):
            css.add_course(('Algorithms', 'Monday'))
    
    def test_q1_5(self):
        css = CSS()
        css.check_course_exist = MagicMock(return_value=True)
        css.add_course(('DataStructure', 'Monday', 1, 2))
        css.add_course(('Algorithms', 'Monday', 3, 4))
        css.add_course(('Probability', 'Monday', 5, 6))
        self.assertTrue(css.remove_course(('Algorithms', 'Monday', 3, 4)))
        self.assertEqual(css.check_course_exist.call_count, 4)
        
        
    def test_q1_6(self): 
        css = CSS()
        css.check_course_exist = MagicMock(return_value=False)
        with self.assertRaises(TypeError):
            css.add_course((1, 'Monday', 5, 6))             # Course name
        with self.assertRaises(TypeError):
            css.add_course(('Probability', 'MyDAY', 5, 6))  # Day
        with self.assertRaises(TypeError):
            css.add_course(('Probability', 'Monday', 5, 0)) # Time    
            
        self.assertFalse(css.remove_course(('ABC', 'Monday', 5, 5))) # not in course list
        
        
        
if __name__ == "__main__":  # pragma: no cover
    unittest.main(verbosity=2)