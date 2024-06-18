#######################################################################################
#  Create Lineage in Neo
#  Iteration 
#
#
#######################################################################################






from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import os


# import variables
load_dotenv()  # Load variables from .env file
neo4j_user = os.getenv('NEO4J_USERNAME_F')
neo4j_password = os.getenv('NEO4J_PASSWORD_F')
neo4j_uri = os.getenv('NEO4J_URI_F')

#fit to script
uri = neo4j_uri
user = neo4j_user
password = neo4j_password

URI = neo4j_uri
AUTH = (neo4j_user, neo4j_password)

graph = Neo4jGraph(
    url=uri, 
    username=user, 
    password=password)


# change the default prompt
CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Additional context:
If the question is about origin, provisioning point or usage point, use both FOCAL_POINT_FOR relationship type to determine which data element is in context.

For how many questions - answer without the node name.




Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question} 

Important: In the generated Cypher query, the RETURN statement must explicitly include the property values used in the query's filtering condition, alongside the main information requested from the original question.

"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

graph.refresh_schema()
chain = GraphCypherQAChain.from_llm(cypher_prompt= CYPHER_GENERATION_PROMPT,llm=
    ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-0125"), graph=graph, verbose=True
)

#chain.invoke("How many data element nodes are there?") 
#chain.invoke("How many data elements are there?") # 10
chain.invoke("what is the source of origin?")
#chain.invoke("what is the source of usage?")


# chain.invoke("visualise the model") - CALL db.schema.visualization()
# MATCH p=()-[:HAS_DIRECT_DATA_FLOW|FOCAL_POINT_FOR]->() RETURN p


# MATCH p=()-[:FOCAL_POINT_FOR]->(n) WHERE n.name =~ '.*Origin.*' RETURN p (this is not using AI - is also case senstive)

# MATCH p=()-[:FOCAL_POINT_FOR]->(n) WHERE n.name =~ '.*(Usage|Provision|Origin).*' RETURN p