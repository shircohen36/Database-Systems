
# coding: utf-8

# In[68]:

import csv
import os


# In[69]:

# check type of values in each coulumn
def checkType(data):
    newData=list(data)
    valueTypeArray=newData.pop(0)
    valueTypeArray=[0 for i in range (0,len(valueTypeArray))]
    for row in newData:
        for i in range (0,len(row)):
            item=row[i]
            try: 
                int(item)
            except ValueError:
                if valueTypeArray[i]==0:
                    valueTypeArray[i]=1
                valueTypeArray[i]=max(valueTypeArray[i],len(item)) 
    return valueTypeArray


# In[70]:

# write the sql file from data file
def writeDataSqlFile(fscheme,fdata,data,tableName,valueTypeArray):
    
    fscheme.write("CREATE TABLE %s (\n" % tableName)
    headline=data.pop(0)
        
    # create table
    fscheme.write("\tID INT NOT NULL AUTO_INCREMENT,\n")
    for i in range (0,len(headline)-1):
        item=headline[i]
        item=item.replace(" ","_")
        if valueTypeArray[i]==0:
            fscheme.write("\t%s INT,\n" % item)
        else:
            if "comment" in item or "discription" in item or valueTypeArray[i]>1500:
                fscheme.write("\t%s TEXT,\n" % item)
            elif item=="name":
                valueTypeArray[i]+=16
                fscheme.write("\t{0} VARCHAR({1}) NOT NULL,\n".format(item,valueTypeArray[i]))
            else:
                valueTypeArray[i]+=16
                fscheme.write("\t{0} VARCHAR({1}),\n".format(item, valueTypeArray[i]))
    fscheme.write("\tPRIMARY KEY (ID)\n")
    fscheme.write(");\n\n")
        
    # insert values to table
    for row in data:
        fdata.write("INSERT INTO %s VALUES (NULL," % tableName)
        for i in range (0,len(row)-1):
            item=row[i]
            item=item.replace("\'","\''")
            if valueTypeArray[i]==0:
                item=int(item)
                fdata.write("%d" % item)
            else:
                fdata.write('\'')
                fdata.write("%s" % item)
                fdata.write('\'')
            if i<len(headline)-2:
                fdata.write(",")
        fdata.write(");\n")
    fdata.write("\n")


# In[ ]:

# write the sql file from match file
def writeMatchSqlFile(fscheme,fdata,data,tableName,valueTypeArray):
   
    fscheme.write("CREATE TABLE %s (\n" % tableName)
    headline=data.pop(0)
        
    # create table
    for i in range (0,len(headline)):
        item=headline[i]
        item=item.replace(" ","_")
        fscheme.write("\t%s INT\n" % item)
        refTable=item.split("_ID")[0]
        fscheme.write("\t\tREFERENCES %s(ID)" % refTable)
        if i<len(headline)-1:
            fscheme.write (',\n')
        else:
            fscheme.write ('\n')
    fscheme.write(");\n\n")
        
    # insert values to table
    for row in data:
        fdata.write("INSERT INTO %s VALUES (" % tableName)
        for i in range (0,len(row)):
            item=row[i]
            item=int(item)
            fdata.write("%d" % item)
            if i<len(headline)-1:
                fdata.write(",")
        fdata.write(");\n")
    fdata.write("\n")


# In[71]:

# create tables from dir
def createDataTable(fscheme,fdata,dirpath):
    for filename in os.listdir(dirpath):
        filepath=dirpath+'/'+filename
        tableName=filename.split('.csv')[0]
        with open(filepath) as f2:
            data = list(csv.reader(f2))
            data.reverse
            f2.close
        valueTypeArray=checkType(data)
        writeDataSqlFile(fscheme,fdata,data,tableName,valueTypeArray)                  


# In[ ]:

# create tables from dir
def createMatchTable(fscheme,fdata,dirpath):
    for filename in os.listdir(dirpath):
        filepath=dirpath+'/'+filename
        tableName=filename.split('.csv')[0]
        with open(filepath) as f2:
            data = list(csv.reader(f2))
            data.reverse
            f2.close
        valueTypeArray=checkType(data)
        writeMatchSqlFile(fscheme,fdata,data,tableName,valueTypeArray) 


# In[ ]:

# write index file
def createIndex(f,dirpath):
        for filename in os.listdir(dirpath):
            tableName=filename.split('.csv')[0]
            f.write("CREATE INDEX nameIndex ON %s(name);\n" % tableName)       


# In[ ]:

# write all DB building queries into one SQL_DB file
def createSQLTables(dir1, dir2,dir3):
    outputSchemePath="SQL_DB/musicDB_scheme.sql"
    outputDataPath="SQL_DB/musicDB_data.sql"
    with open(outputSchemePath,'w') as fscheme:
        with open(outputDataPath,'w') as fdata:
            createDataTable(fscheme,fdata,dir1)
            createMatchTable(fscheme,fdata,dir2)
            createIndex(fscheme,dir3)
            fdata.close
        fscheme.close

