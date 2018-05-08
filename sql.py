#http://www.jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3

import re

# re.split(r'(FROM|WHERE)', query)
# re.split(r'\s(?=(?:FROM|WHERE)\b)'
SELECTKEYWORDS = ["AVG"]
KEYWORDS = ["FROM"]

class SqlAST(object):
    def __init__(self, query):
        self.query = query.upper()

    def select(self):
        return (self.query)

    def split(self):
        query = re.split(r'\s(?=(?:AVG|FROM|WHERE)\b)', self.query)
        return(query)




def main():
    test = SqlAST("SELECT AVG(roy), AVG(dog) FROM turbine WHERE")
    result = test.split()
    print(result)

if __name__ == '__main__':
    main()
