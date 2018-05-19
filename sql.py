#http://www.jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3

import re

class SqlAST(object):
    def __init__(self, query):
        self.query = query.upper()

    def select(self):
        return (self.query)

    # need to split into different lists to make AST
    def parse(self):
        select, tables, where = [], [], []
        self.query = re.split(r'\s(?=(?:SELECT|FROM|WHERE)\b)', self.query)
        for i, part in enumerate(self.query):
            if "SELECT" in part:
                select.append(part)
            if "FROM" in part:
                tables.append(part)
            if "WHERE" in part:
                where.append(part)
        return(select, tables, where)

    def evalSelect(self, select):
        for i, stmt in enumerate(select):
            stmt = re.split('\s|(?<!\d)[,.](?!\d)', stmt)
            stmt = list(filter(None, stmt))
            pattern = re.compile('\A(\w\s+)*(AVG)\s*\(\s*w*')
            for j, word in enumerate(stmt):
                if pattern.match(word): 
                    word = re.sub("AVG", "", word)
                    newSelect = word.replace(word," SUM" + word + ", " +  "COUNT" + word + "")
                    try:
                        if stmt[j + 1]: 
                            newSelect += ", "
                    except IndexError:
                        pass
                    stmt[j] = newSelect.strip()
            stmt = ' '.join(str(word) for word in stmt)
            select[i] = stmt
        return(select)

    def ensureTimeSeries(self, where):
        if any("EVENTTIME" in string for string in where):
            return(True)
        else:
            return(False)

    def mergeStmts(self, select, tables, where):
        stmt = ""
        for i, word in enumerate(select):
            stmt += word + " " + tables[i]
            try:
                stmt += " " + where[i] + " "
            except IndexError:
                pass
        print(stmt)
        #print(select[1])
        #print(tables)
        #print(where)

def main():
    #this sql query causes a bug
    test = SqlAST("SELECT AVG(roy), AVG(dog), Cat FROM turbine WHERE EventTime > 6 AND SELECT(dog) from cat where babe = 0 AND EventTime < 4;")
    select, tables, where = test.parse()
    #print(select)
    if test.ensureTimeSeries(where):
        select = test.evalSelect(select)
        query = test.mergeStmts(select, tables, where)
        
    else:
        print("Unsupported query. Must have time-interval.")
    #print(select, "\n", tables, "\n", where)
    #print(''.join(stmt))
    #final = test.convert(result)
    #print(final)

if __name__ == '__main__':
    main()
