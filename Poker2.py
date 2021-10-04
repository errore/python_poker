import sys
import random
import pygame

def create_player_cards():
    # 创建卡片信息,player
    _card = [x for x in range(13)]
    cards = []
    player = [[], [], [], []]
    # 单副牌（除去大小王）
    for x in range(4):
        color = list(map(lambda n: (n, x), _card))
        cards = cards + color
    # 再加一副牌
    cards = cards * 2
    # 洗牌
    count = 0
    random.shuffle(cards)
    # 发牌
    for ct in cards:
        player[count % 4].append(ct)
        count += 1
    return player


def sort_by_card(_card):
    n, _ = _card
    if n <= 1:
        n += 13
    return n


'''--------------main-----------------'''
# 初始化显示
pygame.init()
size = width, height = 1280, 720
black = 0, 0, 0
screen = pygame.display.set_mode(size)
# 载入牌面
card_colors = ('k', 'l', 'p', 's')  # 花色
card_images = [[], [], [], []]

for c in range(4):
    for i in range(1, 14):
        img = pygame.image.load(f"img/{card_colors[c]}{i}.png")
        card_images[c].append(img)  # 载入所有牌面

players_cards = create_player_cards()

l_count = 0
for li in range(4):
    r_count = 0
    players_cards[li].sort(key=sort_by_card)
    for c in players_cards[li]:
        card, c_colors = c
        screen.blit(card_images[c_colors][card], (150 + r_count, 50 + l_count))
        pygame.time.wait(10)
        pygame.display.flip()
        r_count += 30
    l_count += 100

# 主循环
while 1:
    # 处理退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
