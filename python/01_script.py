import os
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI


from neo4j import GraphDatabase, RoutingControl
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

neo4j_user = os.getenv('NEO4J_USERNAME')
neo4j_password = os.getenv('NEO4J_PASSWORD')
neo4j_uri = os.getenv('NEO4J_URI')

URI = neo4j_uri
AUTH = (neo4j_user, neo4j_password)



# scafold 
graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)

graph.refresh_schema()
chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True
)

#chain.run("How many employees are there in total?")
#chain.invoke("How many burlgary crimes are there?")

chain.invoke("How many nodes are there?")

