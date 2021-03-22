"""
클래스 내부에서 변수를 선언하는 두 가지 방식에 대해 고민해봄
"""

class TestClass:
    var1 = 0
    
    def __init__(self, init):
        self.var2 = init
        

if __name__ == '__main__':
    
    print(f"INPUT : test1 = TestClass(1)")
    test1 = TestClass(1)
    print(f"OUTPUT")
    print(f"test1.var1 = {test1.var1}") # 0 
    print(f"test1.var2 = {test1.var2}") # 1
    print("-"*30)
    TestClass.var1 = 2
    test1.var2 = 2
    print(f"INPUT : TestClass.var1 = 2")
    print(f"INPUT : test1.var2 = 2")
    print(f"OUTPUT")
    print(f"test1.var1 = {test1.var1}") # 2 -> 클래스에 직접 속한 변수를 수정하면 모든 인스턴스가 다 바뀜
    print(f"test1.var2 = {test1.var2}") # 2 -> 인스턴스 변수 변경
    print("-"*30)
    print("INPUT : test2 = TestClass(3)")
    test2 = TestClass(3)
    print(f"OUTPUT")
    print(f"test1.var1 = {test1.var1}") # 3
    print(f"test1.var2 = {test1.var2}") # 3
    print(f"test2.var1 = {test2.var1}") # 2
    print(f"test2.var2 = {test2.var2}") # 3
    print("-"*30)
    print("INPUT : test1.var1 = 4")
    test1.var1 = 4
    print(f"OUTPUT")
    print(f"test1.var1 = {test1.var1}") # 4 -> 인스턴스에서 클래스의 변수를 수정하는 순간 그 변수는 인스턴스의 변수가 되어버림
    print(f"test2.var1 = {test2.var1}") # 2
    print(f"TestClass.var1 = {TestClass.var1}") # 2
    print("-"*30)
    print("INPUT : TestClass.var1 = 5")
    TestClass.var1 = 5
    print(f"OUTPUT")
    print(f"test1.var1 = {test1.var1}") # 2
    print(f"test2.var1 = {test2.var1}") # 2
    print(f"TestClass.var1 = {TestClass.var1}")
    print("-"*30)
    print("INPUT : TestClass.var2 = 6")
    print("INPUT : test3 = TestClass(10)")
    TestClass.var2 = 6
    test3 = TestClass(10)
    print(f"OUTPUT")
    print(f"test1.var2 = {test1.var1}") # 2
    print(f"test2.var2 = {test2.var2}") # 2
    print(f"TestClass.var2 = {TestClass.var2}")
    print(f"test3.var1 = {test3.var1}") # 2
    print(f"test3.var2 = {test3.var2}") # 2
        