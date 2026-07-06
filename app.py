import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.chains import LLMMathChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.agents import Tool, initialize_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Load environment variables (e.g. from .env file)
load_dotenv()

## Set up the Streamlit app
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant",page_icon="🧮")
st.title("Text To Math Problem Solver Using Llama 3.3")

# Use env variable if available as default
default_api_key = os.getenv("GROQ_API_KEY", "")
groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password",value=default_api_key)


if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

llm=ChatGroq(model="llama-3.3-70b-versatile",groq_api_key=groq_api_key)


## Initializing the tools
wikipedia_wrapper=WikipediaAPIWrapper()
def wikipedia_search(query: str) -> str:
    return wikipedia_wrapper.run(query)

wikipedia_tool=Tool(
    name="Wikipedia",
    func=wikipedia_search,
    description="A tool for searching the Internet to find the various information on the topics mentioned"
)

## Initialize the Math tool
math_chain=LLMMathChain.from_llm(llm=llm)
def calculate(query: str) -> str:
    return math_chain.run(query)

calculator=Tool(
    name="Calculator",
    func=calculate,
    description="A tools for answering math related questions. Only input mathematical expression need to be provided"
)

prompt="""
You are an agent tasked for solving users mathematical question. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below
Question:{question}
Answer:
"""

prompt_template=PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combine all the tools into chain
chain=LLMChain(llm=llm,prompt=prompt_template)
def reason(query: str) -> str:
    return chain.run(query)

reasoning_tool=Tool(
    name="Reasoning tool",
    func=reason,
    description="A tool for answering logic-based and reasoning questions."
)

## initialize the agents

assistant_agent=initialize_agent(
    tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi, I'm a Math chatbot who can answer all your maths questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

## Lets start the interaction
question=st.text_area("Enter your question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

if st.button("find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(question,callbacks=[st_cb]
                                         )
            st.session_state.messages.append({'role':'assistant',"content":response})
            st.write('### Response:')
            st.success(response)

    else:
        st.warning("Please enter the question")









