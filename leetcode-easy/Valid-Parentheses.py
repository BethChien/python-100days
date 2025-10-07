'''
stack 暫時存放資料的盒子
LIFO last in first out (最後放進去的東西，會先被拿出來)
stack[-1] 清單裡的最後一個東西
return not stack 回傳true
'''

class Solution:
    def isValid(self, s: str) -> bool:
        #create a hashmap that matches open parenthese with its closing
        #create a dictionary to matching open and close bracket
        matching = {')':'(', '}':'{', ']':'['}
        stack = []
        #s = "()[]{}"
        for char in s:
            if char not in matching:
                stack.append(char)
            elif matching[char] != stack[-1] or not stack:
                return False
            else:
                stack.pop()
        return not stack
