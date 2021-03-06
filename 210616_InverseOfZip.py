# zip 연산을 하면 두 iterable을 하나의 반복문으로 출력할 수 있다.

a = ('a', 'b', 'c')
b = (1,2,3)

print(list(zip(a,b)))
# [('a', 1), ('b', 2), ('c', 3)]

# 반대로 [('a', 1), ('b', 2), ('c', 3)] 가 입력으로 주어졌을 때 
# ('a', 'b', 'c'), (1,2,3) 을 만들기 위해서는 다음과 같이 하면 됨
# zip(*zipped_list)

X = ('a', 1)
Y = ('b', 2)
Z = ('c', 3)

print(list(zip(*(X,Y,Z))))
# [('a', 'b', 'c'), (1, 2, 3)]