import pygame
import sys
import os
import pickle
import time
import random
from Buckshot_Roulette import NPC, all_item, shop_item, shopkeeper, host, collection_manager

os.chdir('/home/sam/oop-python-nycu/tests/team_16/game_testing')
class participant:
    def __init__(self, controlable, hp, item):
        self.controlable = controlable
        self.hp = hp
        self.item = item

class computer(participant):
    def __init__(self, hp, item):
        participant.__init__(self, False, hp, item)
        self.handcuff = False
        self.bullet_pattern = []
        self.known_live = 0
        self.known_blank = 0
        self.max_item = 8
    def dohandcuff(self):
        self.handcuff = True
    def unhandcuff(self):
        self.handcuff = False
    def reset_bullet_pattern(self,number):
        self.bullet_pattern = []
        for i in range(number):
            self.bullet_pattern.append('unknown')
        self.known_live = 0
        self.known_blank = 0
    def set_bullet_pattern(self,poition,value):
        self.bullet_pattern[poition] = value
        if value == 'live':
            self.known_live += 1
        else:
            self.known_blank += 1
    def pop_bullet_pattern(self):
        if self.bullet_pattern.pop(0) == 'live':
            self.known_live -=1
        else:
            self.known_blank -=1

class player(participant):
    def __init__(self, hp, item, money):
        participant.__init__(self, True, hp, item)
        self.handcuff = False
        self.money = money
        self.max_item = 8
    def dohandcuff(self):
        self.handcuff = True
    def unhandcuff(self):
        self.handcuff = False

class game:
    def __init__(self, player, computer, hp):
        self.action = 0
        self.player = player
        self.computer = computer
        self.player.hp = hp
        self.computer.hp = hp
        self.round = 1
        self.handsaw = False
        self.live_bullet = 0
        self.blank = 0
        self.remain_bullet = []
        self.remain_bullet_count = 0
        self.choose = ''
        self.item_list = ['放大鏡','香菸','手鋸','啤酒','手銬','手機','轉換器','過期藥物']
        self.special_item = ['未知藍圖','禁藥','大口徑子彈','榴彈砲','彈藥包']   
        print('遊戲開始,每人有',hp,'點血量')

    def give_item(self,number):
        for i in range(number):
            if len(self.player.item) < self.player.max_item:
                chance = random.randint(1,5)
                '''if (chance == 5) and (self.player.item.count('未知藍圖') <= 1):
                    item='未知藍圖'
                    print('你獲得了',item)
                    self.player.item.append(item)
                else:'''
                item=self.item_list[random.randint(0,7)]
                print('你獲得了',item)
                self.player.item.append(item)
            else:
                print('你的物品欄已滿')
            if len(self.computer.item) < self.computer.max_item:
                chance = random.randint(1,10)
                if chance == 10:
                    item='未知藍圖'
                    self.computer.item.append(item)
                else:
                    self.computer.item.append(self.item_list[random.randint(0,7)])

    def computer_bonus(self,bonus_number):
        self.computer.item.append(self.item_list[random.randint(0,7)])
        if (bonus_number+1) % 2 == 0:
            self.computer.hp += 1
            print('莊家的血量增加了一點')

    def start(self,live_bullet,blank,item_number):
        global current_turn
        self.remain_bullet_count = live_bullet + blank
        current_turn = 'player'
        self.live_bullet = live_bullet
        self.blank = blank
        self.action = 0
        print('第',self.round,'局開始')
        if self.player.handcuff:
            self.player.unhandcuff()
            print('你的手銬解除,可以自由行動了')
        if self.computer.handcuff:
            self.computer.unhandcuff()
            print('莊家的手銬解除,可以自由行動了')
        self.handsaw = False 
        self.give_item(item_number)
        self.remain_bullet = []
        self.computer.reset_bullet_pattern(self.live_bullet+self.blank)
        print('這局有',self.live_bullet,'發實彈',self.blank,'發空包彈')
        for i in range(self.live_bullet):
            self.remain_bullet.append(True)
        for i in range(self.blank):
            self.remain_bullet.append(False)
        random.shuffle(self.remain_bullet)
        self.player_turn_start()

    def player_turn_start(self):
        self.action = 0
        print('==========================================')
        print('你的回合')
        print('你的物品欄:',self.player.item)
        print('玩家血量:',self.player.hp,'莊家血量:',self.computer.hp)  
        print('剩餘',self.live_bullet,'發實彈',self.blank,'發空包彈')
        print('請選擇要做的事')
        print('1.射向莊家, 2.射向自己, 3.使用物品, 4.顯示莊家物品欄')

    def player_turn(self):
        global current_turn,pretext,pretext2
        if self.action==1:
            if self.remain_bullet[0]&self.handsaw:
                self.computer.hp -= 2
                pretext ='你射中了莊家,'
                pretext2 = '造成兩點傷害'
                self.handsaw = False
                self.computer.pop_bullet_pattern()
                self.live_bullet -= 1
            elif self.remain_bullet[0]:
                self.computer.hp -= 1
                pretext ='你射中了莊家,'
                pretext2 = '造成一點傷害'
                self.computer.pop_bullet_pattern()
                self.live_bullet -= 1
            else:
                pretext ='你的子彈打空了'
                self.computer.pop_bullet_pattern()
                self.blank -= 1
                self.handsaw = False
            self.remain_bullet.pop(0)
            current_turn = 'dealer'
        elif self.action==2:
            if self.remain_bullet[0]&self.handsaw:
                self.player.hp -= 2
                pretext ='你射中了自己,'
                pretext2 = '造成兩點傷害'
                self.handsaw = False
                self.computer.pop_bullet_pattern()
                self.live_bullet -= 1
                current_turn = 'dealer'
            elif self.remain_bullet[0]:
                self.player.hp -= 1
                pretext ='你射中了自己,'
                pretext2 = '造成一點傷害'
                self.computer.pop_bullet_pattern()
                self.live_bullet -= 1
                current_turn = 'dealer'
            else:
                pretext ='你的子彈打空了,'
                pretext2 = '額外獲得一回合'
                self.computer.pop_bullet_pattern()
                self.blank -= 1
                #continue
            self.remain_bullet.pop(0)
        elif self.action==3:
            if self.choose == '手鋸':
                if self.handsaw:
                    pretext ='手鉅效果已經存在了'
                    return
                self.handsaw = True
                pretext ='你使用了手鋸,下一'
                pretext2 = '發子彈造成兩倍傷害'
            elif self.choose == '啤酒':
                if self.remain_bullet.pop(0):
                    pretext ='你使用了啤酒,'
                    pretext2 = '退掉一發實彈'
                    self.live_bullet -= 1
                else:
                    pretext ='你使用了啤酒,'
                    pretext2 = '退掉一發空包彈'
                    self.blank -= 1
                self.computer.pop_bullet_pattern()
                if len(self.remain_bullet) == 0:
                        pretext ='子彈打完了'
                        return
            elif self.choose == '手機':
                pretext ='你使用了手機'
                if len(self.remain_bullet) == 1:
                    n = 0
                else:
                    n=random.randint(1,len(self.remain_bullet)-1)
                if self.remain_bullet[n]:
                    pretext ='第',n+1,'發是實彈'
                else:
                    pretext ='第',n+1,'發是空包彈'
            elif self.choose == '轉換器':
                pretext ='你使用了轉換器,現在'
                pretext2 = '這發子彈將反轉'
                self.remain_bullet[0] = not self.remain_bullet[0]
                if self.remain_bullet[0]:
                    self.live_bullet += 1
                    self.blank -= 1
                else:
                    self.live_bullet -= 1
                    self.blank += 1
            elif self.choose == '過期藥物':
                if random.randint(0,1):
                    pretext ='你使用了過期藥物,'
                    pretext2 = '失去了一點血量'
                    self.player.hp -= 1
                else:
                    pretext ='你使用了過期藥物,'
                    pretext2 = '回復了2點血量'
                    self.player.hp += 2
                if self.player.hp <= 0:
                    time.sleep(2)
                    print('**************************************')
                    pretext ='你死了'
                    time.sleep(2)
                    return
            elif self.choose == '放大鏡':
                pretext ='你使用了放大鏡'
                pretext2 = '看到 ','實彈' if self.remain_bullet[0] else '空包彈'
            elif self.choose == '香菸':
                pretext ='你使用了香菸,'
                pretext2 = '回復一點血量'
                self.player.hp += 1
            elif self.choose == '手銬':
                if self.computer.handcuff:
                    pretext ='莊家已經被銬住了'
                    return
                pretext ='你使用了手銬,莊家'
                pretext2 = '下回合無法行動'
                self.computer.dohandcuff()
            elif self.choose == '禁藥':
                    #70%機率血量翻倍並+3，30%血量降低到1點，若血量為1則死亡
                pretext ='你使用了禁藥'
                if random.randint(1,10) <= 7 or self.player.have_lust_mark:
                    self.player.hp *= 2
                    self.player.hp += 3
                    pretext ='你的血量大幅提升'
                else:
                    if self.player.hp == 1:
                        pretext ='你死了'
                        self.player.hp = 0  
                        return
                    self.player.hp = 1
                    pretext ='你中毒了，血量降為1'
            elif self.choose == '大口徑子彈':
                #將目前這發直接子彈替換成大口徑子彈並直接發射，造成3點傷害，如果有使用手鋸則造成6點傷害
                if self.handsaw:
                    self.computer.hp -= 6
                    pretext ='你發射了大口徑子彈,'
                    pretext2 = '造成6點傷害'
                else:
                    self.computer.hp -= 3
                    pretext ='你發射了大口徑子彈,'
                    pretext2 = '造成3點傷害'
                if self.remain_bullet.pop(0):
                    self.live_bullet -= 1
                else:
                    self.blank -= 1
                self.computer.pop_bullet_pattern()
                current_turn = 'dealer'
                skip = True
                self.handsaw = False
            elif self.choose == '榴彈砲':
                #將自身血量降低至1點，並發射現在這發子彈，若為實彈則造成(降低的血量+1)點傷害，使用手鋸則造成兩倍傷害，若為空包彈則不造成傷害，使用後輪到莊家的回合
                damage = self.player.hp
                self.player.hp = 1
                if self.remain_bullet.pop(0):
                    if self.computer.fog > 0:
                        pretext ='朦朧國王使你射偏了'
                        self.computer.fog -= 1
                        self.handsaw = False
                    elif self.handsaw:
                        self.computer.hp -= 2*damage
                        pretext ='你發射了榴彈砲,'
                        pretext2 = '造成',2*damage,'點傷害'
                        self.handsaw = False
                    else:
                        self.computer.hp -= damage
                        pretext ='你發射了榴彈砲,'
                        pretext2 = '造成',damage,'點傷害'
                    self.live_bullet -= 1
                else:
                    pretext ='你發射了榴彈砲,'
                    pretext2 = '但是子彈打空了'
                    self.blank -= 1
                self.computer.pop_bullet_pattern()
                current_turn = 'dealer'
            elif self.choose == '彈藥包':
                #對莊家造成剩餘實彈數量的傷害，之後用實彈和空包彈隨機將彈藥填滿至8發
                damage = self.live_bullet
                if self.handsaw:
                    damage *= 2
                pretext ='你使用了彈藥包,'
                pretext2 = '對莊家造成',damage,'點傷害'
                self.computer.hp -= damage
                self.handsaw = False
                self.remain_bullet = []
                self.live_bullet = 0
                self.blank = 0
                for i in range(8-len(self.remain_bullet)):
                    if random.randint(0,1):
                        self.remain_bullet.append(True)
                        self.live_bullet += 1
                    else:
                        self.remain_bullet.append(False)
                        self.blank += 1
                random.shuffle(self.remain_bullet)
                pretext ='彈藥已重新裝填'
                self.computer.reset_bullet_pattern(self.live_bullet+self.blank)
                if self.player.blessing > 0:
                    self.handsaw = self.blessing(self.remain_bullet,'玩家',self.handsaw)
            elif self.choose == '漆黑皇后':
                #移除雙方所有道具，將彈夾裝填為一發空包彈一發實彈，這發實彈將造成5點傷害
                pretext ='你使用了漆黑皇后，彈藥裝填為一發空包彈一發5點傷害實彈，祈禱吧!'
                self.player.item = []
                self.computer.item = []
                self.remain_bullet = [True,False]
                self.live_bullet = 1
                self.blank = 1
                self.computer.reset_bullet_pattern(self.live_bullet+self.blank)
                random.shuffle(self.remain_bullet)
                killer_queen = True
                not_blue_print = False
                self.player.queen_used.append('漆黑皇后')
                if self.player.blessing > 0:
                    self.handsaw = self.blessing(self.remain_bullet,'玩家',self.handsaw)
            elif self.choose == '神聖皇后':
                #回3點血量，背包上限+2，獲得3個隨機物品
                pretext ='你使用了神聖皇后，回復3點血量，背包上限+2，獲得3個隨機物品'
                self.player.hp += 3
                self.player.max_item += 3
                self.give_participant_item(3,self.player)
                self.player.max_item -= 1
                self.player.queen_used.append('神聖皇后')
            elif self.choose == '蔚藍皇后':
                #玩家的回合結束時，獲得一個隨機物品
                pretext ='你使用了蔚藍皇后，輪到莊家的回合時你將獲得一個隨機物品'
                self.player.item_queen += 1   
                self.player.queen_used.append('蔚藍皇后')
            elif self.choose == '腥紅皇后':
                #玩家的回合開始時，附加手鉅效果
                pretext ='你使用了腥紅皇后，每回合獲得手鋸效果並免疫手鉅的額外傷害，可以觸發五次'
                self.player.blood_queen += 5       
                self.player.queen_used.append('腥紅皇后')
            elif self.choose == '琉璃皇后':
                #每次重新裝彈(回合開始、彈藥包、漆黑皇后)時通靈第一顆子彈，若為實彈則附加手鉅效果
                #若為空包彈則回復一點血量並消除莊家一個道具或獲得一個隨機道具
                #使用當下清空莊家的道具、清空彈夾並裝上一顆實彈
                pretext ='你獲得了琉璃的祝福，莊家的道具被清空，彈夾重新裝填為一發實彈'
                self.computer.item = [] 
                self.computer.reset_bullet_pattern(1)
                self.remain_bullet = [True]
                if not self.handsaw:
                    self.handsaw = True
                    pretext ='你獲得了手鋸效果'
                time.sleep(1)
                self.live_bullet = 1
                self.blank = 0
                self.player.blessing += 1
                self.player.queen_used.append('琉璃皇后')     
        self.choose = ''

        draw_player_round()
        pygame.display.update()
        if self.action != 0:
            time.sleep(2)             
        self.action = 0        
                

    def in_between(self):
        if self.computer.hp <= 0:
            time.sleep(2)
            print('**************************************')
            print('你贏了')
            time.sleep(2)
            return
        if self.player.hp <= 0:
            time.sleep(2)
            print('**************************************')
            print('你死了')
            time.sleep(2)
            return
        if len(self.remain_bullet) == 0:
            print('子彈打完了')
            print('進入下一局')
            return
        print('==========================================')
        print('莊家的回合')
        print('==========================================')
        time.sleep(1)

    def computer_turn(self):
        global current_turn
        if (self.live_bullet-self.computer.known_live) <= 0:
            for i in range(len(self.computer.bullet_pattern)):
                if self.computer.bullet_pattern[i] == 'unknown':
                    self.computer.set_bullet_pattern(i,'blank')
        elif (self.blank-self.computer.known_blank) <= 0:
            for i in range(len(self.computer.bullet_pattern)):
                if self.computer.bullet_pattern[i] == 'unknown':
                    self.computer.set_bullet_pattern(i,'live')

        if self.computer.handcuff:
            print('莊家被手銬銬住了,無法行動')
            self.computer.unhandcuff()
            current_turn = 'player'
            return
        while True:
            time.sleep(2)
            if len(self.remain_bullet) == 0:
                print('子彈打完了')
                print('進入下一局')
                return
            
            if self.computer.bullet_pattern[0] == 'live':
                self.action = 1
            elif self.computer.bullet_pattern[0] == 'blank':
                self.action = 2
            elif len(self.computer.item) == 0:
                self.action = random.randint(1,2)
            else:
                self.action = random.randint(1,3)
            if (self.live_bullet > self.blank) & (self.action == 2):
                self.action = 1

            if self.action==3:
                self.action = random.randint(1,2)

                #莊家的行動選項和玩家相同
            if self.action==1:
                try_count = 0
                if self.remain_bullet[0]&self.handsaw:
                    self.player.hp -= 2
                    print('莊家射中了你,造成兩點傷害')
                    self.handsaw = False
                    self.live_bullet -= 1
                    self.computer.pop_bullet_pattern()
                elif self.remain_bullet[0]:
                    self.player.hp -= 1
                    print('莊家射中了你,造成一點傷害')
                    self.live_bullet -= 1
                    self.computer.pop_bullet_pattern()
                else:
                    print('莊家的子彈打空了')
                    self.blank -= 1
                    self.computer.pop_bullet_pattern()
                    self.handsaw = False
                self.remain_bullet.pop(0)
                current_turn = 'player'

            elif self.action==2:
                if self.remain_bullet[0]&self.handsaw:
                    self.computer.hp -= 2
                    print('莊家射中了自己,造成兩點傷害')
                    print('莊家是笨蛋嗎笑死')
                    self.handsaw = False
                    self.live_bullet -= 1
                    self.computer.pop_bullet_pattern()
                    current_turn = 'player'
                elif self.remain_bullet[0]:
                    self.computer.hp -= 1
                    print('莊家射中了自己,造成一點傷害')
                    self.live_bullet -= 1
                    self.computer.pop_bullet_pattern()
                    self.handsaw = False
                    current_turn = 'player'
                else:
                    print('莊家射向自己，子彈打空了,額外獲得一回合')
                    self.computer.pop_bullet_pattern()
                    self.blank -= 1
                    self.handsaw = False
                self.remain_bullet.pop(0)

            if self.player.hp <= 0:
                time.sleep(2)
                print('**************************************')
                print('你死了')
                time.sleep(2)
                return
            if self.computer.hp <= 0:
                time.sleep(2)
                print('**************************************')
                print('你贏了')
                time.sleep(2)
                return
            if self.player.handcuff:
                print('你被手銬銬住了,無法行動')
                self.player.unhandcuff()
                try_count = 0
                continue
            if len(self.remain_bullet) == 0:
                print('子彈打完了')
                print('進入下一局')
                return
            break































# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BuckShot")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonts
try:
    font = pygame.font.Font('Noto_Sans_TC/NotoSansTC-VariableFont_wght.ttf', 24)
    description_font = pygame.font.Font('Noto_Sans_TC/NotoSansTC-VariableFont_wght.ttf', 18)
except pygame.error as e:
    print(f"Error loading font: {e}")
    pygame.quit()
    sys.exit()

# Load images
try:
    welcome_image = pygame.image.load('welcome.png')
    lobby_image = pygame.image.load('lobby.png')
    shop_image = pygame.image.load('shop.png')
    game_image = pygame.image.load('game.png')
    challenge_image = pygame.image.load('challenge.png')
    samael_image = pygame.image.load('薩邁爾.png')
    leviathan_image = pygame.image.load('利維坦.png')
    game_over_image = pygame.image.load('game_over.png')
    game_win_image = pygame.image.load('game_win.png')

except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Define NPC interactions
def npc_interaction(npc, action, callback):
    dialogues = {
        "Leviathan": {
            "normal": [
                "利維坦: 小老弟買顆心臟吧，你死了可就沒人陪我聊天了",
                "利維坦叼了根菸，悠閒地滑著手機",
                "利維坦不在，店裡空無一人，商品靜靜的陳列著",
                "利維坦把玩著手銬和槍械零件，似乎沒注意到你"
            ],
            "before_challenge": [
                "利維坦: 小夥子要挑戰我? 希望你已經做好赴死的心理準備了,我可不會手下留情喔",
                "利維坦: 順帶一提，如果你還沒從莉莉斯納裡聽說過的話，我可是我們三人之中最強的喔?",
                "利維坦: 如果你能讓我欣賞你，我就來教你道具的真正使用方式 ",
                "利維坦: 準備好的話就去賭桌找我吧"
            ],
        },
        "Samael": {
            "normal": [
                "薩邁爾: 你要挑戰我? 你的勇氣令人敬佩",
                "薩邁爾: 我和其他兩位不同，不喜歡花俏的道具或規則",
                "薩邁爾: 這場試煉，請以你自己雙眼看破未來",
                "薩邁爾: 如果你能擊敗我，我會賜予你我的羽翼",
                "薩邁爾: 談話就此打住，準備好的話就去賭桌找我吧"
            ],
        }
    }

    if npc == "Leviathan":
        character_image = leviathan_image
        if action == "normal":
            text = dialogues["Leviathan"]["normal"]
        elif action == "before_challenge":
            text = dialogues["Leviathan"]["before_challenge"]
    elif npc == "Samael":
        character_image = samael_image
        if action == "normal":
            text = dialogues["Samael"]["normal"]
        elif action == "before_challenge":
            text = dialogues["Samael"]["before_challenge"]

    for line in text:
        draw_dialogue_box(screen, line, character_image)
        pygame.display.flip()
        wait_for_enter()
    
    callback()

def wait_for_enter():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Button class
class Button:
    def __init__(self, text, x, y, width, height, callback, description):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.description = description
        self.hovered = False
        self.active = True

    def draw(self, screen):
        color = GRAY if self.hovered else WHITE
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, 
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        global Game, pretext2
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.active:
                pretext2 = ''
                self.callback()                

    def draw_description(self, screen):
        if self.hovered:
            description_surface = description_font.render(self.description, True, WHITE)
            screen.blit(description_surface, (self.rect.x, self.rect.y - 30))

# Callback functions for buttons
def start_new_game():
    global current_screen, player_name, player_health, dealer_health, main_player, dealer
    current_screen = 'enter_name'
    player_name = ""
    player_health = 10
    dealer_health = 10
    main_player = Player(player_health, [], 0)
    dealer = host()

def load_game():
    global current_screen
    if os.path.exists('savefile.pkl'):
        with open('savefile.pkl', 'rb') as f:
            global main_player, lobby_NPC
            main_player, lobby_NPC = pickle.load(f)
        current_screen = 'lobby'
    else:
        print("No saved game found!")

def quit_game():
    pygame.quit()
    sys.exit()

def enter_shop():
    global current_screen
    current_screen = 'shop'
    resized_shop_image = pygame.transform.scale(shop_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(resized_shop_image, (0, 0))
    pygame.display.flip()
    npc_interaction("Leviathan", "normal", show_shop_items)

def enter_game():
    global current_screen, Game
    current_screen = 'game'

    hp=random.randint(2,6)
    global pretext
    pretext = ''
    Game = game(player(10,[],100),computer(10,[]),hp)
    live_bullet = random.randint(1,4)
    blank = random.randint(1,4)
    item_number = random.randint(2,5)
    Game.start(live_bullet,blank,item_number)
    Game.round += 1
    draw_reload(str(live_bullet),str(blank))

def enter_challenge():
    global current_screen
    current_screen = 'challenge'
    resized_challenge_image = pygame.transform.scale(challenge_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(resized_challenge_image, (0, 0))
    pygame.display.flip()
    npc_interaction("Leviathan", "before_challenge", enter_challenge)

def return_to_lobby():
    global current_screen
    current_screen = 'lobby'

def use_mag():
    global Game
    if '放大鏡' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '放大鏡'
    Game.player.item.remove('放大鏡')

def use_hp():
    global Game
    if '香菸' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '香菸'
    Game.player.item.remove('香菸')

def use_saw():
    global Game
    if '手鋸' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '手鋸'
    Game.player.item.remove('手鋸')

def use_beer():
    global Game
    if '啤酒' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '啤酒'
    Game.player.item.remove('啤酒')

def use_hand():
    global Game
    if '手銬' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '手銬'
    Game.player.item.remove('手銬')

def use_phone():
    global Game
    if '手機' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '手機'
    Game.player.item.remove('手機')

def use_change():
    global Game
    if '轉換器' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '轉換器'
    Game.player.item.remove('轉換器')

def use_med():
    global Game
    if '過期藥物' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '過期藥物'
    Game.player.item.remove('過期藥物')

def use_drug():
    global Game
    if '禁藥' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '禁藥'
    Game.player.item.remove('禁藥')

def use_big():
    global Game
    if '大口徑子彈' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '大口徑子彈'
    Game.player.item.remove('大口徑子彈')

def use_bomb():
    global Game
    if '榴彈砲' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '榴彈砲'
    Game.player.item.remove('榴彈砲')

def use_bullet():
    global Game
    if '彈藥包' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '彈藥包'
    Game.player.item.remove('彈藥包')

def use_black_queen():
    global Game
    if '漆黑皇后' not in Game.player.item:
        return
    Game.action = 3
    Game.choose = '漆黑皇后'
    Game.player.item.remove('漆黑皇后')

def use_holy_queen():
    Game.action = 3
    Game.choose = '神聖皇后'
    Game.player.item.remove('神聖皇后')

def use_blue_queen():
    Game.action = 3
    Game.choose = '蔚藍皇后'
    Game.player.item.remove('蔚藍皇后')

def use_red_queen():
    Game.action = 3
    Game.choose = '腥紅皇后'
    Game.player.item.remove('腥紅皇后')

def use_glass_queen():
    Game.action = 3
    Game.choose = '琉璃皇后'
    Game.player.item.remove('琉璃皇后')




def shoot_dealer():
    global dealer_health, current_turn, Game, wait_for_draw
    #dealer_health -= 1
    #print("Shot at dealer! Dealer's health:", dealer_health)
    #current_turn = 'dealer'
    Game.action = 1
    wait_for_draw = 0

def shoot_self():
    global player_health, current_turn, Game, wait_for_draw
    #player_health -= 1
    #print("Shot at self! Player's health:", player_health)
    #current_turn = 'dealer'
    Game.action = 2
    wait_for_draw = 0

def check_dealer_bag():
    print("Checked dealer's bag!")

def check_game_over():
    global Game
    if Game.player.hp <= 0:
        game_over()

def check_game_win():
    global Game
    if Game.computer.hp <= 0:
        game_win()

def game_over():
    global current_screen
    current_screen = 'game_over'
    resized_game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(resized_game_over_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)  # Wait for 5 seconds
    pygame.quit()
    sys.exit()

def game_win():
    global current_screen
    current_screen = 'game_win'
    if main_player.money ==0:
        main_player.money += random.randint(23165,84565)
    else:
        main_player.money *=2
        
    resized_game_win_image = pygame.transform.scale(game_win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(resized_game_win_image, (0, 0))
    display_centered_text(f"你贏了！獲得了獎金"+str(main_player.money), color=WHITE)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds
    return_to_lobby()

# Create buttons
welcome_buttons = [
    Button("Start New Game", 300, 200, 200, 50, start_new_game, "Start a new game."),
    Button("Load Game", 300, 300, 200, 50, load_game, "Load a saved game."),
    Button("Quit Game", 300, 400, 200, 50, quit_game, "Exit the game.")
]

lobby_buttons = [
    Button("Enter Shop", 300, 200, 200, 50, enter_shop, "Visit the shop to buy items."),
    Button("Enter Game", 300, 300, 200, 50, enter_game, "Start a new game."),
    Button("Enter Challenge", 300, 400, 200, 50, enter_challenge, "Take on a challenge.")
]

shop_buttons = [
    Button("Return to Lobby", 300, 500, 200, 50, return_to_lobby, "Return to the lobby.")
]

game_buttons = [
    Button("Return to Lobby", 20, 20, 160, 40, return_to_lobby, "Return to the lobby."),
    Button("射向莊家", 20, 80, 160, 40, shoot_dealer, "Shoot the dealer"),
    Button("射向自己", 20, 140, 160, 40, shoot_self, "Shoot yourself"),
    Button("查看莊家的背包", 20, 200, 160, 40, check_dealer_bag, "Check dealer's bag")
]

challenge_buttons = [
    Button("Return to Lobby", 300, 500, 200, 50, return_to_lobby, "Return to the lobby.")
]

item_buttons = [
    Button("放大鏡", 20, 20, 40, 40, use_mag, "你可以查看現在這發子彈是實彈或空包彈"),
    Button("香菸", 20, 20, 40, 40, use_hp, "緩解壓力，回復一點血量"),
    Button("手鋸", 20, 20, 40, 40, use_saw, "鋸下散彈槍前端，下一發子彈傷害加倍"),
    Button("啤酒", 20, 20, 40, 40, use_beer, "退出並查看當前這發子彈"),
    Button("手銬", 20, 20, 40, 40, use_hand, "把莊家銬起來，下一回合莊家無法行動"),
    Button("手機", 20, 20, 40, 40, use_phone, "預知未來某一發子彈是實彈或空包彈"),
    Button("轉換器", 20, 20, 40, 40, use_change, "將實彈轉換成空包彈，空包彈轉換成實彈"),
    Button("過期藥物", 20, 20, 40, 40, use_med, "50%機率回復2點血量，50%機率損失1點血量"),
    Button("禁藥", 20, 20, 40, 40, use_drug, "70%機率血量大幅提升，30%機率中毒,由3個過期藥物合成"),
    Button("大口徑子彈", 20, 20, 40, 40, use_big, "當前子彈換成大口徑子彈並直接射出，造成3點傷害，注意這會結束你的回合,由2個手鉅和1個放大鏡合成"),
    Button("榴彈砲", 20, 20, 40, 40, use_bomb, "使用榴彈砲攻擊，若為實彈則造成自身當前血量的傷害，注意這會結束你的回合並使你剩下1點血量,由1個大口徑子彈、1個腎上腺素和1個轉換器合成"),
    Button("彈藥包", 20, 20, 40, 40, use_bullet, "直接射出所有子彈並重新裝填八顆子彈,由2個啤酒和1個香菸合成"),
    Button("漆黑皇后", 20, 20, 40, 40, use_black_queen, "將子彈重新裝填為1發5點傷害的實彈和1發空包彈，同時清空雙方物品欄"),
    Button("神聖皇后", 20, 20, 40, 40, use_holy_queen, "回復2點血量，獲得3個隨機物品，增加2格背包空間"),
    Button("蔚藍皇后", 20, 20, 40, 40, use_blue_queen, "每次輪到莊家的回合時，獲得1個隨機物品"),
    Button("腥紅皇后", 20, 20, 40, 40, use_red_queen, "每回合獲得手鉅效果並免疫莊家的手鉅雙倍傷害效果，最多觸發5次")
    
]

current_screen = 'welcome'
player_name = "" 
tutorial_prompt = False
current_turn = 'player'
dealer_health = 10
player_health = 10
Game = None

class Player:
    def __init__(self, health, items, win_count):
        self.health = health
        self.items = items
        self.win_count = win_count
        self.money = 0  # Example money amount for the player

class Shopkeeper(shopkeeper):
    def display_items(self):
        for i, item in enumerate(self.shop):
            print(f"{i}. {item.name} - {item.price}元: {item.description} (剩餘{item.stock}個)")

    def buy_item(self, index, player):
        if index < 0 or index >= len(self.shop):
            print("Invalid item selection.")
            return

        item = self.shop[index]
        if player.money >= item.price and item.stock > 0:
            player.money -= item.price
            item.raise_price()
            player.items.append(item)
            print(f"Purchased {item.name}.")
        else:
            print("Not enough money or item out of stock.")

# Initialize shopkeeper
shop_keeper = Shopkeeper()

def show_shop_items():
    resized_shop_image = pygame.transform.scale(shop_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(resized_shop_image, (0, 0))
    y_offset = 100
    for i, item in enumerate(shop_keeper.shop):
        item_text = f"{i}. {item.name} - {item.price}元: {item.description} (剩餘{item.stock}個)"
        display_text(item_text, 50, y_offset, color=WHITE)
        y_offset += 40
    display_text(f"你的金錢: {main_player.money}", 50, y_offset, color=WHITE)
    display_text("請輸入你想購買的商品編號或按ESC離開商店", 50, y_offset + 40, color=RED)
    pygame.display.flip()

def handle_shop_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            item_index = int(input("請輸入你想購買的商品編號: "))
            shop_keeper.buy_item(item_index, main_player)
            show_shop_items()
        elif event.key == pygame.K_ESCAPE:
            return_to_lobby()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        for button in shop_buttons:
            button.handle_event(event)

def resize_buttons(buttons, screen_width, screen_height):
    for button in buttons:
        if button.text == "Return to Lobby":
            button.rect.x = 20
            button.rect.y = 20
        else:
            button.rect.x = screen_width // 2 - 240 + buttons.index(button) * 180
            button.rect.y = screen_height - 60

def display_text(text, x, y, color=BLACK):
    text = str(text)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def display_centered_text(text, color=BLACK):
    text_surface = font.render(text, True, color)
    x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    y = (SCREEN_HEIGHT - text_surface.get_height()) // 2
    screen.blit(text_surface, (x, y))



def draw_dialogue_box(screen, text, character_image):
    dialogue_box_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 250, 100)
    pygame.draw.rect(screen, BLACK, dialogue_box_rect)
    pygame.draw.rect(screen, WHITE, dialogue_box_rect, 5)
    
    lines = text.split("\n")
    for i, line in enumerate(lines):
        text_surface = description_font.render(line, True, WHITE)
        screen.blit(text_surface, (dialogue_box_rect.x + 10, dialogue_box_rect.y + 10 + i * 20))
    
    character_image_resized = pygame.transform.scale(character_image, (150, 300))
    screen.blit(character_image_resized, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 400))

def draw_player_round():
    global Game, pretext
    pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 210, 200, 200))
    display_text("名字:", 20, SCREEN_HEIGHT - 200)
    display_text(player_name, 80, SCREEN_HEIGHT - 200)
    display_text("血量:", 20, SCREEN_HEIGHT - 160)
    #display_text(str(player_health), 80, SCREEN_HEIGHT - 160)
    display_text(str(Game.player.hp), 80, SCREEN_HEIGHT - 160)
    
    
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 210, 200, 200))
    display_text("莊家:", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
    display_text("Dealer", SCREEN_WIDTH - 140, SCREEN_HEIGHT - 200)
    display_text("血量:", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 160)
    #display_text(str(dealer_health), SCREEN_WIDTH - 140, SCREEN_HEIGHT - 160)
    display_text(str(Game.computer.hp), SCREEN_WIDTH - 140, SCREEN_HEIGHT - 160)
    
    display_text(pretext, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 120)
    display_text(pretext2, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80)

    item_slot_width = 50
    item_slot_height = 50
    item_slot_x_start = 230
    item_slot_y = SCREEN_HEIGHT - 110
    
    for i in range(15):
        #slot_rect = pygame.Rect(item_slot_x_start + (i % 5) * item_slot_width, item_slot_y - (i // 5) * item_slot_height, item_slot_width, item_slot_height)
        #pygame.draw.rect(screen, WHITE, slot_rect, 2)
        if Game.player.item ==[]:
            return
        if i > len(Game.player.item)-1:
            return  
        elif Game.player.item[i] == '放大鏡':
            #draw item_buttons[0] on the square
            item_buttons[0].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[0].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[0].draw(screen)
            item_buttons[0].draw_description(screen)
        elif Game.player.item[i] == '香菸':
            item_buttons[1].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[1].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[1].draw(screen)
            item_buttons[1].draw_description(screen)
        elif Game.player.item[i] == '手鋸':
            item_buttons[2].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[2].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[2].draw(screen)
            item_buttons[2].draw_description(screen)
        elif Game.player.item[i] == '啤酒':
            item_buttons[3].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[3].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[3].draw(screen)
            item_buttons[3].draw_description(screen)
        elif Game.player.item[i] == '手銬':
            item_buttons[4].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[4].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[4].draw(screen)
            item_buttons[4].draw_description(screen)
        elif Game.player.item[i] == '手機':
            item_buttons[5].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[5].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[5].draw(screen)
            item_buttons[5].draw_description(screen)
        elif Game.player.item[i] == '轉換器':
            item_buttons[6].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[6].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[6].draw(screen)
            item_buttons[6].draw_description(screen)
        elif Game.player.item[i] == '過期藥物':
            item_buttons[7].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[7].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[7].draw(screen)
            item_buttons[7].draw_description(screen)
        elif Game.player.item[i] == '禁藥':
            item_buttons[8].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[8].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[8].draw(screen)
            item_buttons[8].draw_description(screen)
        elif Game.player.item[i] == '大口徑子彈':
            item_buttons[9].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[9].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[9].draw(screen)
            item_buttons[9].draw_description(screen)
        elif Game.player.item[i] == '榴彈砲':
            item_buttons[10].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[10].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[10].draw(screen)
            item_buttons[10].draw_description(screen)
        elif Game.player.item[i] == '彈藥包':
            item_buttons[11].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[11].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[11].draw(screen)
            item_buttons[11].draw_description(screen)
        elif Game.player.item[i] == '琉璃皇后':
            item_buttons[12].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[12].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[12].draw(screen)
            item_buttons[12].draw_description(screen)
        elif Game.player.item[i] == '漆黑皇后':
            item_buttons[13].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[13].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[13].draw(screen)
            item_buttons[13].draw_description(screen)
        elif Game.player.item[i] == '神聖皇后':
            item_buttons[14].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[14].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[14].draw(screen)
            item_buttons[14].draw_description(screen)
        elif Game.player.item[i] == '蔚藍皇后':
            item_buttons[15].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[15].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[15].draw(screen)
            item_buttons[15].draw_description(screen)
        elif Game.player.item[i] == '腥紅皇后':
            item_buttons[16].rect.x = item_slot_x_start + (i % 5) * item_slot_width
            item_buttons[16].rect.y = item_slot_y - (i // 5) * item_slot_height
            item_buttons[16].draw(screen)
            item_buttons[16].draw_description(screen)
def dealer_turn():
    global player_health, current_turn
    player_health -= 1
    print("Dealer shot player! Player's health:", player_health)
    current_turn = 'player'
    time.sleep(1)

def draw_dealer_turn():
    display_text("莊家的回合", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, color=RED)
    pygame.display.update()
    #dealer_turn()

def draw_reload(live_bullet, blank):
    resized_game_image = pygame.transform.scale(game_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(resized_game_image, (0, 0))
    display_centered_text("重新裝彈，這次有"+live_bullet+"發實彈和"+blank+"發空包彈", color=WHITE)
    pygame.display.update()
    time.sleep(3)

running = True
wait_for_draw = 0
pretext = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            resize_buttons(welcome_buttons, SCREEN_WIDTH, SCREEN_HEIGHT)
            resize_buttons(lobby_buttons, SCREEN_WIDTH, SCREEN_HEIGHT)
            resize_buttons(shop_buttons, SCREEN_WIDTH, SCREEN_HEIGHT)
            resize_buttons(game_buttons, SCREEN_WIDTH, SCREEN_HEIGHT)
            resize_buttons(challenge_buttons, SCREEN_WIDTH, SCREEN_HEIGHT)

        if current_screen == 'welcome':
            for button in welcome_buttons:
                button.handle_event(event)
        elif current_screen == 'lobby':
            for button in lobby_buttons:
                button.handle_event(event)
        elif current_screen == 'shop':
            handle_shop_event(event)
        elif current_screen == 'game':
            if current_turn == 'player':
                for button in game_buttons:
                    button.handle_event(event)
                for button in item_buttons:
                    button.handle_event(event)  
        elif current_screen == 'challenge':
            for button in challenge_buttons:
                button.handle_event(event)
        elif current_screen == 'enter_name':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    tutorial_prompt = True
                    current_screen = 'tutorial_prompt'
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        elif current_screen == 'tutorial_prompt':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    current_screen = 'game'
                elif event.key == pygame.K_n:
                    current_screen = 'lobby'

    if current_screen == 'welcome':
        resized_welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_welcome_image, (0, 0))
        for button in welcome_buttons:
            button.draw(screen)
            button.draw_description(screen)
    elif current_screen == 'lobby':
        resized_lobby_image = pygame.transform.scale(lobby_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_lobby_image, (0, 0))
        display_text(f'你的名字是 {player_name}', 50, 50)
        for button in lobby_buttons:
            button.draw(screen)
            button.draw_description(screen)
    elif current_screen == 'shop':
        show_shop_items()
    elif current_screen == 'game':
        resized_game_image = pygame.transform.scale(game_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_game_image, (0, 0))
        Game.remain_bullet_count = len(Game.remain_bullet)
        check_game_over()
        check_game_win()
        if current_screen == 'game':
            if Game.remain_bullet_count == 0:
                live_bullet = random.randint(1,4)
                blank = random.randint(1,4)
                item_number = random.randint(2,5)
                Game.start(live_bullet,blank,item_number)
                Game.round += 1
                draw_reload(str(live_bullet), str(blank))

            if current_turn == 'player':
                draw_player_round()
                #wait for draw
                if wait_for_draw >= 5:
                    for button in game_buttons:
                        button.draw(screen)
                        button.draw_description(screen)
                    Game.player_turn()
                    Game.action = 0
                else:
                    wait_for_draw += 1
            elif current_turn == 'dealer':
                draw_dealer_turn()
                if wait_for_draw >= 5:
                    Game.in_between()
                    time.sleep(1)
                    Game.remain_bullet_count = len(Game.remain_bullet)
                    if Game.remain_bullet_count > 0 and current_turn == 'dealer':
                        Game.computer_turn()
                        Game.action = 0
                        time.sleep(1)
                    Game.remain_bullet_count = len(Game.remain_bullet)
                    if Game.remain_bullet_count > 0 and current_turn == 'player':
                        Game.player_turn_start()
                    time.sleep(1)
                    wait_for_draw = 0
                else:
                    wait_for_draw += 1
    elif current_screen == 'challenge':
        resized_challenge_image = pygame.transform.scale(challenge_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_challenge_image, (0, 0))
        for button in challenge_buttons:
            button.draw(screen)
            button.draw_description(screen)
    elif current_screen == 'enter_name':
        resized_welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_welcome_image, (0, 0))
        draw_dialogue_box(screen, "請輸入你的名字:", samael_image)
        display_text(player_name, 60, SCREEN_HEIGHT - 120, color=WHITE)
        pygame.display.flip()
    elif current_screen == 'tutorial_prompt':
        resized_welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_welcome_image, (0, 0))
        draw_dialogue_box(screen, "要進行新手教學嗎? (y/n)", samael_image)
        pygame.display.flip()
    elif current_screen == 'game_over':
        resized_game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_game_over_image, (0, 0))
    elif current_screen == 'game_win':
        resized_game_win_image = pygame.transform.scale(game_win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_game_win_image, (0, 0))
        display_centered_text(f"你贏了！你現在擁有" + str(main_player_money), color=WHITE)

    pygame.display.flip()

pygame.quit()
sys.exit()
