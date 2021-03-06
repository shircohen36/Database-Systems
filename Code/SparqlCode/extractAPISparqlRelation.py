from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict

def splitString (st):
    if '**' in st:
        st=st.split("**")
        return st
    if '*' in st:
        st=st.split("*")
        return st
    if ',' in st:
        st=st.split(",")
        return st
    if ' - ' in st:
        st=st.split(" - ")
        return st
    if '|' in st:
        st=st.split("|")
        return st
    return [st]


def getTableFromQuery(typeTable,let,col,langlist,toGroup):
    headers="*"
    const=""
    langconst=""
    groupByconst=""
    sampleHeader="(Sample(?name) as ?name) "
    colName=col.split("/")[-1]
    if "#" in colName:
        colName=colName.split("#")[-1]
    const = "?type <"+col+"> ?"+colName+". "
    if toGroup:
        sampleHeader+="(Sample(?"+colName+") as ?"+colName+") "
    if toGroup:
        groupByconst="GROUP BY ?type"
        headers = "?type "+sampleHeader
    if colName in langlist:
        langconst += "FILTER langMatches(lang(?"+colName+"),"+"\"en\""+"). "

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX : <http://dbpedia.org/resource/>
        PREFIX dbpedia2: <http://dbpedia.org/property/>
        PREFIX dbpedia: <http://dbpedia.org/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT """+headers+""" WHERE{
            ?type a dbo:"""+typeTable+""".
            ?type foaf:name ?name. """
            + const + """
            FILTER regex(?name,"""+let+""","i").
            """+ langconst+"""
            }"""+groupByconst+"""
            ORDER BY ?type
     """)
 #   print (sparql.queryString)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def createRelationTable(tableName,tableType,columnlist,langlist):

    tavRange=[['a','z'],['1','9']]

    fileName="RelationTables/"+tableName+".csv"
    with open(fileName,'w') as f:

        ## write headers ##
        headers=tableName.split("_")
        f.write("{0},{1}\n".format(headers[0],headers[1]))

        for rng in tavRange:
            startR=ord(rng[0])
            endR=ord(rng[1])+1

            for tav in range(startR, endR):
                let="\""+"^"+chr(tav)+"\""

                for col in columnlist:
                    results=getTableFromQuery(tableType,let,col,langlist,False) #return query

                ## write rows ##
                    for result in results["results"]["bindings"]:
                        rowname=result["name"]["value"]
                        try:
                            rowname=rowname.replace(",",";")
                            rowname=rowname.encode("utf-8")
                        except: #don't print line if name encoding is bad
                            continue
                        col=col.split("/")[-1]
                        if "#" in col:
                            col=col.split("#")[-1]
                        colvalue=result[col]["value"]
                        colvalue=splitString(colvalue)
                        for colName in colvalue:
                            if colName.isspace() or colName=='': #empty string
                                continue
                            if "/" in colName:
                                colName=colName.split('/')[-1]
                                colName=colName.replace('_',' ')
                            if '\n' in colName:
                                colName=colName.split('\n')[0]
                            try:
                                colName=colName.replace(",",";")
                                colName=colName.encode("utf-8")
                                f.write("{0},{1}\n".format(rowname,colName))
                            except:  #don't print if encoding is bad
                                f.write("{0},NULL\n".format(rowname))

        f.close()


def createCSVTables():

    print ("Creating Tables...\n\n")

  # tableName="MusicGenre_MusicSubGenre"
    # tableType="MusicGenre"
    # columns=["http://dbpedia.org/property/subgenres"]
    # langlist=["name","subgenres"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="MusicGenre_MusicDerivativeGenre"
    # tableType="MusicGenre"
    # columns=["http://dbpedia.org/property/derivatives"]
    # langlist=["name","derivatives"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="MusicGenre_MusicFusionGenre"
    # tableType="MusicGenre"
    # columns=["http://dbpedia.org/property/fusiongenres"]
    # langlist=["name","fusiongenres"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # tableName="MusicGenre_MusicStylisticOriginGenre"
    # tableType="MusicGenre"
    # columns=["http://dbpedia.org/property/stylisticOrigins"]
    # langlist=["name","stylisticOrigins"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="MusicalArtist_MusicGenre"
    # tableType="MusicalArtist"
    # columns=["http://dbpedia.org/property/genre","http://dbpedia.org/property/genres",
    #          "http://dbpedia.org/ontology/genre","http://dbpedia.org/property/musicGenre"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # tableName="Band_MusicGenre"
    # tableType="Band"
    # columns=["http://dbpedia.org/property/genre","http://dbpedia.org/property/genres",
    #          "http://dbpedia.org/ontology/genre","http://dbpedia.org/property/musicGenre"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # tableName="Song_MusicGenre"
    # tableType="Song"
    # columns=["http://dbpedia.org/property/genre","http://dbpedia.org/property/genres",
    #          "http://dbpedia.org/ontology/genre","http://dbpedia.org/property/musicGenre"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # tableName="Single_MusicGenre"
    # tableType="Single"
    # columns=["http://dbpedia.org/property/genre","http://dbpedia.org/property/genres",
    #          "http://dbpedia.org/ontology/genre","http://dbpedia.org/property/musicGenre"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # tableName="Album_MusicGenre"
    # tableType="Album"
    # columns=["http://dbpedia.org/property/genre","http://dbpedia.org/property/genres",
    #          "http://dbpedia.org/ontology/genre","http://dbpedia.org/property/musicGenre"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="Band_BandMembers"
    # tableType="Band"
    # columns=["http://dbpedia.org/property/currentMembers","http://dbpedia.org/property/currentMember",
    #          "http://dbpedia.org/property/bandMember","http://dbpedia.org/property/formerMembers"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="Song_Artists"
    # tableType="Song"
    # columns=["http://dbpedia.org/property/artist"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="Single_Artists"
    # tableType="Single"
    # columns=["http://dbpedia.org/ontology/musicalBand","http://dbpedia.org/ontology/musicalArtist","http://dbpedia.org/property/artist"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # tableName="Album_Artists"
    # tableType="Album"
    # columns=["http://dbpedia.org/ontology/musicalBand","http://dbpedia.org/ontology/musicalArtist",
    #          "http://dbpedia.org/property/artist"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="Song_Album"
    # tableType="Song"
    # columns=["http://dbpedia.org/property/Album"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="Single_Album"
    # tableType="Single"
    # columns=["http://dbpedia.org/property/Album"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")

    # tableName="MusicalArtist_AssociatedArtists"
    # tableType="MusicalArtist"
    # columns=["http://dbpedia.org/ontology/associatedMusicalArtist","http://dbpedia.org/ontology/associatedMusicalBand"]
    # langlist=["name"]
    # createRelationTable(tableName,tableType,columns,langlist)
    # print ("Table: "+tableName+" Completed!\n")
    #
    # print ("\nAll Tables Were Successfully Created!\n")
