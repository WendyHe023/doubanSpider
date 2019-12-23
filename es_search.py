from elasticsearch import Elasticsearch

from xingren.models.es_types import DoubanType

if __name__ == "__main__":
    # s = DoubanType.search()
    #
    # s = s.suggest('title_suggestions', '肖', completion={'field': 'title.suggest'})
    # s = s.extra(_source='suggest')
    # # s = s.query('match', title='肖')
    #
    # response = s.execute()
    # # print(response.suggest.title_suggestions)
    #
    # completions = set(r['text'] for r in response.suggest.title_suggestions[0]['options'] if len(r['text']) > 0)
    # # completions = list(r['text'] for r in response.suggest.title_suggestions[0]['options'])
    # print(completions)
    client = Elasticsearch(hosts=["10.28.197.177"])
    key_word = '肖'
    page = 0
    response = client.search(
        index="xingren",
        body={
            "query": {
                "multi_match": {
                    "query": key_word,
                    "fields": ["title", "overview"]
                }
            },
        }
    )

    print(response['hits']['hits'])
