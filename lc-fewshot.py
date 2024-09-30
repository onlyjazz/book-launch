from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI model
model = ChatOpenAI(model="gpt-4o")

# Define few-shot examples
examples = [
    {
        "input": "The quick brown fox jumps over the lazy dog.",
        "output": "A fast auburn canine leaps above an idle hound."
    },
    {
        "input": "To be or not to be, that is the question.",
        "output": "Existence or nonexistence, therein lies the inquiry."
    }
]

# Create a few-shot prompt template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=ChatPromptTemplate.from_template(
        "Input: {input}\nOutput: {output}"
    ),
    suffix="Input: {input}\nOutput:",
    input_variables=["input"]
)

# Create a full prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that paraphrases sentences."),
    ("human", few_shot_prompt)
])

# Create a chain
chain = prompt | model | StrOutputParser()

# Use the chain
result = chain.invoke({
    "input": "Life is like a box of chocolates, you never know what you're gonna get."
})

print(result)