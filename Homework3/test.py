import collections
def findLadders(beginWord, endWord, wordList):
    # if endWord not in wordList:
    #     return []
    # n=len(beginWord)
    # flag,tree=0,collections.defaultdict(set)
    # q={beginWord}
    # while not flag and q:
    #     new_q=set()
    #     for word in q:
    #         for a in 'qwertyuiopasdfghjklzxcvbnm':
    #             for i in range(n):
    #                 new_word=word[:i]+a+word[i+1:]
    #                 if new_word in wordList and new_word not in tree:
    #                     if new_word==endWord:
    #                         flag=1
    #                     else:
    #                         new_q.add(new_word)
    #                     tree[word].add(new_word)
    #     q=new_q
    # def bt(x):
    #     return [[x]] if x == endWord else [[x] + rest for y in tree[x] for rest in bt(y)]
    # return bt(beginWord)

    tree, words, n = collections.defaultdict(set), set(wordList), len(beginWord)
    if endWord not in wordList: return []
    found, q, nq = False, {beginWord}, set()
    while q and not found:
        words -= set(q)
        for x in q:
            for y in [x[:i] + c + x[i + 1:] for i in range(n) for c in 'qwertyuiopasdfghjklzxcvbnm']:
                if y in words:
                    if y == endWord:
                        found = True
                    else:
                        nq.add(y)
                    tree[x].add(y)
        q, nq = nq, set()
    def bq(x):
        if x==endWord:
            return [[x]]
        else:
            return [[x]+q for p in tree[x] for q in bq(p)]
    return bq(beginWord)

if __name__=='__main__':
    print(findLadders('hit','cog',["hot","dot","dog","lot","log","cog"]))
    print([['start']+['end']])