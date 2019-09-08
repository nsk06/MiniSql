import os,sys,csv,copy
import sqlparse
Tables = {}
meta = {}
final_answer = []
cols = []
Join_data_col = {}
Join_data_row = []
def readmetadata(filename):
    global meta
    with open(filename) as f:
        lines = f.readlines()
    lines = [i.strip('\n') for i in lines]
    # print(lines)
    check = False
    for line in lines:
        if(line=="<begin_table>"):
            check=True
            continue
        elif(line=="<end_table>"):
            meta[cur_table]=mytablelist
            continue
        else:
            if(check==True):
                cur_table=line
                check=False
                mytablelist = []
            else:
                mytablelist.append(line)
    return meta
def tables():
    global Tables
    metadata = readmetadata('metadata.txt')
    for table in metadata:
        tabledata = []
        filename = str(table)+'.csv'
        try:
            with open(filename) as tablecsv:
                data = csv.reader(tablecsv)
                # tabledata.append(metadata[table])
                for rows in data:
                    cur_table_row = {}
                    for i in range(0,len(rows)):
                        cur_table_row[metadata[table][i]]= rows[i]
                    tabledata.append(cur_table_row)
            Tables[table]=tabledata             
        except:
            print("No File For table",table)
            sys.exit(-1)
def checkint(val):
    try:
        int(val)
        return True
    except:
        return False
def handlewherequeries(tables,wherequery):
    global final_answer
    ops = ['<','>','=','>=','<=']
    wherequery = wherequery[6:].strip(';')
    lt = wherequery.lower().split(' ')
    lto = wherequery.split(' ')
    # if(len(lt)==0):
    #     print("Incorrect Syntax")
    #     sys.exit(-1)
    if("and" in lt):
        pos = lt.index("and")
        cond1 = ''.join(lto[0:pos])
        cond2 = ''.join(lto[pos+1:])
        for o in ops:
            if o in cond1:
                op1 = o
                temp = cond1.split(o)
                col1 = temp[0]
                val1 = temp[1]
            if o in cond2:
                op2 = o
                temp = cond2.split(o)
                col2 = temp[0]
                val2 = temp[1]
        # print(col1,val1,col2,val2,op1,op2)
        cur_cols = matchtablecolumns(tables,[col1,col2])
        # print(cur_cols)
        if(not checkint(val1)):
            cond1col2 = val1
            cond1col2 = matchtablecolumns(tables,[cond1col2])[0]
        if(not checkint(val2)):
            cond2col2 = val2 
            cond2col2 = matchtablecolumns(tables,[cond2col2])[0]
        if(op1=="="):
            op1="=="
        if(op2=="="):
            op2="=="
        col1 = cur_cols[0]
        col2 = cur_cols[1]
        templist = []
        if(checkint(val1) and checkint(val2)):
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col1):
                        if(eval(e[1]+op1+val1)):
                            ct1 = True
                        else:
                            ct1=False
                            break
                    if(e[0]==col2):
                        if(eval(e[1]+op2+val2)):
                            ct2 = True
                        else:
                            ct2=False
                            break
                if(ct1==True and ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)
        elif(checkint(val1)==True and checkint(val2)==False):
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col1):
                        if(eval(e[1]+op1+val1)):
                            ct1 = True
                        else:
                            ct1=False
                            break
                    if(e[0]==col2):
                        for i in rows:
                            if(i[0]==cond2col2):
                                if(eval(e[1]+op2+i[1])):
                                    ct2=True
                                else:
                                    ct2=False
                                    break
                        if(ct2==False):
                            break
                if(ct1==True and ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)
        elif(checkint(val1)==False and checkint(val2)==True):
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col2):
                        if(eval(e[1]+op2+val2)):
                            ct2 = True
                        else:
                            ct2=False
                            break
                    if(e[0]==col1):
                        for i in rows:
                            if(i[0]==cond1col2):
                                if(eval(e[1]+op1+i[1])):
                                    ct1=True
                                else:
                                    ct1=False
                                    break
                        if(ct1==False):
                            break
                if(ct1==True and ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)
        elif(checkint(val1)==False and checkint(val2)==False):
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col1):
                        for i in rows:
                            if(i[0]==cond1col2):
                                if(eval(e[1]+op1+i[1])):
                                    ct1=True
                                else:
                                    ct1=False
                                    break
                        if(ct1==False):
                            break
                    if(e[0]==col2):
                        for i in rows:
                            if(i[0]==cond2col2):
                                if(eval(e[1]+op2+i[1])):
                                    ct2=True
                                else:
                                    ct2=False
                                    break
                        if(ct2==False):
                            break
                if(ct1==True and ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)

        
    elif("or" in lt):
        pos = lt.index("or")
        cond1 = ''.join(lto[0:pos])
        cond2 = ''.join(lto[pos+1:])
        for o in ops:
            if o in cond1:
                op1 = o
                temp = cond1.split(o)
                col1 = temp[0]
                val1 = temp[1]
            if o in cond2:
                op2 = o
                temp = cond2.split(o)
                col2 = temp[0]
                val2 = temp[1]
        cur_cols = matchtablecolumns(tables,[col1,col2])
        col1 = cur_cols[0]
        col2 = cur_cols[1]
        templist = []
        if(op1=="="):
            op1="=="
        if(op2=="="):
            op2="=="
        if(not checkint(val1)):
            cond1col2 = val1
            cond1col2 = matchtablecolumns(tables,[cond1col2])[0]
        if(not checkint(val2)):
            cond2col2 = val2 
            cond2col2 = matchtablecolumns(tables,[cond2col2])[0]
        if(checkint(val1) and checkint(val2)):        
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col1):
                        if(eval(e[1]+op1+val1)):
                            ct1 = True
                        else:
                            ct1=False
                    if(e[0]==col2):
                        if(eval(e[1]+op2+val2)):
                            ct2 = True
                        else:
                            ct2=False
                if(ct1==True or ct2==True):
                    templist.append(rows)
            # print(templist)
            final_answer = copy.deepcopy(templist)
        elif(checkint(val1)==True and checkint(val2)==False):
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col1):
                        if(eval(e[1]+op1+val1)):
                            ct1 = True
                        else:
                            ct1=False
                    if(e[0]==col2):
                        for i in rows:
                            if(i[0]==cond2col2):
                                if(eval(e[1]+op2+i[1])):
                                    ct2=True
                                else:
                                    ct2=False
                if(ct1==True or ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)
        elif(checkint(val1)==False and checkint(val2)==True):
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col2):
                        if(eval(e[1]+op2+val2)):
                            ct2 = True
                        else:
                            ct2=False
                    if(e[0]==col1):
                        for i in rows:
                            if(i[0]==cond1col2):
                                if(eval(e[1]+op1+i[1])):
                                    ct1=True
                                else:
                                    ct1=False
                if(ct1==True or ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)
        elif(checkint(val1)==False and checkint(val2)==False): 
            for rows in final_answer:
                ct1=ct2=False
                for e in rows:
                    if(e[0]==col1):
                        for i in rows:
                            if(i[0]==cond1col2):
                                if(eval(e[1]+op1+i[1])):
                                    ct1=True
                                else:
                                    ct1=False
                    if(e[0]==col2):
                        for i in rows:
                            if(i[0]==cond2col2):
                                if(eval(e[1]+op2+i[1])):
                                    ct2=True
                                else:
                                    ct2=False
                if(ct1==True or ct2==True):
                    templist.append(rows)
            final_answer = copy.deepcopy(templist)       
    else:
        # print(wherequery)
        onecondition = wherequery
        onecondition = onecondition.split(' ')
        onecondition = ''.join(onecondition)
        for o in ops:
            if(o in onecondition):
                temp = onecondition.split(o)
                col1=temp[0]
                op1 = o
                val1 = temp[1]
        # print("here",col1)        
        col1 = matchtablecolumns(tables,[col1])[0]
        if(op1=="="):
            op1="=="
        if(checkint(val1)==False):
            condcol2 = val1
            condcol2 = matchtablecolumns(tables,[condcol2])[0]
        if(checkint(val1)):
            templist = []
            for rows in final_answer:
                for e in rows:
                    if(e[0]==col1):
                        if(eval(e[1]+op1+val1)):
                            templist.append(rows)
                            break
            # print(templist)
            final_answer = copy.deepcopy(templist)
        else:
            templist = []
            for rows in final_answer:
                for e in rows:
                    if(e[0]==col1):
                        for i in rows:
                            if(i[0]==condcol2):
                                if(eval(e[1]+op1+i[1])):
                                    templist.append(rows)
                                    break
            if(col1[col1.index('.')+1:]==condcol2[condcol2.index('.')+1:] and op1=="=="):#join
                finaltemp = []
                for r in templist:
                    rd = []
                    for e in r:
                        if(e[0]!=condcol2):
                            rd.append(e)
                    finaltemp.append(rd)
                final_answer = copy.deepcopy(finaltemp)
            else:
                final_answer = copy.deepcopy(templist)

def print_answer(cols):
    global final_answer
    ppt = []
    if(len(final_answer)>0):
        a = final_answer[0]
        for i in cols:
            for e in a:
                if(i==e[0]):
                    ppt.append(i)
    # print(ppt)
    cols = copy.deepcopy(ppt)
    print(','.join(cols))
    for rows in final_answer:
        ans=""
        for col in cols:
            for c in rows:
                if(c[0]==col):
                    ans+=c[1]
            if(cols.index(col)!=len(cols)-1):
                ans+=","
        print(ans)
def validate_tables(tables):
    for table in tables:
        if table in Tables:
            return True
        else:
            return False
def selectall():
    global cols
    cols = ["*"]
def matchtablecolumns(tables,cols):
    global final_answer,Join_data_col
    allcol_list = []
    for table in tables:
        mycols = meta[table]
        for i in mycols:
            allcol_list.append(table+'.'+i)
    if(len(cols)==0):
        return []
    elif(cols[0]=="*"):
        temp = []
        for table in tables:
            mycols = meta[table]
            for i in mycols:
                temp.append(table+'.'+i)
        return temp
    else:
        col_list = []
        # print(cols)
        for col in cols:
            colcheck=False
            for table in tables:
                allcols = meta[table]
                if(col in allcols):
                    if(colcheck==False):
                        col_list.append(table+'.'+col)
                        colcheck=True
                    else:
                        print("The Column ",col," is ambiguous")
                        sys.exit(-1)
                elif(col in allcol_list):
                        col_list.append(col)
                        break
        if(len(col_list)==0):
            print("No such column")
            sys.exit(-1)
        return col_list

def selectalljoin(tables):
    global final_answer
    final_list = []
    if(len(tables)==1):
        cols=meta[tables[0]]
        cols = [str(tables[0])+'.'+i for i in cols]
        # final_answer.append(cols)
        for rows in Tables[tables[0]]:
            row_data = []
            for j in rows:
                row_data.append((str(tables[0])+'.'+j,rows[j]))
            final_list.append(row_data)
        return final_list
    else:
        multilist = []
        multilist = selectalljoin(tables[1:])
        for i in Tables[tables[0]]:
            for j in multilist:
                join_list = copy.deepcopy(j)
                for k in i:
                    join_list.append((str(tables[0])+'.'+k,i[k]))
                final_list.append(join_list)
    return final_list
def distincttoken(dist_cols,tables):
    global final_answer
    templist = []
    # print(dist_cols)
    for rows in final_answer:
        row_data = []
        rd=""
        for c in dist_cols:
            for i in rows:
                if(i[0]==c):
                   row_data.append(i)
                   break
        templist.append(row_data)
    templist = list(set(map(tuple,templist)))
    # print(templist)
    # templist = list(set(templist))
    final_answer = copy.deepcopy(templist)
def columnstoredata(tables):
    global Join_data_row,Join_data_col
    col_list = matchtablecolumns(tables,["*"])
    for i in col_list:
        Join_data_col[i]=[]
    # print(Join_data_row)
    for rows in Join_data_row:
        for c in rows:
            Join_data_col[c[0]].append(int(c[1]))
    # print(Join_data_col)   
def wherewithfunctions(tables):
    global final_answer,Join_data_col
    # ops = ['<','>','=','>=','<=']
    # wherequery = wherequery[6:].strip(';')
    # lt = wherequery.lower().split(' ')
    # lto = wherequery.split(' ')
    # templist = []
    templist = copy.deepcopy(Join_data_col)
    for i in templist:
        templist[i] = []
    for rows in final_answer:
        for e in rows:
            templist[e[0]].append(e[1])
    Join_data_col = copy.deepcopy(templist)

def evaluatefunction(tables,functioncols):
    global meta
    if(len(tables)>1):
        print("Not supported on multiple tables")
        sys.exit(-1)
    col_list = matchtablecolumns(tables,["*"])    
    col_func = str(functioncols)
    if('(' not in col_func or ')' not in col_func  ):
        print("Wrong Syntax....")
        sys.exit(-1)
    else:
        col_func = col_func[col_func.index('(')+1:col_func.index(')')]
        mycols = meta[tables[0]]
        if(col_func in mycols):
            col_func = tables[0] + '.' + col_func
            # col_func = "max"+ "(" + col_func +')'
            # print(col_func)
        elif(col_func in col_list):
            # print(col_func)
            pass
        else:
            print("No such column")
            sys.exit(-1)
        # print(functioncols)
        functioncols = str(functioncols)
        if("max" in functioncols):
            ans = max(Join_data_col[col_func])
            col_func = "max"+ "(" + col_func +')'
            print(col_func)
            print(ans)
        elif("min" in functioncols):
            ans = min(Join_data_col[col_func])
            col_func = "min"+ "(" + col_func +')'
            print(col_func)
            print(ans)
        elif("sum" in functioncols):
            ans = sum(Join_data_col[col_func])
            col_func = "sum"+ "(" + col_func +')'
            print(col_func)
            print(ans)
        elif("avg" in functioncols):
            ans = sum(Join_data_col[col_func])/float(len(Join_data_col[col_func]))
            col_func = "avg"+ "(" + col_func +')'
            print(col_func)
            print(ans)
        elif("distinct" in functioncols):
            ans = list(set(Join_data_col[col_func]))
            ol_func = "distinct"+ "(" + col_func +')'
            print(col_func)
            for a in ans:
                print(a)
        # print(col_func)
    # if("max" in functioncols)
def Query(query):
    global final_answer,cols,Join_data_col,Join_data_row
    query = ' '.join(query.split())
    query = sqlparse.parse(query)[0]
    if(str(query.tokens[0]).upper()!="SELECT"):
        print("This type of query is not supported")
        sys.exit(-1)
    token2type=""
    i=2
    # print(query.tokens)
    if(query.tokens[2]!=None):
        if("distinct" in str(query.tokens[2]).lower() and type(query.tokens[2]).__name__=="Token"):
            token2type="distinct"
            i+=2
            distinct_cols_token = str(query.tokens[4]).split(',')
        elif(type(query.tokens[i]).__name__=="Token" and str(query.tokens[2]).lower()=="*"):
            token2type="all"
            selectall()
        elif(type(query.tokens[i]).__name__=="Function"):
            token2type="function"
            functioncols = (query.tokens[i])
        else:
            token2type="columns"
            cols = str(query.tokens[i]).split(',')
            temp = []
            for c in cols:
                temp.append(c.replace(' ',''))
            cols = copy.deepcopy(temp)
            # print("hre",cols)
    else:
        print("Incorrect Syntax....")
        sys.exit(-1)
    i+=4
    if(i<len(query.tokens)):
        tables = str(query.tokens[i])
        tables = tables.split(',')
    else:
        print("Incorrect Syntax....")
        sys.exit(-1)
    wheretype=False
    i+=2
    # print(query.tokens[i])
    if(i<len(query.tokens)):
        if("where" in str(query.tokens[i]).lower()):
            wheretype=True
            wherequery = str(query.tokens[i])
            i+=2
    if(validate_tables(tables)==False):
        print("No such table in database.Check your query again...")
        sys.exit(-1)
    else:
        final_answer = selectalljoin(tables)
        Join_data_row = selectalljoin(tables)
        columnstoredata(tables)
        # print(cols)
        if(token2type=="all"):
            # selectall()
            cols = matchtablecolumns(tables,cols)
            pass
        elif(token2type=="columns"):
            cols=matchtablecolumns(tables,cols)            
        elif(token2type=="distinct"):
            dist_cols = matchtablecolumns(tables,distinct_cols_token)
            distincttoken(dist_cols,tables)
            cols = dist_cols
        elif(token2type=="function"):
            if(wheretype==False):
                evaluatefunction(tables,functioncols)
                return
        if(wheretype==True):
            handlewherequeries(tables,wherequery)
        if(token2type=="function" and wheretype==True):
            wherewithfunctions(tables)
            evaluatefunction(tables,functioncols)
            return
    # print(cols)
    print_answer(cols)

        
if __name__ == "__main__":
    tables()
    # print(meta)
    if(len(sys.argv)<2):
        print("Please Enter the query as command line arguement")
    else:
        try:
            Query(sys.argv[1])
        except:
            print("You have an error in your SQL syntax; "
                   "check the manual for the right syntax to use.")
            sys.exit(-1)

