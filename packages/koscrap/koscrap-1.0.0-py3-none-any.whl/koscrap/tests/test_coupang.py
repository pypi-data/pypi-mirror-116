from ..coupang import Coupang


class TestInit:
    def test_valid(self):
        try:
            Coupang("가방")
            assert True
        except:
            assert False
    
    def test_invalid_no_search_text(self):
        try:
            Coupang()
            assert False
        except:
            assert True

    def test_invalid_arg_syntax(self):
        try:
            Coupang(int(123))
            assert False
        except:
            assert True

    def test_invalid_arg_extra(self):
        try:
            Coupang('가방', '연필')
            assert False
        except:
            assert True


coupang = Coupang('가방')
class TestGetImages:
    def test_valid(self):
        images = coupang.get_images()
        assert type(images) == list and images


class TestGetProduct:
    def test_valid(self):
        product = coupang.get_product(1)
        assert type(product) == dict and product
    