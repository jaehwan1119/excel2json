from typing import List, Dict, Any

# 임의의 데이터
temp_document_data = {
    'id' : "EXAU2302308290",
    'metadata' : {
        "title": "국립국어원 웹 말뭉치 추출 EXAU2302308290",
        "creator": "국립국어원",
        "distributor": "국립국어원",
        "year": "2023",
        "category": "웹 > 리뷰 > 누리소통망",
        "annotation_level": "부적절 발언 탐지",
        "sampling": "본문 전체 / 부분 추출 - 임의 추출 / 부분 추출 - 특정 부분 추출"
    },
    'document': []
}

# document data
class Data:
    def __init__(self):
        self.id = '' # json으로부터 불러옴
        self.metadata = {} # json으로부터 불러옴
        self.paragraph = [] # json으로부터 불러옴
        self.sentence = [] # excel로부터 불러옴
        self.immoral_expression = [] # excel로부터 불러옴

    def to_dict(self):
        return {
            "id": self.id,
            "metadata": self.metadata,
            "paragraph": self.paragraph,
            "sentence": self.sentence,
            "immoral_expression": self.immoral_expression
        }

# data의 원소 (json으로부터 불러옴)
class Paragraph:
    def __init__(self, id: str = None, form: str = None, original_form: str = None,):
        self.id = id
        self.form = form
        self.original_form = original_form

# data의 원소 (excel로부터 불러옴)
class Sentence:
    def __init__(self, id: str = None, form: str = None, original_form: str = None):
        self.id = id
        self.form = form
        self.original_form = original_form

    def __str__(self):
        return (f"Sentence(id={self.id}, form={self.form}, original_form={self.original_form})")

    def to_dict(self):
        return {
            "id": self.id,
            "form": self.form,
            "original_form": self.original_form
        }

# data의 원소 (excel로부터 불러옴)
class ImmoralExpression:
    def __init__(self, expression_id: str = None, expression_form: str = None,
                 expression: dict = None):
        self.expression_id = expression_id
        self.expression_form = expression_form
        self.expression = expression

    def __str__(self):
        return (f"ImmoralExpression(id={self.expression_id}, form={self.expression_form}, expression={self.expression})")

    def to_dict(self):
        return {
            "expression_id": self.expression_id,
            "expression_form": self.expression_form,
            "expression": self.expression
        }

# immoral_expression의 원소(excel로부터 불러옴)
class Expression:
    def __init__(self, explicitness: List[dict] = None, sentiment: str = None,
                 domains: str = None, intensity: int = None):
        self.explicitness = explicitness
        self.sentiment = sentiment
        self.domains = domains
        self.intensity = intensity

    def __str__(self):
        return (f"Expression(explicitness={self.explicitness}, sentiment={self.sentiment}, domains={self.domains}, intensity={self.intensity})")

    def to_dict(self):
        return {
            "explicitness": self.explicitness,
            "sentiment": self.sentiment,
            "domains": self.domains,
            "intensity": self.intensity
        }

# expression의 원소(excel로부터 불러옴)
class Explicitness:
    def __init__(self, type: str = None, form: str = None, begin: int = None, end: int = None):
        self.type = type
        self.form = form
        self.begin = begin
        self.end = end

    def __str__(self):
        return (f"Explicitness(type={self.type}, form={self.form}, begin={self.begin}, end={self.end})")

    def to_dict(self):
        return {
            "type": self.type,
            "form": self.form,
            "begin": self.begin,
            "end": self.end
        }
