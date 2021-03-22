from dataclasses import dataclass, field
from typing import List

"""
class로 Data를 생성할 경우 일반적으로 인스턴스 생성, 인스턴스간의 비교 등에서
귀찮은 점이 많이 발생함
이를 해결하기 위한 dataclass 활용
"""

@dataclass
class Data:
    id: int
    name: str
    admin: bool = False
    # list를 초기값으로 주는 경우
    # 모든 인스턴스의 초기값을 공유하게 되므로
    # 다음과 같이 구현해야함
    friends: List[int] = field(default_factory=list)


if __name__ == '__main__':
    data = Data(10, "LIH", False)

    print(data)
