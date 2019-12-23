from elasticsearch_dsl import Document, Text, Keyword, Double, Integer, Date, Completion, analyzer, tokenizer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['10.28.238.105'])


# 豆瓣影视类型
class DoubanType(Document):
    # title = Text(
    #     analyzer=analyzer('ik_max_word')
    #
    # )
    # title_suggest = Completion(analyzer=analyzer('ik_max_word'))

    title = Text(
        analyzer=analyzer('ik_max_word'),
        fields={
            'suggest': Completion(
                analyzer=analyzer('ik_max_word')
            ),
        }
    )

    original_title = Text()

    douban_link = Text()
    rating = Double()
    genres = Keyword()
    country = Keyword()
    lang = Keyword()
    year = Integer()
    release_at = Date()
    runtime = Integer()
    season_count = Integer()
    imdb=Keyword()

    overview = Text(
        analyzer="ik_smart"
    )

    small_image = Text()
    # big_image = Text()

    directors = Keyword()
    writers = Keyword()
    casts = Keyword()

    class Index:
        # doc_type = 'douban'
        name = 'xingren'
        settings = {
            "number_of_shards": 3,
        }
