'''
O(n) 當輸入資料的數量是 n 時，執行時間（或空間使用量）會與 n 成正比增加。
只處理母音字母
母音字母反轉，其他不變
stack last in first out
Recursion
'''
#stack
class Solution:
    def reverseVowels(self, s: str) -> str:
        #Time: O(n) Space: O(1)
        vowels = set("aeiouAEIOU")
        stack = []

        #第一次遍歷: 把母音存進 stack
        for c in s:
            if c in vowels:
                stack.append(c)
        
        #第二次遍歷: 遇到母音就從 stack 取出
        result = []
        for c in s:
            if c in vowels:
                result.append(stack.pop())
            else:
                result.append(c)
        return "".join(result)
