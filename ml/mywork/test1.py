import unittest
import task1

class TestURL(unittest.TestCase):        
    known_values = (('', False),
                    ('1.2', False),
                    ('a.b', True),
                    ('www.a/', True),
                    ('a.com', True),
                    ('www.a.com', True),
                    ('http://a.com', True),                                        
                   )
       
    def test_url_known_values(self):
        for s, expect in self.known_values:
            res = task1.isURL(s)
            try:
                self.assertEqual(expect, res)
            except:
                raise Exception("'%s': '%s' expected, '%s' returned" \
                                % (s, str(expect), str(res)))
                    
class TestDATE(unittest.TestCase):        
    known_values = (('', False),
                    ('2013-7-19', True),
                    ('7-19-2013', True),
                    ('7/19-7/30', True),
                    ('7/19/13', True),
                    ('19.7.13', True),
                    ('19.7.2013', True),
                    ('2013 - 7 - 09', False),           
                   )
       
    def test_date_known_values(self):
        for s, expect in self.known_values:
            res = task1.isDate(s)
            try:
                self.assertEqual(expect, res)
            except:
                raise Exception("'%s': '%s' expected, '%s' returned" \
                                % (s, str(expect), str(res)))

class TestNUM(unittest.TestCase):        
    known_values = (('', False),
                    ('19', True),
                    ('1.2', True),
                    ('1.2.3', False),
                    ('19.', False),                                       
                   )
       
    def test_num_known_values(self):
        for s, expect in self.known_values:
            res = task1.isNum(s)
            try:
                self.assertEqual(expect, res)
            except:
                raise Exception("'%s': '%s' expected, '%s' returned" \
                                % (s, str(expect), str(res)))

class TestCODE(unittest.TestCase):        
    known_values = (('', False),
#                    ('S4OFF', True),
                    ('4OFF', True),
                    ('LOVE', False),
                    ('4S4B', False),                                       
                   )
       
    def test_code_known_values(self):
        for s, expect in self.known_values:
            res = task1.isNum(s)
            try:
                self.assertEqual(expect, res)
            except:
                raise Exception("'%s': '%s' expected, '%s' returned" \
                                % (s, str(expect), str(res)))

class TestPreProcess(unittest.TestCase):        
    known_values = (('', []),
                    ('($40 OFF)!', ['$','NUM','off']),
                    ('Save $11.95', ['save','$','NUM']),
                    ('(7/25-7/28)', ['DATE']),   
                    ("customer's", ['customer',"'s"]), 
                    ("V-neck Floor-Length", ['v-neck','floor-length']), 
                    ("4x6/4xD prints.", ['4x6/4xd','print']), 
                    ("Deals,iHealthTree", ['deals,ihealthtree']), 
                    ("Priced Item + Free Shipping", ['priced','item','free','shipping']), 
                                                      
                   )
       
    def test_code_known_values(self):
        for s, expect in self.known_values:
            res = task1.preprocess(s)
            try:
                self.assertEqual(expect, res)
            except:
                raise Exception("'%s': '%s' expected, '%s' returned" \
                                % (s, str(expect), str(res)))                               
if __name__ == '__main__':
    unittest.main()
