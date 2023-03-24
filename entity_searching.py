import pytest
from EntitySearching import EntitySearching


class Test:
    def test_base_search():
        nlp = spacy.load("en_core_web_sm")
        query = "What is the weather like in London today?"
        parent = None
        threshold = 0.6
        relation = None
        es = EntitySearching(nlp, query, parent,
                             threshold, relation, base=True)
        expected_result = {"entityClass": "location",
                           "token": "London", "parentClass": None}
        assert len(es.result[1]) == 1
        assert es.result[1][0]["entityClass"] == "location"
        assert es.result[1][0]["token"] == "London"
        assert es.result[1][0]["parentClass"] is None

    def test_EntitySearching_custom_search():
        nlp = spacy.load('en_core_web_sm')
        query = "What is the weather like in London today"
        parent = "location"
        threshold = 0.7
        es = EntitySearching(nlp, query, parent, threshold)
        expected_result = {"entityClass": "location", "token": "London",
                           "identifier": "London", "parentClass": None}
        assert len(es.result[1]) == 1
        assert es.result[1][0]["entityClass"] == "location"
        assert es.result[1][0]["token"] == "London"
        assert es.result[1][0]["identifier"] == "London"
        assert es.result[1][0]["parentClass"] is None

    def test_filter_result():
        nlp = spacy.load('en_core_web_sm')
        query = "What is the weather like in London today"
        parent = "location"
        threshold = 0.7
        es = EntitySearching(nlp, query, parent, threshold,None,"location")
        
        result = {
                    "entityClass": "Location",
                    "token": "London",
                    "identifier": "London",
                    "parentClass": None,
                    "metaData": {"matcher": "none", "identifier": "London"}
                }
        es.result = result
        filtered_result = es.filter_result()
        
        assert len(filtered_result) == 2
        assert filtered_result['London'][0] == ('London', None, 'Location', 'none')