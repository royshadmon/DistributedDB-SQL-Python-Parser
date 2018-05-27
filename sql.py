#http://www.jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3

import re
from connectdb import runDB

class SelectSqlAST(object):
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
            print(where)
            return(True)
        else:
            return(False)

    def mergeStmts(self, select, tables, where):
        stmt = ""
        for i, word in enumerate(select):
            stmt += word + " " + tables[i]
            stmt += " " + where[i] + " "
        return(stmt)


class CreateSqlAST(object):
    def __init__(self, create):
        self.create = create.upper()

    def parse(self):
        self.create = re.split('CREATE\s+TABLE\s+[A-Z]+[A-Z0-9]*\s*\(\s*', self.create)
        self.create = re.split('\,|\)|\;', self.create[1])
        return (self.create)

    def ensureTimeSeries(self):
        TIMEpattern = re.compile('(EVENTTIME)\s+(DATE)')
        for i, word in enumerate(self.create):
            if TIMEpattern.match(word.strip()):
                print("yes")
                return(True)
        return(False)


class runQuery(object):
    def __init__(self, query):
        self.query = query

    def evalQuery(self):
        run = runDB(self.query)
        return run.selectStmt()



def main():
    #this sql query causes a bug
    test = SelectSqlAST("Select AVG(temperature), pressure from turbine where EventTime < '2019-01-01' AND Select temperature from turbine where dog < 2;")
    select, tables, where = test.parse()
    print(where)
    if test.ensureTimeSeries(where, select):
        select = test.evalSelect(select)
        query = test.mergeStmts(select, tables, where)
        #run = runQuery(query)
        #run.evalQuery()
    else:
        print("Unsupported query. Must have time-interval.")

    #query = "Create table roy2232 (roy int, dog varchar(255), eventtime date, lake time);"
    #create = CreateSqlAST(query)
    #parsedCreate = create.parse()
    #if create.ensureTimeSeries():
    #    run = runQuery(query)
    #    run.evalQuery()
    #else:
    #    print("Must create table with `EventTime' as a column name")

if __name__ == '__main__':
    main()
