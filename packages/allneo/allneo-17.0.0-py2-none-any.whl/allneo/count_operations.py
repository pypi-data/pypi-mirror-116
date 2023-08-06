from neo4j import GraphDatabase
import sys
##get conection or error 
def get_connect(uri,user,pwd):
    connect=0
    try:
        driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
        connect=1
    except Exception as error:
        print(error)
    if(connect==1):
        return (driver)
    else:
        print("please check your hostname , userid and password")
        
##get the count
def count_node(uri,user,pwd):  
        driver=get_connect(uri,user,pwd)
        if driver is not None:
            session=driver.session()
            count_query="""match (n) return count(n) as count"""
            count_result=session.run(count_query)
            for count in count_result:
                nodecount=count["count"]
            return nodecount
##get node with specific label count

    