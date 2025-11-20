'''
將兩個字串 word1 和 word2 交錯合併，從 word1 開始輪流取字母。
若其中一個字串較長，則把剩下的部分接在最後。
'''
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
      result = []
      for i in range(max(len(word1), len(word2))):
        if i < len(word1):
          result.append(word1[i])
        if i < len(word2):
          result.append(word2[i])
      return ''.join(result)
