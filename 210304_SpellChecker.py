import re
import os
from collections import Counter

class SpellChecker():
    
    def __init__(self, txt_file=os.path.join('Data','big.txt')):
        """
        txt 파일을 불러와서 단어 단위로 빈도수 분석
        txt 파일 출처는 https://norvig.com/big.txt
        """
        
        with open(txt_file, 'r') as f:
            self.text = f.read().lower()
            
        # print(self.text[:1000])
        
        words = re.findall('\w+', self.text)
        self.counter = Counter(words)
        self.total_num = sum(self.counter.values())
        
    def prob(self, word, total_num=self.total_num):
        return self.counter.get(word,0) / total_num
        
if __name__ == '__main__':
    sc = SpellChecker()
    print(sc.prob('high'))