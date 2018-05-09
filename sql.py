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

    # need to split into different lists to make AST
    def parse(self):
        self.query = re.split(r'\s(?=(?:FROM|WHERE)\b)', self.query)
        #print(self.query)
        select = self.query[0]
        tables = self.query[1]
        where = self.query[2]
        #print(where)
        #self.query=re.split('\s|(?<!\d)[,.](?!\d)', self.query)
        #for index, word in enumerate(self.query):
        #    if "AVG(" in word:
        #        word = re.sub("AVG", "", word)
                #word = ''.join(e for e in word if e.isalnum())
        #        self.query[index] = " SUM" + word + ", " +  "COUNT" + word
        #    if "FROM" not in self.query[(index+1) % len(self.query)]:
        #        i = 1
        #        self.query[index] += ", "
        #    else:
        #        self.query[index] += " "
        #    print(index, word)
        return(select, tables, where)
#https://stackoverflow.com/questions/2582138/finding-and-replacing-elements-in-a-list-python
    def convertSelect(self, select):
        query = re.split('\s|(?<!\d)[,.](?!\d)', select)
        query = list(filter(None, query))
        for index, word in enumerate(query):
            if "AVG(" in word:
                word = re.sub("AVG", "", word)
                newSelect = word.replace(word," SUM" + word + ", " +  "COUNT" + word + "")
                try:
                    if query[index + 1]: 
                        newSelect += ", "
                except IndexError:
                    pass
                query[index] = newSelect
        return(query)

def main():
    test = SqlAST("SELECT AVG(roy), AVG(dog), Cat FROM turbine WHERE")
    select, tables, where = test.parse()
    #print(select, "\n", tables, "\n", where)
    stmt = test.convertSelect(select)
    print(''.join(stmt))
    #final = test.convert(result)
    #print(final)

if __name__ == '__main__':
    main()
