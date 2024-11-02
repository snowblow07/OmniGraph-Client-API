import json
#from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from neo4j import GraphDatabase
from langchain_core.messages import SystemMessage, trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
# Google AI API key
import google.generativeai as genai
# LangChain Modules
#from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_core.output_parsers import StrOutputParser
#load module environment variables
from dotenv import load_dotenv
import datetime

#load the environment variables
load_dotenv()

# Neo4j database connection details
NEO4J_URI = os.environ.get("NEO4J_URI", "your_neo4j_uri_here")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "your_neo4j_password_here")

import os
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#from langchain_google_vertexai import ChatVertexAI

# Create a Neo4j driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Function to get chat history from Neo4j
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    #session_id = "hermes_" + session_id # Prepend "hermes_" to session_id
    with driver.session() as session:
        result = session.run("MATCH (n:SESSION {name: $session_id}) RETURN n", session_id=session_id)
        node = result.single()
        if node is None:
            session.run("CREATE (n:SESSION {name: $session_id, history: []})", session_id=session_id)
            history = []
        else:
            history = [json.loads(msg) for msg in node["n"]["history"]]
        
        chat_history = ChatMessageHistory()
        for msg in history:
            if msg["type"] == "human":
                chat_history.add_message(HumanMessage(content=msg["content"]))
            elif msg["type"] == "ai":
                chat_history.add_message(AIMessage(content=msg["content"]))
        
        return chat_history

# Function to update chat history in Neo4j
def update_session_history(session_id: str, message, message_type: str, ip: str, timestamp: str):
    message_json = json.dumps({
        "content": message,
        "type": message_type,
        "ip": ip,
        "timestamp": timestamp
    })
    with driver.session() as session:
        session.run(
            """
            MATCH (n:SESSION {name: $session_id})
            SET n.history = n.history + [$message]
            """,
            session_id=session_id, message=message_json
        )

# create a parser
parser = StrOutputParser()

# create a model
#model = ChatOllama(model="llama3.1")
#model = genai.GenerativeModel("gemini-1.5-flash")
model = ChatGoogleGenerativeAI(
#    model="gemini-3.1-pro-preview",
    model="gemini-flash-lite-latest",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# create a prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant. Answer all questions to the best of your ability.
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# create a prompt
#prompt = ChatPromptTemplate.from_messages(
#    [
#        (
#            "system",
#            "You are a helpful assistant. Answer all questions to the best of your ability.",
#        ),
#        MessagesPlaceholder(variable_name="messages"),
#    ]
#)
#chain = prompt | model

# function receive promt from user and return the answer
def agent(content, language="english", config="Visitor", ip="0.0.0.0"):
    '''
    This function receives a prompt from a user and returns the answer.
    Args:
        prompt: str: The prompt from the user.
        config: str: The session_id.
    Returns:
        answer: str: The answer from the model.
    '''

    # Get the current timestamp
    timestamp = datetime.datetime.now().isoformat()

    # create a trimmer to trim the messages
    trimmer = trim_messages(
        max_tokens=30000,
        strategy="last",
        token_counter=model,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    # Create a sample list of messages to test the trimmer
    #messages = [
    #    SystemMessage(content="you are a good assistant"),
    #    HumanMessage(content="hi! I'm bob"),
    #    AIMessage(content="hi!"),
    #    HumanMessage(content="I like vanilla ice cream"),
    #    AIMessage(content="nice"),
    #    HumanMessage(content="whats 2 + 2"),
    #    AIMessage(content="4"),
    #    HumanMessage(content="thanks"),
    #    AIMessage(content="no problem!"),
    #    HumanMessage(content="having fun?"),
    #    AIMessage(content="yes!"),
    #]

    # create a chain of prompt and model
    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | prompt | model
    )

    # invoke the chain
    #response = chain.invoke(
    #    {
    #        "messages": messages + [HumanMessage(content="what math problem did i ask")],
    #        "language": "English",
    #    }
    #)
    #print(response.content)

    # create a chat history
    #with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

    # Create a runnable with chat history
    with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

    # Create a config that we pass into the runnable every time. This config will contain the session_id.
    config = {"configurable": {"session_id": config}}

    # Invoke the chain in plain text
    response = with_message_history.invoke(
        {
            # use this if you want to lad the prefilled lest "messages"
            #"messages": messages + [HumanMessage(content="what was our last iteraction?")],
            "messages": [HumanMessage(content=content)],
            "language": language,
        }, 
        config=config,
    )

    # invo1que the chain using stream method
    #for r in with_message_history.stream(
    #    {
    #        "messages": [HumanMessage(content=content)],
    #        "language": language,
    #    },
    #    config=config,
    #):
    #    print(r.content, end="|")
    
    # Parse the response
    answer = parser.invoke(response)

    # Update the chat history in Neo4j with IP and timestamp
    update_session_history(config["configurable"]["session_id"], content, "human", ip, timestamp)
    update_session_history(config["configurable"]["session_id"], answer, "ai", ip, timestamp)

    return answer

# test the chat function
# print(agent("Hello I am Manny, tell me a joke", config="Manuel Rosero", language="english"))

# Print the history
#print("\nPrint chat history\n")
#with driver.session() as session:
#    result = session.run("MATCH (n:SESSION) RETURN n")
#    for record in result:
#        print(record["n"])

