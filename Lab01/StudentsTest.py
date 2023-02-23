import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()
    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        print("\nStart set_name test\n")
        for i, name in enumerate(self.user_name):
            self.students.set_name(name)
            self.user_id.append(i)
            self.assertEqual(self.students.name[i], self.user_name[i])
            print("{} {}".format(i, name))
        print("\nFinish set_name test\n")

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        print("\nStart get_name test")
        print("user_id length = {}".format(len(self.user_id)))
        print("user_name length = {}\n".format(len(self.user_name)))

        mex = len(self.user_name)
        for i in range(len(self.user_name)+1):
            if(i < mex):
                self.assertEqual(self.students.get_name(i), self.user_name[i])
            else:
                self.assertEqual(self.students.get_name(i), 'There is no such user')
            print("id {} : {}".format(i, self.students.get_name(i)))
        print("\nFinish get_name test")

if __name__ == '__main__':  # pragma: no cover
    unittest.main(verbosity=2)