#######################################################################################
#  Create Lineage in Neo
#  Iteration 2:   Simple model using seperate notes for origin, provision point and usage point
#
#
#######################################################################################



from neo4j import GraphDatabase
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


#Create nodes and relationships using python driver

def add_data_element (driver, src_name, tgt_name):
    driver.execute_query(
        "MERGE (src:Data_Element {name: $src_name}) "
        "MERGE (tgt:Data_Element {name: $tgt_name}) "
        "MERGE (src)-[:HAS_DIRECT_DATA_FLOW]->(tgt)",
        src_name=src_name, tgt_name=tgt_name, database_="neo4j",
    )

#Set Properties
def set_source_of_origin (driver, src_name):
    driver.execute_query(
        "MATCH (n {name: $src_name}) "
        "SET n.SoureOfOrigin = 'Y' "
        "RETURN n.name, n.SoureOfOrigin",
        src_name=src_name,  database_="neo4j"
    )


def add_focal_point (driver, src_name, tgt_name):
    driver.execute_query(
        "MERGE (src:Data_Element {name: $src_name}) "
        "MERGE (tgt:Focal_Point {name: $tgt_name}) "
        "MERGE (src)-[:FOCAL_POINT_FOR]->(tgt)",
        src_name=src_name, tgt_name=tgt_name, database_="neo4j",
    )


def add_BusinessTerm (driver, src_name, tgt_name):
    driver.execute_query(
        "MERGE (src:BT {name: $src_name}) "
        "MERGE (tgt:Data_Element {name: $tgt_name}) "
        "MERGE (src)-[:LOGICALLY_LINKS_TO]->(tgt)",
        src_name=src_name, tgt_name=tgt_name, database_="neo4j",
    )

def add_BusinessObjective_DE(driver, src_name, tgt_name):
    driver.execute_query(
        "MERGE (src:BO {name: $src_name}) "
        "MERGE (tgt:Data_Element {name: $tgt_name}) "
        "MERGE (src)-[:LOGICALLY_LINKS_TO]->(tgt)",
        src_name=src_name, tgt_name=tgt_name, database_="neo4j",
    )

def add_BusinessObjective_FP(driver, src_name, tgt_name):
    driver.execute_query(
        "MERGE (src:BO {name: $src_name}) "
        "MERGE (tgt:BT {name: $tgt_name}) "
        "MERGE (src)-[:LOGICALLY_LINKS_TO]->(tgt)",
        src_name=src_name, tgt_name=tgt_name, database_="neo4j",
    )


#instantiate and wrap in CRUD functions
def add_nodes ():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        #add_data_element
        add_data_element(driver, "SS_THING_Name", "IH_THING_Name")
        add_data_element(driver, "IH_THING_Name", "EDW_STG_THING_Name")
        add_data_element(driver, "EDW_STG_THING_Name", "ACQ_THING_name")
        add_data_element(driver, "ACQ_THING_name", "IL_TX_THING_name")
        add_data_element(driver, "ACQ_THING_name", "IL_SAT_THING_name")
        add_data_element(driver, "ACQ_THING_name", "IL_LINK_THING_name")
        add_data_element(driver, "ACQ_THING_name", "IL_HUB_THING_name")
        add_data_element(driver, "IL_TX_THING_name", "CBB_THING_name")
        add_data_element(driver, "IL_SAT_THING_name", "CBB_THING_name")
        add_data_element(driver, "IL_LINK_THING_name", "CBB_THING_name")
        add_data_element(driver, "IL_HUB_THING_name", "CBB_THING_name")
        add_data_element(driver, "CBB_THING_name", "CNS_THING_name")
        add_data_element(driver, "CNS_THING_name", "APP_CNS_THING_name")

        #add_focal_point to Data elements
        add_focal_point(driver, "SS_THING_Name", "Source_of_Origin")
        add_focal_point(driver, "CNS_THING_name", "Provisioning_Point")
        add_focal_point(driver, "APP_CNS_THING_name", "Source_of_Usage")

        #add_BusinessTerm to Data elements
        add_BusinessTerm(driver, "THING Number", "SS_THING_Name")
        add_BusinessTerm(driver, "THING Number", "IH_THING_Name")
        add_BusinessTerm(driver, "THING Number", "EDW_STG_THING_Name")
        add_BusinessTerm(driver, "THING Number", "ACQ_THING_name")
        add_BusinessTerm(driver, "THING Number", "IL_TX_THING_name")
        add_BusinessTerm(driver, "THING Number", "IL_SAT_THING_name")
        add_BusinessTerm(driver, "THING Number", "IL_LINK_THING_name")
        add_BusinessTerm(driver, "THING Number", "IL_HUB_THING_name")
        add_BusinessTerm(driver, "THING Number", "CBB_THING_name")
        add_BusinessTerm(driver, "THING Number", "APP_CNS_THING_name")

        # add_BusinessObjective to Data elements
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "SS_THING_Name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "IH_THING_Name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "EDW_STG_THING_Name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "ACQ_THING_name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "IL_TX_THING_name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "IL_SAT_THING_name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "IL_LINK_THING_name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "IL_HUB_THING_name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "CBB_THING_name")
        add_BusinessObjective_DE(driver, "OBJECTIVE_1", "APP_CNS_THING_name")
                                 
        
        # add_BusinessObjective to Focal Points

        add_BusinessObjective_FP(driver, "OBJECTIVE_1", "Source_of_Origin")
        add_BusinessObjective_FP(driver, "OBJECTIVE_1", "Provisioning_Point")
        add_BusinessObjective_FP(driver, "OBJECTIVE_1", "Source_of_Origin")

#execution
add_nodes()

# Match (n: Data_Element) DETACH DELETE n