from urllib.parse import quote
from .modules.get_soup import get_soup


class Product:
    """쿠팡에서 검색한 상품의 정보가 담겨있는 클래스입니다."""

    def __init__(self, image, name, price, star, url):
        self._image = image
        self._name = name
        self._price = price
        self._star = star
        self._url = url
    
    def get_contents(self):
        """상품 정보를 반환합니다."""

        contents = {}
        contents['image'] = self._image
        contents['name'] = self._name
        contents['price'] = self._price
        contents['star'] = self._star
        contents['url'] = self._url
        return contents


class Coupang:
    """쿠팡에서 상품 정보를 검색합니다."""

    def __init__(self, search_text: str):
        """쿠팡에서 'search_text'를 검색하여 그 결과를 저장합니다."""

        self._search_text = search_text
        self._products = []

        encode_text = quote(search_text)
        url = f'https://www.coupang.com/np/search?q={encode_text}'
        soup = get_soup(url)
        ul = soup.find("ul", {"id":"productList"})
        products = ul.findAll("a", {"class":"search-product-link"})
        for product in products:
            url = product.get("href")
            image = product.find("img").get("src")
            if image[-12:] == 'blank1x1.gif':
                image = None
            name = product.select_one(".name").get_text()
            price = product.select_one(".price-value").get_text()
            star = product.select_one(".rating")
            if star != None:
                star = star.get_text()
            self._products.append(Product(image, name, price, star, url))
    
    def __str__(self):
        """검색어 정보를 반환합니다."""

        return f"'{self._search_text}'에 대한 쿠팡 검색 결과입니다."
    
    def get_images(self):
        """검색 결과로 나온 이미지들을 리스트 형태로 반환합니다."""

        img_list = list(filter(lambda x: x, map(lambda x: x._image, self._products)))
        return img_list
    
    def get_product(self, idx):
        f"""'{idx}'번째 상품에 대한 정보를 가져옵니다."""

        product = self._products[idx]
        return product.get_contents()


if __name__ == "__main__":
    coupang = Coupang('가방')
    print(coupang)
    print(coupang.get_images())