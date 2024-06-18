# https://github.com/tomasonjo/blogs/blob/master/llm/langchain_neo4j.ipynb

import os
from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

#block 1
graph = Neo4jGraph(
    url="bolt://44.202.7.166:7687", 
    username="neo4j", 
    password="possibilities-overlay-eddies")



#block 2
os.environ['OPENAI_API_KEY'] = "sk-"

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True,
)

#block 3  
"""Let's start with a simple test."""

chain.invoke({'query': """
Which intermediary is connected to most entites?
"""})


#block 4
"""Let's move on to the next example.."""

chain.invoke({'query':"""
Who are the officers of ZZZ-MILI COMPANY LTD.?
"""})


#block 5
"""a question that would utilize the power of graph databases."""

chain_improved.run("""
How are entities SOUTHWEST LAND DEVELOPMENT LTD. and Dragon Capital Markets Limited related?
""")

#block 6
"""gpt-3.5-turbo follows hints and instructions in the input. For example, we can ask it to find only the shortest path.."""

chain.invoke({'query':"""
How are entities SOUTHWEST LAND DEVELOPMENT LTD. and Dragon Capital Markets Limited connected?
Find a shortest path.
"""})


#block 7
"""Now that we dropped a hint that only the shortest path should be retrieved, we don't run into cardinality explosion troubles anymore. 
However, one thing I noticed is that the LLM sometimes doesn't provide the best results if a path object is returned. 
However, we can also fix that by instructing the model what information to use."""

chain.invoke({'query':"""
How are entities SOUTHWEST LAND DEVELOPMENT LTD. and Dragon Capital Markets Limited connected?
Find a shortest path.
Return only name properties of nodes and relationship types
"""})


#block 8
"""
Now we can a better response and more appropriate response. 
The more hints you drop to an LLM, the better results you can expect. 
For example, you can also instruct it which relationships it can traverse.
"""

chain.invoke({'query':"""
How are entities SOUTHWEST LAND DEVELOPMENT LTD. and Dragon Capital Markets Limited connected?
Find a shortest path and use only officer, intermediary, and connected relationships.
Return only name properties of nodes and relationship types
"""})