from base import BaseTest
from emailcontents.quoted import extract

class Test(BaseTest):
    def test(self):
        "Check empty"
        a = ""
        x = {'text' : "", 'quoter': "", 'raw': "", "empty":True}
        x = self._massage(x)
        self.assertEquals( extract(a), x )

    def none_test(self):
        "Check None"
        a = None
        x = {'text' : "", 'quoter': "", 'raw': "", "empty":True}
        x = self._massage(x)
        self.assertEquals( extract(a), x )
