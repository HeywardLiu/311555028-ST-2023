import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()
    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        print("\nStart set_name test\n")
        
        for name in self.user_name:
            id = self.students.set_name(name)
            self.assertNotIn(id, self.user_id)  # check unique id
            self.user_id.append(id)
            print("{} {}".format(id, name))
            
        print("\nFinish set_name test\n")

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        print("\nStart get_name test")
        print("user_id length = {}".format(len(self.user_id)))
        print("user_name length = {}\n".format(len(self.user_name)))
        
        mex = 0
        for i in range(len(self.user_id)+1): # find mex of user_id set
            if i not in self.user_id:
                mex = i
                break
            
        for id, name in zip(self.user_id, self.user_name): # check get_name(id) == corresponding user name
            self.assertEqual(name, self.students.get_name(id))
            print("id {} : {}".format(id, self.students.get_name(id)))        
        self.assertEqual('There is no such user', self.students.get_name(mex)) # check mex and its corresponding output
        print("id {} : {}".format(mex, self.students.get_name(mex)))
        
        print("\nFinish get_name test")

if __name__ == '__main__':  # pragma: no cover
    unittest.main(verbosity=2)