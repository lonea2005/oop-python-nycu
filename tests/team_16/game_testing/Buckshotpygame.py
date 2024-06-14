import pygame
import sys
import os
import pickle
import time
import random
from Buckshot_Roulette import NPC, all_item, shop_item, shopkeeper, host, collection_manager

os.chdir('/home/sam/oop-python-nycu/tests/team_16/game_testing')

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
    character_image = pygame.image.load('薩邁爾.png')
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Define NPC interactions
def npc_interaction(npc, action):
    dialogues = {
        "Leviathan": {
            "normal": [
                "利維坦: 小老弟買顆心臟吧，你死了可就沒人陪我聊天了",
                "利維坦叼了根菸，悠閒地滑著手機",
                "利維坦不在，店裡空無一人，商品靜靜的陳列著",
                "利維坦把玩著手銬和槍械零件，似乎沒注意到你"
            ],
            "before_challenge": [
                "利維坦: 小夥子要挑戰我? 希望你已經做好赴死的心理準備了，我可不會手下留情喔",
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
        if action == "normal":
            text = random.choice(dialogues["Leviathan"]["normal"])
        elif action == "before_challenge":
            text = random.choice(dialogues["Leviathan"]["before_challenge"])
    elif npc == "Samael":
        if action == "normal":
            text = random.choice(dialogues["Samael"]["normal"])
        elif action == "before_challenge":
            text = random.choice(dialogues["Samael"]["before_challenge"])

    draw_dialogue_box(screen, text, character_image)
    pygame.display.flip()
    time.sleep(3)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, callback, description):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.description = description
        self.hovered = False

    def draw(self, screen):
        color = GRAY if self.hovered else WHITE
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2, 
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
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
    npc_interaction("Leviathan", "normal")

def enter_game():
    global current_screen
    current_screen = 'game'

def enter_challenge():
    global current_screen
    current_screen = 'challenge'
    npc_interaction("Leviathan", "before_challenge")

def return_to_lobby():
    global current_screen
    current_screen = 'lobby'

def shoot_dealer():
    global dealer_health, current_turn
    dealer_health -= 1
    print("Shot at dealer! Dealer's health:", dealer_health)
    current_turn = 'dealer'

def shoot_self():
    global player_health, current_turn
    player_health -= 1
    print("Shot at self! Player's health:", player_health)
    current_turn = 'dealer'

def check_dealer_bag():
    print("Checked dealer's bag!")

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

current_screen = 'welcome'
player_name = ""
tutorial_prompt = False
current_turn = 'player'
dealer_health = 10
player_health = 10

class Player:
    def __init__(self, health, items, win_count):
        self.health = health
        self.items = items
        self.win_count = win_count
        self.money = 1000000  # Example money amount for the player

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

def draw_shop():
    screen.fill(WHITE)
    y_offset = 100
    for i, item in enumerate(shop_keeper.shop):
        item_text = f"{i}. {item.name} - {item.price}元: {item.description} (剩餘{item.stock}個)"
        display_text(item_text, 50, y_offset)
        y_offset += 40
    display_text(f"你的金錢: {main_player.money}", 50, y_offset)
    pygame.display.flip()

def handle_shop_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            item_index = int(input("請輸入你想購買的商品編號: "))
            shop_keeper.buy_item(item_index, main_player)
        elif event.key == pygame.K_ESCAPE:
            return_to_lobby()

def resize_buttons(buttons, screen_width, screen_height):
    for button in buttons:
        if button.text == "Return to Lobby":
            button.rect.x = 20
            button.rect.y = 20
        else:
            button.rect.x = screen_width // 2 - 240 + buttons.index(button) * 180
            button.rect.y = screen_height - 60

def display_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_dialogue_box(screen, text, character_image):
    dialogue_box_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 250, 100)
    pygame.draw.rect(screen, BLACK, dialogue_box_rect)
    pygame.draw.rect(screen, WHITE, dialogue_box_rect, 5)
    
    text_surface = description_font.render(text, True, WHITE)
    screen.blit(text_surface, (dialogue_box_rect.x + 10, dialogue_box_rect.y + 10))
    
    character_image_resized = pygame.transform.scale(character_image, (150, 300))
    screen.blit(character_image_resized, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 400))

def draw_player_round():
    pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 210, 200, 200))
    display_text("名字:", 20, SCREEN_HEIGHT - 200)
    display_text(player_name, 80, SCREEN_HEIGHT - 200)
    display_text("血量:", 20, SCREEN_HEIGHT - 160)
    display_text(str(player_health), 80, SCREEN_HEIGHT - 160)
    
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 210, 200, 200))
    display_text("莊家:", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
    display_text("Dealer", SCREEN_WIDTH - 140, SCREEN_HEIGHT - 200)
    display_text("血量:", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 160)
    display_text(str(dealer_health), SCREEN_WIDTH - 140, SCREEN_HEIGHT - 160)
    display_text("說明:", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 120)
    
    item_slot_width = 50
    item_slot_height = 50
    item_slot_x_start = 230
    item_slot_y = SCREEN_HEIGHT - 110
    
    for i in range(15):
        slot_rect = pygame.Rect(item_slot_x_start + (i % 5) * item_slot_width, item_slot_y - (i // 5) * item_slot_height, item_slot_width, item_slot_height)
        pygame.draw.rect(screen, WHITE, slot_rect, 2)

def dealer_turn():
    global player_health, current_turn
    player_health -= 1
    print("Dealer shot player! Player's health:", player_health)
    current_turn = 'player'
    time.sleep(1)

def draw_dealer_turn():
    display_text("莊家的回合", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2, color=RED)
    dealer_turn()

running = True
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
        draw_shop()
    elif current_screen == 'game':
        resized_game_image = pygame.transform.scale(game_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_game_image, (0, 0))
        if current_turn == 'player':
            draw_player_round()
            for button in game_buttons:
                button.draw(screen)
                button.draw_description(screen)
        elif current_turn == 'dealer':
            draw_dealer_turn()
    elif current_screen == 'challenge':
        resized_challenge_image = pygame.transform.scale(challenge_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_challenge_image, (0, 0))
        for button in challenge_buttons:
            button.draw(screen)
            button.draw_description(screen)
    elif current_screen == 'enter_name':
        resized_welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_welcome_image, (0, 0))
        draw_dialogue_box(screen, "請輸入你的名字:", character_image)
        display_text(player_name, 60, SCREEN_HEIGHT - 120, color=WHITE)
        pygame.display.flip()
    elif current_screen == 'tutorial_prompt':
        resized_welcome_image = pygame.transform.scale(welcome_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(resized_welcome_image, (0, 0))
        draw_dialogue_box(screen, "要進行新手教學嗎? (y/n)", character_image)
        pygame.display.flip()

    pygame.display.flip()

pygame.quit()
sys.exit()
