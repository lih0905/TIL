"""
Argparser를 좀더 편하게 쓸 수 있게 해주는 simple_parsing 패키지 사용법
dataclass로 만들어진데이터 인스턴스를 argument 인자로 넣을 수 있다.
"""

from dataclasses import dataclass
from simple_parsing import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--foo", type=int, default=123, help="foo help")

@dataclass
class Options:
    """ Argument Input이 될 dataclass """
    log_dir: str    # Help string for a required log_dir str argument
    learning_rate: float = 1e-4 # Learning rate for the training

parser.add_arguments(Options, dest="options")


if __name__ == '__main__':
    args = parser.parse_args()
    print(f"foo:{args.foo}")
    print(f"options:{args.options}")

