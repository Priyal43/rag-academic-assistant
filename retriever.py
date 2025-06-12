import chromadb

def retrieve_relevant_chunks(query, top_k=3):
    client = chromadb.PersistentClient(path="db/")
    collection = client.get_or_create_collection(name="papers")

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents)
