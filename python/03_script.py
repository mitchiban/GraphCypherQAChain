import os
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI


from neo4j import GraphDatabase, RoutingControl
from dotenv import load_dotenv

from langchain_core.prompts.prompt import PromptTemplate



load_dotenv()  # Load variables from .env file

neo4j_user = os.getenv('NEO4J_USERNAME')
neo4j_password = os.getenv('NEO4J_PASSWORD')
neo4j_uri = os.getenv('NEO4J_URI')


# change the default prompt
CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
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

chain.invoke("How many nodes are there?")