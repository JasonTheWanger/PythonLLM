import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("my_documents")

text = "Apples are red"
embedding = model.encode(text).tolist()  
collection.add(
    documents=[text],
    embeddings=[embedding],
    ids=["doc1"]
)

query = "What color are apples?"
query_vec = model.encode(query).tolist()
results = collection.query(query_embeddings=[query_vec], n_results=1, )

print(results)
