import main, unittest

class fRequest():
    def __init__(self, name):
        self.__name = name
    def get_argument(self):
        return(self.__name)

class testReceiverClass(unittest.TestCase):
    def setup(self):
        self.receiver = main.receiver()
    def testFakeHandler(self):
        request fRequest('testdata')
        self.receiver.run()
