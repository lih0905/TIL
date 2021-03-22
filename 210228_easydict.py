""" EasyDict를 활용하여 딕셔너리의 속성을 부여"""

from easydict import EasyDict as edict

d = edict({'foo':3, 'bar':{'x':1, 'y':2}})
print(f"d.foo:{d.foo}")
print(f"d.bar:{d.bar}")
print(f"d.bar.x:{d.bar.x}")

print(f"d.items():{d.items()}")

class Flower(edict):
    power = 1

f = Flower({'height':12})
print(f"f.items():{f.items()}")
print(f"f.power:{f.power}")
print(f"f.height:{f.height}")
