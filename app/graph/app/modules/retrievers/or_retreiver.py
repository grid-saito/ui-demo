import os

from bs4 import BeautifulSoup as Soup
from faiss import IndexFlatL2
from langchain.indexes import SQLRecordManager, index
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders.recursive_url_loader import \
    RecursiveUrlLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from modules.models.langchain_azure import langchain_azure_embeddings_model


def extract_content(x):
    soup = Soup(x, "html.parser")
    return soup.text


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


namespace = "faiss/optibot"
db_path = "record_manager_cache.sql"

if os.path.exists(namespace):
    db = FAISS.load_local(
        namespace, langchain_azure_embeddings_model, allow_dangerous_deserialization=True
    )
else:
    record_manager = SQLRecordManager(
        namespace, db_url=f"sqlite:///{db_path}"
    )
    record_manager.create_schema()
    dimensions: int = len(langchain_azure_embeddings_model.embed_query("dummy"))
    db = FAISS(
        embedding_function=langchain_azure_embeddings_model,
        index=IndexFlatL2(dimensions),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        normalize_L2=False
    )

    # LCEL docs
    urls = [
        "https://scmopt.github.io/opt100/",
        "https://www.msi.co.jp/solution/nuopt/docs/techniques/index.html",
        "https://web.tuat.ac.jp/~miya/ipmemo.html"
    ]
    docs = []
    for url in urls:
        loader = RecursiveUrlLoader(
            url=url, max_depth=4, extractor=extract_content
        )
        docs.extend(loader.load())
    print("docs loaded")

    # # Sort the list based on the URLs and get the text
    # d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
    # d_reversed = list(reversed(d_sorted))
    # concatenated_content = "\n\n\n --- \n\n\n".join(
    #     [doc.page_content for doc in d_reversed]
    # )

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents(
        [x.page_content for x in docs],
        metadatas=[x.metadata for x in docs]
    )

    for i in range(len(texts) // 10):
        docs = texts[i*10:(i+1)*10]
        result = index(
            docs,
            record_manager,
            vector_store=db,
            cleanup="incremental",
            source_id_key="source",
        )
        print(f"indexed {i*10} to {(i+1)*10}: result {result}")
    db.save_local(namespace)


retriever = db.as_retriever()
