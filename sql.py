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
        select = []
        tables = []
        where = []
        self.query = re.split(r'\s(?=(?:SELECT|FROM|WHERE)\b)', self.query)
        print(self.query)
        for i, part in enumerate(self.query):
            if "SELECT" in part:
                select.append(part)
            if "FROM" in part:
                tables.append(part)
            if "WHERE" in part:
                where.append(part)
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


    def ensureTimeSeries(self, where):
        #if where.Contains("EVENTTIME"):
        #filter(lambda string: "EVENTTIME" in string, where)
        if any("EVENTTIME" in string for string in where):
            return(True)
        else:
            return(False)

def main():
    test = SqlAST("SELECT AVG(roy), AVG(dog), Cat FROM turbine WHERE EventTime > 6 AND SELECT dog from cat where babe = 0 AND EventTime < 4;")
    select, tables, where = test.parse()
    if test.ensureTimeSeries(where):
        print("yessir")
    else:
        print("Unsupported query. Must have time-interval.")
    #print(select, "\n", tables, "\n", where)
    #stmt = test.evalSelect(select)
    #print(''.join(stmt))
    #final = test.convert(result)
    #print(final)

if __name__ == '__main__':
    main()
