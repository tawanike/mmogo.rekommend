from elasticsearch_dsl import Document, Date, Integer, Keyword, Text


class Product(Document):
    title = Keyword()

    class Index:
        name = 'products'
        settings = {
            "number_of_shards": 3
        }
