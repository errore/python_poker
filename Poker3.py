import sys
import random
import pygame

class Card(pygame.sprite.Sprite):
    # 属性牌面大小，用于比较
    card_number = 0

    # 构造函数，需要提供牌面大小和颜色，以及图像缓存
    def __init__(self, number, color, images):
        self.card_number = number
        pygame.sprite.Sprite.__init__(self)
        # 初始化图像
        self.image = images[color][number]
        # 位置初始化
        self.rect = self.image.get_rect()

    def put(self):
        self.rect.x, self.rect.y = 0, 0

    def get_number(self):
        return self.card_number


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


# 载入图像资源
def load_card_images():
    card_colors = ('k', 'l', 'p', 's')  # 花色
    images = [[], [], [], []]

    for color in range(4):
        for i in range(1, 14):
            img = pygame.image.load(f"img/{card_colors[color]}{i}.png")
            img = pygame.transform.scale(img, (112, 156))
            images[color].append(img)  # 载入所有牌面资源

    return images


# 定义牌面大小排序规则
def sort_by_card(_card):
    n, _ = _card
    if n <= 1:
        n += 13
    return n


# 主函数
def main():
    """----------------init-----------------"""
    # 初始化显示
    pygame.init()
    size = 1280, 720
    screen = pygame.display.set_mode(size)
    white = 255, 255, 255
    gold = 255, 200, 10
    pygame.display.set_caption("快乐揍地主")
    # 游戏时钟（fps）
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    # 载入音频
    voice = []
    for n in range(1, 14):
        voice.append(pygame.mixer.Sound(f"sound/{n}.wav"))
    pygame.mixer.music.load("bg.oga")
    # 载入背景
    back_ground = pygame.image.load("img/bg.png")
    # 载入牌面
    card_images = load_card_images()  # 图片缓存
    # 生成玩家手牌
    players_cards = create_player_cards()
    # 渲染背景
    screen.blit(back_ground, (0, 0))
    # 四个玩家手牌精灵组
    sprites = [[], [], [], []]
    cards_groups = [pygame.sprite.Group()] * 4
    # 玩家位置
    player_position = [(350, 50), (50, 250), (350, 500), (600, 300)]
    # 文字
    font = pygame.font.SysFont('microsoft Yahei', 50)
    texts = ("Michael Ze", "Johnny Jun", "William Han", "Ricky Cong")
    text_position = [(350, 10), (50, 200), (350, 680), (1000, 250)]
    for i in range(4):
        screen.blit(font.render(texts[i], False, white), text_position[i])
    # 更新显示
    pygame.display.flip()

    """----------------start-----------------"""
    # 发牌
    for li in range(4):
        r_count = 0  # 行计数
        players_cards[li].sort(key=sort_by_card)  # 排序
        for c in players_cards[li]:
            card, c_color = c  # 处理卡片信息
            # 处理卡片精灵
            sprite = Card(card, c_color, card_images)
            sprite.rect.x, sprite.rect.y = player_position[li]
            sprite.rect.x += r_count  # 卡牌位置偏移
            # 精灵添加到组
            sprites[li].append(sprite)
            cards_groups[li].add(sprite)
            cards_groups[li].draw(screen)
            # 更新显示
            pygame.display.update()
            # 播放声音
            pygame.mixer.Sound("sound/fx.wav").play()
            clock.tick(25)
            r_count += 20

    pygame.mixer.music.play()

    # 抢地主
    pygame.mixer.Sound("sound/qiang.wav").play()
    pygame.time.delay(6000)
    dizhu = random.randint(0, 3)
    put_card = 0
    cache = 0
    """----------------update-----------------"""
    # 主循环
    while True:
        # if put_card >= 20:
        #     pygame.time.set_timer(pygame.USEREVENT, 800)
        # 处理输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 按ESC退出
            if event.type == pygame.K_ESCAPE:
                sys.exit()
            # 自定义用户事件,打牌（1秒一次）
            if event.type == pygame.USEREVENT:
                game_over = False
                for i in sprites:
                    if len(i) == 0:
                        game_over = True
                if not game_over:
                    # 语音触发
                    if random.randint(1, 6) == 1:
                        if random.randint(0, 1) == 1:
                            pygame.mixer.Sound("sound/dedede.wav").play()
                        else:
                            pygame.mixer.Sound("sound/gkd.wav").play()

                    player = (dizhu + put_card) % 4
                    card_to_put = random.randint(0, len(sprites[player]) - 1)  # 随机出牌
                    if cache != 0:
                        cache.kill()
                    cache = sprites[player][card_to_put]
                    cache.put()
                    pygame.mixer.Sound("sound/fx.wav").play()
                    voice[sprites[player][card_to_put].get_number()].play()
                    sprites[player].pop(card_to_put)
                    put_card += 1

        # 更新背景
        screen.blit(back_ground, (0, 0))

        # 更新文字
        count = 0
        for i in range(4):
            if count != dizhu:
                screen.blit(font.render(texts[i], False, white), text_position[i])
            else:
                screen.blit(font.render(texts[i], False, gold), text_position[i])
            count += 1

        # 更新牌组
        for li in range(4):
            r_count = 0  # 行计数
            for c in sprites[li]:
                c.rect.x, c.rect.y = player_position[li]
                c.rect.x += r_count
                r_count += 20
            cards_groups[li].draw(screen)

        # 更新显示
        pygame.display.update()
        clock.tick(60)


# 程序入口
if __name__ == "__main__":
    main()
