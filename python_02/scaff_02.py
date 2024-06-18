# https://github.com/tomasonjo/blogs/blob/master/llm/neo4jvector_langchain_deepdive.ipynb

# pip install langchain openai wikipedia tiktoken neo4j langchain_openai

import os
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.document_loaders import WikipediaLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

os.environ["OPENAI_API_KEY"] = "sk-"



def read_wikipedia_article():
    ## block 1
    # Read the wikipedia article
    raw_documents = WikipediaLoader(query="The Witcher").load()
    # Define chunking strategy
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=20
    )
    # Chunk the document
    documents = text_splitter.split_documents(raw_documents)
    for d in documents:
        del d.metadata["summary"]
    return documents
## block 2



url = "bolt://54.236.226.158:7687"
username = "neo4j"
password = "radiuses-investment-college"

neo4j_db = Neo4jVector.from_documents(
    documents,
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    database="neo4j",  # neo4j by default
    index_name="wikipedia",  # vector by default
    node_label="WikipediaArticle",  # Chunk by default
    text_node_property="info",  # text by default
    embedding_node_property="vector",  # embedding by default
    create_id_index=True,  # True by default
)

neo4j_db.query("SHOW CONSTRAINTS")

## block 2
neo4j_db.query(
    """SHOW INDEXES
       YIELD name, type, labelsOrTypes, properties, options
       WHERE type = 'VECTOR'
    """
)


## block 2
neo4j_db.add_documents(
    [
        Document(
            page_content="LangChain is the coolest library since the Library of Alexandria",
            metadata={"author": "Tomaz", "confidence": 1.0}
        )
    ],
    ids=["langchain"],
)




## block 2
existing_index = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    index_name="wikipedia",
    text_node_property="info",  # Need to define if it is not default
)

print(existing_index.node_label)
print(existing_index.embedding_node_property)


## block 2

existing_index.query(
    """MATCH (w:WikipediaArticle {id:'langchain'})
       MERGE (w)<-[:EDITED_BY]-(:Person {name:"Galileo"})
    """
)

## block 2
retrieval_query = """
OPTIONAL MATCH (node)<-[:EDITED_BY]-(p)
WITH node, score, collect(p) AS editors
RETURN node.info AS text,
       score,
       node {.*, vector: Null, info: Null, editors: editors} AS metadata
"""

existing_index_return = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    database="neo4j",
    index_name="wikipedia",
    text_node_property="info",
    retrieval_query=retrieval_query,
)

## block 2
existing_index_return.similarity_search("What do you know about LangChain?", k=1)
