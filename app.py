import logging
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
#from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css,bot_template,user_template

logger = logging.getLogger('app')


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,
        chunk_overlap=60,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorsore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorsore


def get_chat_history(chat_history) -> str:
    buffer = ""
    if type(chat_history) == 'str':
        chat_history2 = chat_history.replace("AI:", "Assistant:")
        return chat_history2
    return buffer


def get_conversation_chain(vectorsore):
    llm = ChatOpenAI()
    memory = ConversationBufferWindowMemory(memory_key='chat_history', return_message=True, k=5)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorsore.as_retriever(),
        memory=memory,
        get_chat_history=get_chat_history
    )
    return conversation_chain


def handle_userinput(user_question):
    conversation_chain = st.session_state.conversation
    print(conversation_chain.memory.chat_memory.messages)
    response = st.session_state.conversation({'question': user_question})
    print(response)
    #st.write(response)
    st.write(bot_template.replace("{{MSG}}", response['answer']), unsafe_allow_html=True)
    st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)

    #历史记录倒序
    if response['chat_history'] != "":
        historys = response['chat_history'].split("\n")
        historys.reverse()
        for i, message in enumerate(historys):
            if i % 2 == 0:
                message = message.replace("AI:", "")
                st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)
            else:
                message = message.replace("Human:", "")
                st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple pdfs", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("chat with multiple pdfs :books:")
    user_question = st.text_input("Ask a question about your dockments:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("your documents")
        pdf_docs = st.file_uploader("upload your pdfs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                #get pdf text
                raw_text = get_pdf_text(pdf_docs)
                #get pdf text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)
                #create vector store
                vectors = get_vectorstore(text_chunks)
                # #create cinverstion chain
                st.session_state.conversation = get_conversation_chain(vectors)


if __name__ == '__main__':
    main()