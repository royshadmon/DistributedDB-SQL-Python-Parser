#http://www.jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3

import re

# re.split(r'(FROM|WHERE)', query)
# re.split(r'\s(?=(?:FROM|WHERE)\b)'

class SqlAST(object):
    def __init__(self, query):
        self.query = query.upper()

    def select(self):
        return (self.query)

    # need to split into different lists to make AST
    def parse(self):
        self.query = re.split(r'\s(?=(?:SELECT|FROM|WHERE)\b)', self.query)
        select = self.query[0]
        tables = self.query[1]
        where = self.query[2]
        print("list is\n", self.query)
        return(select, tables, where)

    def evalSelect(self, select):
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

    def ensureTimeSeries (self, whereClause):
        if any("EventTime" in keyword for keyword in whereClause):
            return(True)

def main():
    test = SqlAST("SELECT AVG(roy), AVG(dog), Cat FROM turbine WHERE SELECT dog from cat;")
    select, tables, where = test.parse()
    if test.ensureTimeSeries(where):
        print("yessir")
    else:
        print("Unsupported query. Must have time-interval.")
    #print(select, "\n", tables, "\n", where)
    stmt = test.evalSelect(select)
    print(''.join(stmt))
    #final = test.convert(result)
    #print(final)

if __name__ == '__main__':
    main()
