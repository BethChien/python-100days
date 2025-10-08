'''
stack 暫時存放資料的盒子
LIFO last in first out (最後放進去的東西，會先被拿出來)
stack[-1] 清單裡的最後一個東西
return not stack 回傳true
'''

class Solution:
    def isValid(self, s: str) -> bool:
        # 建立對應關係表：右括號 → 左括號
        matching = {')': '(', '}': '{', ']': '['}
        stack = []

        for char in s:
            if char not in matching:  # 若是左括號
                stack.append(char)
            else:  # 若是右括號
                # 若堆疊為空 或 最上層不匹配，回傳 False
                if not stack or matching[char] != stack[-1]:
                    return False
                stack.pop()  # 匹配成功就移除一組

        # 若最後堆疊為空，代表全部匹配完成
        return not stack
