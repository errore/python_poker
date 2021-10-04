import random

# 创建卡片信息,player
card = [x for x in range(13)]
cards = []
player = [[], [], [], []]
# 单副牌（除去大小王）
for x in range(4):
    color = list(map(lambda n: (n, x), card))
    cards = cards + color
# 再加一副牌
cards = cards * 2
# 洗牌
random.shuffle(cards)
# 发牌
count = 0
for c in cards:
    player[count % 4].append(c)
    count += 1
for p in player:
    print(p)
