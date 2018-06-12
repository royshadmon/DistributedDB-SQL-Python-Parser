import re
from connectdb import runDB

class SelectSqlAST(object):
    def __init__(self, query):
        self.query = query.upper()

    def select(self):
        return (self.query)

    def parse(self):
        select, tables, where = [], [], []
        self.query = self.query.replace("(", " ")
        self.query = self.query.replace(")", " ")
        self.query = re.split(r'\s(?=(?:SELECT|FROM|WHERE)\b)', self.query)
        for i, part in enumerate(self.query):
            if "SELECT" in part:
                select.append(part.strip())
            if "FROM" in part:
                tables.append(part.strip())
            if "WHERE" in part:
                where.append(part.strip())
        return(select, tables, where)

    def evalSelect(self, select):
        for i, stmt in enumerate(select):
            stmt = re.split('\s|(?<!\d)[,.](?!\d)', stmt)
            stmt = list(filter(None, stmt))
            AVG = re.compile('AVG')
            SELpattern = re.compile('(SELECT)')
            PEEKparen = re.compile('[\s | \w]*\(\w*')
            SUMpattern = re.compile('(SUM)')
            COUNTpattern = re.compile('(COUNT)')
            for j, word in enumerate(stmt):
                word = word.strip()
                if AVG.match(word): 
                    word = re.sub("AVG", "", word)
                    word = word.replace(word," SUM(" + stmt[j+1] + "), " +  "COUNT(" + stmt[j+1] + ")")
                    stmt.remove(stmt[j+1])
                    try:
                        if stmt[j + 1]:
                            word += ", "
                    except IndexError:
                        pass
                    stmt[j] = word.strip()

                elif not SELpattern.match(word) and (j < len(stmt) - 1):
                    if SUMpattern.match(word) or COUNTpattern.match(word):
                        stmt[j] = word + "(" + stmt[j+1] + ")"
                        stmt.remove(stmt[j+1])
                        try:
                            if stmt[j+1]:
                                stmt[j] += ","
                        except IndexError:
                            continue
                    elif not PEEKparen.match(word):
                        stmt[j] = word + ","
                    else:
                        stmt[j] = word
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
            stmt += word + " " + tables[i] + " " + where[i]
            try:
                if select[i+1]: 
                    stmt += " ("
            except IndexError:
                pass
        i = 1
        stmt = stmt[:len(stmt)-1]
        while i < len(select):
            stmt += ")"
            i += 1
        stmt += ";"
        return(stmt)

def main():
    query = input('AnyLog # ')
    if len(query.strip()) == 0:
        main()
    sess = SelectSqlAST(query)
    hint = query.upper().strip().split(" ")
    if re.compile('(DROP)|(CREATE)|(INSERT)').match(hint[0]):
        main()
    else:
        select, tables, where = sess.parse()
        if sess.ensureTimeSeries(where, select):
            select = sess.evalSelect(select)
            query = sess.mergeStmts(select, tables, where)
            print(query.upper())
            main()
        else:
            print("Unsupported query. Must have time-interval.")
            main()

if __name__ == '__main__':
    main()
