from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from datetime import datetime

# Load model from Ollama
llm = ChatOllama(model="llama3.2")

# Embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load FAISS vector store safely
db = FAISS.load_local(
    folder_path="faiss_index",
    embeddings=embedding,
    allow_dangerous_deserialization=True  # ✅ Enable safe if YOU created the index
)

retriever = db.as_retriever(search_kwargs={"k": 4})

# Conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Date-aware prompt template
template = PromptTemplate.from_template("""
You are a helpful CRM assistant. Today's date is {date}.

Context:
{context}

Chat History:
{chat_history}

Question:
{question}

Answer:
""")

def get_chat_chain():
    today = datetime.now().strftime("%B %d, %Y")
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": template.partial(date=today)}
    )

# with SequentialChain

# from langchain.prompts import PromptTemplate
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.chains import RetrievalQA, LLMChain, SimpleSequentialChain
# from langchain_ollama import ChatOllama
# from langchain_core.documents import Document

# # 🧠 Set up embedding model and load FAISS vector store
# embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# db = FAISS.load_local("faiss_index", embeddings=embedding, allow_dangerous_deserialization=True)

# # 🤖 Connect to your local LLaMA server (via HuggingFaceEndpoint or a custom wrapper)
# llm = ChatOllama(model="llama3.2")

# # 🧩 Chain 1: Retrieval and Answering
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=db.as_retriever(),
#     return_source_documents=False,
#     chain_type="stuff"
# )

# # 🧩 Chain 2: Final Rewriting Prompt to Humanize Response
# formatter_prompt = PromptTemplate.from_template("""
# You are a helpful assistant responding to CRM-related queries.

# Rephrase the following content in a human-friendly, professional, natural tone:
# {response}

# Human-style summary:""")
# reformat_chain = LLMChain(llm=llm, prompt=formatter_prompt)

# # 🔗 Final Pipeline Chain: QA → Formatter
# chain = SimpleSequentialChain(
#     chains=[qa_chain, reformat_chain],
#     verbose=True
# )

# # 🔧 Function to return the chain
# def get_chat_chain():
#     return chain
