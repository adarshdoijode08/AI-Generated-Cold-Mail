import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills_or_text):
        if not skills_or_text:
            return []

        if isinstance(skills_or_text, list):
            query_texts = skills_or_text if skills_or_text else []
        elif isinstance(skills_or_text, str):
            query_texts = [skills_or_text]
        else:
            return []

        if not query_texts:
            return []

        result = self.collection.query(query_texts=query_texts, n_results=2)
        metadatas = result.get('metadatas', [])
        links = []
        for item in metadatas:
            if isinstance(item, list):
                for entry in item:
                    if isinstance(entry, dict) and entry.get('links'):
                        links.append(entry['links'])
            elif isinstance(item, dict) and item.get('links'):
                links.append(item['links'])
        return list(dict.fromkeys(links))