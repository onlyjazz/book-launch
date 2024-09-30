from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


#Initialize the OpenAI model
model = ChatOpenAI(model="gpt-3.5-turbo")

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Summarize the following text in {word_count} words: {text}")
])

# Create a chain
chain = prompt | model | StrOutputParser()

# Use the chain
result = chain.invoke({
    "word_count": "50",
    "text": "LangChain is a framework for developing applications powered by language models. It enables applications that are context-aware and reason-driven. LangChain provides memory, enables connections to other data sources, and allows language models to interact with their environment."
})

print(result)

