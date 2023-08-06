from ..wikipedia import Wikipedia

class TestInit:
    def test_valid(self):
        try:
            Wikipedia('강아지')
            assert True
        except:
            assert False
    
    def test_inavlid_no_search_text(self):
        try:
            Wikipedia()
            assert False
        except:
            assert True
    
    def test_invalid_syntax(self):
        try:
            Wikipedia(int(123))
            assert False
        except:
            assert True
    
    def test_invalid_extra_arg(self):
        try:
            Wikipedia('강아지', '고양이')
            assert False
        except:
            assert True


wiki = Wikipedia('강아지')
class TestGetList:
    def test_valid(self):
        test = wiki.get_list()
        assert type(test) == list and test
    
    def test_invalid_extra_arg(self):
        try:
            wiki.get_list('')
            assert False
        except:
            assert True


class TestGet:
    def test_valid(self):
        test = wiki.get('0')
        assert type(test) == dict and\
                test['title'] == '개요' and\
                type(test['content']) == str

    def test_invalid_range_less(self):
        try:
            wiki.get('-1')
            assert False
        except:
            assert True

    def test_invalid_range_over(self):
        try:
            wiki.get('100')
            assert False
        except:
            assert True

    def test_invalid_syntax(self):
        try:
            wiki.get(0)
            assert False
        except:
            assert True