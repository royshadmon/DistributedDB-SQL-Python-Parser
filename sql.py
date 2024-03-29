import re
from connectdb import runDB

class SelectSqlAST(object):
    def __init__(self, query):
        self.query = query.upper()

    def select(self):
        return (self.query)

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
            AVGpattern = re.compile('\A(\w\s+)*(AVG)\s*\(\s*w*')
            SELpattern = re.compile('(SELECT)')
            for j, word in enumerate(stmt):
                if AVGpattern.match(word): 
                    word = re.sub("AVG", "", word)
                    newSelect = word.replace(word," SUM" + word + ", " +  "COUNT" + word + "")
                    try:
                        if stmt[j + 1]: 
                            newSelect += ", "
                    except IndexError:
                        pass
                    stmt[j] = newSelect.strip()
                elif not SELpattern.match(word) and (j < len(stmt) - 1):
                    stmt[j] = word + ","
            stmt = ' '.join(str(word) for word in stmt)
            select[i] = stmt
        return(select)

    def ensureTimeSeries(self, where, select):
        if len(select) == len(where) and all("EVENTTIME" in string for string in where):
            return(True)
        else:
            return(False)

    def mergeStmts(self, select, tables, where):
        stmt = ""
        for i, word in enumerate(select):
            stmt += word + " " + tables[i]
            stmt += " " + where[i] + " "
        return(stmt)

class runQuery(object):
    def __init__(self, query):
        self.query = query

    def evalQuery(self):
        run = runDB(self.query)
        return run.selectStmt()



def main():
    query = input('AnyLog # ')
    test = SelectSqlAST(query)
    select, tables, where = test.parse()
    if test.ensureTimeSeries(where, select):
        select = test.evalSelect(select)
        query = test.mergeStmts(select, tables, where)
        run = runQuery(query)
        run.evalQuery()
    else:
        print("Unsupported query. Must have time-interval.")

    main()

if __name__ == '__main__':
    main()
