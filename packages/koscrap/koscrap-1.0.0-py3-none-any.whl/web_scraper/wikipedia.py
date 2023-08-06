from urllib.parse import quote
from .modules.get_soup import get_soup


class Chapter:
    """위키백과에서의 한 쳅터에 대한 클래스입니다."""

    def __init__(self, title):
        self._title = title
        self._content = ''
        self._parent = None
    
    def add_content(self, content):
        self._content += content
    
    def set_parent(self, parent_node):
        self._parent = parent_node


class Wikipedia:
    """위키백과에서 'search_text'를 검색한 결과를 저장하는 클래스입니다."""

    def __init__(self, search_text: str):
        """'search_text'는 위키백과에서의 검색어 입니다.
        
        example:
            wiki = Wikipedia('강아지')"""
        
        self._summary = ''
        self._chapters = {'0': Chapter('개요')}
        self._titles = []
        
        encode_text = quote(search_text)
        url = f'https://ko.wikipedia.org/wiki/{encode_text}'
        soup = get_soup(url)
        # total_content: 위키백과에서 검색한 단어에 대한 모든 내용.
        total_content = soup.find('div', {'class': 'mw-parser-output'})
        if not total_content:
            self._chapters['0'].add_content(f"'{search_text}'에 대한 검색결과가 없습니다.")
            return
        # chapter_idx = '3.1', chapter_list = [3, 1]
        chapter_idx, chapter_list = '0', [0]
        parent_num = 0
        for content in total_content:
            tag = content.name
            if tag == None:
                continue
            elif tag[0] == 'h':
                new_parent_num = int(tag[1]) - 2
                if new_parent_num <= parent_num:
                    chapter_list = chapter_list[:new_parent_num+1]
                    chapter_list[-1] += 1
                else:
                    chapter_list.append(1)
                chapter_idx = '.'.join(map(str, chapter_list))
                self._chapters[chapter_idx] = Chapter(title=content.text.split('[')[0])
                self._titles.append(content.text)
            elif tag == 'p':
                self._chapters[chapter_idx].add_content(content.text)
            elif tag == 'ul':
                self._chapters[chapter_idx].add_content(content.text)

    
    def __str__(self):
        """클래스를 출력하면 첫 번째 쳅터(주로 '개요')의 내용을 출력합니다.
        
        example:
            print(wiki)

            >> 어린 개를 일컫는 순우리말이다. (...이하 중략)"""

        return self._chapters['0']._content
    
    def get_list(self):
        """쳅터의 목록을 list 형태로 가져옵니다.
        
        example:
            print(wiki.get_list)
            
            >> ['1', '1.1', '2', '3', '3.1']"""
        
        return list(self._chapters.keys())

    def get(self, chapter_num):
        """'chapter_num'에 해당하는 내용을 출력합니다.
        
        example:
            print(wiki.get(2))
            
            >> 2. 본래 뜻과 다르게 사용하는 경우
                어린 자식이나 손주를 부르는 말로도 쓰며, (...이하 중략)
            
        참고로, 내용이 존재하지 않을 수도 있습니다."""
        
        title = self._chapters[chapter_num]._title
        content = self._chapters[chapter_num]._content
        if not content:
            content = '(내용이 존재하지 않습니다.)'
        result = {}
        result['title'] = title
        result['content'] = content
        return result

if __name__ == "__main__":
    wiki = Wikipedia("강아지")
    print(wiki)
    print(wiki.get('1'))