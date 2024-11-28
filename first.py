# region First task
# 1. Если мы из корректно записанного арифметического
# выражения, содержащего числа, знаки операций и открывающие и
# закрывающие круглые скобки выбросим числа и знаки операций,
# а затем запишем оставшиеся в выражении скобки без пробелов между ними,
# то полученный результат назовем правильным скобочным выражением
# [скобочное выражение "(()(()))" - правильное, а "()(" и "())(" - нет].
# Найти число правильных скобочных выражений, содержащих N
# открывающихся и N закрывающихся скобок. N вводится с клавиатуры.
# N неотрицательное целое число.

# Пример:
# N =    1 (по одной скобке открывающейся и закрывающейся) - ответ 1
# ()
# )(
# ))
# ((
# Только один правильный вариант

# Для введенного числа 2 - 2 :
# endregion

import re


ex = '(1+(23+3)*1+38*(6/2)+((3-2)+1)+1)'
ex_brackets = '(()()((())))'

#this function delete numbers and +*/-
def get_only_brackets(s: str):
    s = re.sub(r"[0-9\+//\-/*]+", "", s)
    return s




#this fun checks if the string is valid and return True or False
def isValid(s: str):
   
    stack = [s[0]]
    # you can add other kinds of brackets for comparing if you need it. 
    brackets = {")": "("}
    for i in range(1, len(s)):
        #add  to stack if it "("
        if s[i] == "(":
            stack.append(s[i])
        else:
            #check stack if it's =0 than there is not "("  and it means the first brackets is )  
            if len(stack) == 0:
                return False
            #getting last element for comparing and it's not closing brackets that is the same so we need to add it.
            el = stack.pop()
            if el != brackets[s[i]]:
                stack.append(el)
                stack.append(s[i])
    #checking if there are left some values in  stack. It means they did not find a pair
    return False if len(stack) > 0 else True



def run(s: str, num: int) -> int:
    if num == 0 or num*2>len(s)+1:
        return 0    
    num *= 2
    values: list[str] = []
    #two pointers technic
    first, second = 0, num
    #run until when second is not the same as the length of the string
    while second <= len(s):
        #get the substring for needed length.
        sub_str = s[first:second]
        #check if the string is valid and add it to our values
        if isValid(sub_str):
            values.append(sub_str)
        #increase our pointers
        second += 1
        first += 1
    print(values)
    return len(values)


try:
    val = input("Insert number, please. ")
    num:int = int(val)
    print(run(ex_brackets, num))
except Exception as e:
    print(f"Numbers was not correct -> {val}")

# Could not understand do you need unqie brackets or all brackers that match the condition
# for unique bracket you need to change list for set 

