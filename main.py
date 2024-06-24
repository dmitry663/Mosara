def aaa(func):
    user_paid = True 

    def wrapper(asd):      # 호출할 함수를 감싸는 함수 
        if asd:
            return func()
        else:
            return
        
    return wrapper


@aaa(True)
def bbb():
    return "True"

print(bbb())