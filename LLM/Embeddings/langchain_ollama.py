from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document

# Tratamento de arquivo, nesse caso era um txt com final |SEPARADOR|
def process_file(file_path: str):
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split("|SEPARADOR|")
            if parts:
                text = parts[0].strip() 
                if text:
                    text = text[1:-1]
                if text:
                    documents.append(Document(page_content=text))
    return documents

def start_embedding():
    # Carrega os documentos (pode ser um diretório ou um único arquivo)
    documents = process_file("mensagens.txt")
    print(f"{len(documents)} documentos carregados..")

    # Cria o vector store com ChromaDB
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")  # substitua por um modelo local se preferir
    vectorstore = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )


    print("Salvando no ChromaDB")
    batch_size = 500
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        vectorstore.add_documents(batch)
        print(f"Lote {i // batch_size + 1} de {len(documents) // batch_size + 1} adicionado.")

    print("Finalizado")