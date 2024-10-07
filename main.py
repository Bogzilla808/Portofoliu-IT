import random
import sys
import pandas as pd
import pygame
import pygame_gui
from pygame.locals import *
from threading import Timer

pygame.init()


# TODO: -------------------------------CLASSES ---------- CLASSES ----------- CLASSES ----------------------
class SaveManager:
    def load(self, lv2, attack2, defense2, currentHP2, maxHP2, currentMP2, maxMP2, gold2, currentXP2, maxXP2, skillPoints2):
        data = pd.read_csv("Data/save.csv")
        data_dict = data.to_dict()
        lv2 = data_dict['level'][0]
        attack2 = data_dict['attack'][0]
        defense2 = data_dict['defense'][0]
        currentHP2 = data_dict['currentHP'][0]
        maxHP2 = data_dict['maxHP'][0]
        currentMP2 = data_dict['currentMP'][0]
        maxMP2 = data_dict['maxMP'][0]
        gold2 = data_dict['gold'][0]
        currentXP2 = data_dict['currentXP'][0]
        maxXP2 = data_dict['maxXP'][0]
        skillPoints2 = data_dict['skillPoints'][0]
        return lv2, attack2, defense2, currentHP2, maxHP2, currentMP2, maxMP2, gold2, currentXP2, maxXP2, skillPoints2

    def save(self, data_dict):
        new_data = pd.DataFrame.from_dict(data_dict)
        new_data.to_csv("Data/save.csv", index=False)


class Entity:
    def __init__(self):
        self.gfx = pygame.transform.scale(pygame.image.load("Images/placeholder.png"), (128, 128))
        self.elements = []
        self.rect = self.gfx.get_rect(center=(400, 400))
        self.xPos = 0
        self.yPos = 0

    def draw(self, window, x, y):
        window.blit(self.gfx, (x, y))


# DROP TABLE RANDINT(1, 10000)
# DROP CHANCE = (1, 100) >>>> 1% DROP CHANCE
# IF RANDINT >= 1 && RANDINT <= 100 DROP ITEM
# ADD TREASURE CLASSES BASED ON LEVEL
# <= 1 : COMMON 60 % 6000
# >= 10 : RARE  15 % 1500
# >= 20 : CURSED 15 % 1500
# >= 30 : BLOOD 5 % 500
# >= 40 : LEGENDARY 2 % 200
# >= 50 : MYTHIC 0.1 % 10
# >= 100 : DIVINE 0.05% 5
# >= 300 : ANGELIC --- TOP TIER 0.01 % 1


rarity_list = ["common", "rare", "cursed", "blood", "legendary", "mythic", "divine", "angelic"]
quality_list = ["broken", "crude", "rusted", "normal", "prestige", "master-crafted", "ancient", "purgatory-forged"]


class Collectible(Entity):
    def __init__(self):
        super().__init__()
        self.type = "Collectible"
        self.drop_chance = 10
        self.get_rarity_quality()
        self.rarity_text = sans_font.render(f"{self.quality} {self.rarity} {self.type}", True, (0, 0, 0))
        ITEM_TEXT_LIST.append(self)  # REMOVE WHEN ITEM IS PICKED UP

    def spawn(self):
        COLLECTIBLE_LIST.append(self)

    def update(self):
        self.rarity_text = sans_font.render(f"{self.quality} {self.rarity} {self.type}", True, self.rarity_color)


    def get_rarity_quality(self):
        random_rarity = random.randint(1, 9716)
        if 1 <= random_rarity <= 6000:
            self.rarity = "Common"
            self.rarity_color = (255, 255, 255)
        elif 6000 < random_rarity <= 7500:
            self.rarity = "Rare"
            self.rarity_color = (252, 198, 3)
        elif 7500 < random_rarity <= 9000:
            self.rarity = "Cursed"
            self.rarity_color = (137, 14, 171)
        elif 9000 < random_rarity <= 9500:
            self.rarity = "Blood"
            self.rarity_color = (240, 26, 76)
        elif 9500 < random_rarity <= 9700:
            self.rarity = "Legendary"
            self.rarity_color = (240, 76, 26)
        elif 9700 < random_rarity <= 9710:
            self.rarity = "Mythic"
            self.rarity_color = (122, 240, 26)
        elif 9710 < random_rarity <= 9715:
            self.rarity = "Divine"
            self.rarity_color = (26, 26, 240)
        else:  # if random_rarity == 9716
            self.rarity = "Angelic"
            self.rarity_color = (26, 229, 240)

        # WEAPON QUALITY
        #
        # broken 1-1000     10%           ----- stats decreased by 80 %
        # rusted  1001-2500   15%         ----- stats decreased by 50 %
        # crude  2501-4500    20%         ----- stats decreased by 20 %
        # normal 4501-8000    35%         ----- normal stats ----------
        # prestige 8001-9000  10%         ----- stats increased by 15 %
        # master-crafted 9001-9500  5%    ----- stats increased by 25 %
        # ancient 9500-9980        4.8%   ----- stats increased by 40 %
        # purgatory-forged  9981-100000   0.2%  ---- stats increased by 100%
        random_quality = random.randint(1, 10000)
        if 1 <= random_quality <= 1000:
            self.quality = "Broken"
        elif 1000 < random_quality <= 2500:
            self.quality = "Rusted"
        elif 2500 < random_quality <= 4500:
            self.quality = "Crude"
        elif 4500 < random_quality <= 8000:
            self.quality = "Normal"
        elif 8000 < random_quality <= 9000:
            self.quality = "Prestige"
        elif 9000 < random_quality <= 9500:
            self.quality = "Master-Crafted"
        elif 9500 < random_quality <= 9980:
            self.quality = "Ancient"
        else:
            self.quality = "Purgatory-Forged"

# TODO: EQUIPMENT SECTION -----------------------------------------------------------------------------------------
# Weapon, HeadGear, Armor, Cloak, Gloves, Amulet, Belt, Boots


class Weapon(Collectible):
    def __init__(self):
        super().__init__()
        self.drop_chance = 20
        self.gfx = pygame.transform.scale(pygame.image.load("Images/Equipment/sword.png"), (64, 64))
        self.type = "Weapon"
        self.update()


class Tiara(Collectible):
    def __init__(self):
        super().__init__()
        self.gfx = pygame.transform.scale(pygame.image.load("Images/Equipment/Tiara.png"), (1200/10, 497/10))
        self.type = "HeadPiece"
        self.update()


class ChestPlate(Collectible):
    def __init__(self):
        super().__init__()
        self.gfx = pygame.transform.scale(pygame.image.load("Images/Equipment/Chestplate.png"), (100, 100))
        self.type = "Armor"
        self.update()


class Cloak(Collectible):
    def __init__(self):
        super().__init__()
        self.gfx = pygame.transform.scale(pygame.image.load("Images/Equipment/thief_cloak.png"), (100, 100))
        self.type = "Cloak"
        self.update()

# TODO: EQUIPMENT SECTION -----------------------------------------------------------------------------------------


class Player(Entity):
    def __init__(self):
        super().__init__()
        # STATS
        self.maxHealth = 100
        self.currentHealth = 40
        self.targetHealth = 40
        self.health_bar_length = 50
        self.currentMana = 5
        self.maxMana = 10
        self.attack = 10
        self.defense = 2
        self.isDead = False
        self.attack_range = 200

        # LEVELING
        self.currentXP = 0
        self.maxXP = 100
        self.level = 1
        self.skill_points = 1

        self.health_ratio = self.targetHealth / self.health_bar_length
        self.health_change_speed = 1

        # CURRENCY
        self.gold = 0

    def get_damage(self, amount):
        if self.targetHealth > 0:
            self.targetHealth -= amount
        if self.targetHealth <= 0:
            self.isDead = True
            self.die()

    def get_health(self, amount):
        if self.targetHealth < self.maxHealth:
            self.targetHealth += amount
        elif self.targetHealth >= self.maxHealth:
            self.targetHealth = self.maxHealth

    def level_up(self):
        self.level += 1
        self.currentXP = 0
        self.maxXP = round(self.maxXP * 1.15)
        self.skill_points += 1
        if self.currentHealth < self.maxHealth:
            self.targetHealth = self.maxHealth
        if self.currentMana < self.maxMana:
            self.currentMana = self.maxMana

    def basic_attack(self, damage, target_enemy):
        target_enemy.get_damage(damage)

    def die(self):
        self.gfx = pygame.transform.scale(pygame.image.load("Images/avatar_dead.png"), (128, 128))
        self.isDead = True
        ENEMY_LIST.clear()

        # PLAY DEATH SOUND

        t = Timer(3.0, function=self.revive)
        t.start()

    def revive(self):
        self.currentXP = 0
        self.currentHealth = self.maxHealth / 4
        self.targetHealth = self.currentHealth
        self.isDead = False


# TODO: ABILITIES ------------------------------- ABILITIES -------------------------------- ABILITIES ----------------

class FrostNova(Entity):
    def __init__(self):
        self.width = 100
        self.height = 100
        self.xPos = player.xPos
        self.yPos = player.yPos
        self.expands = True
        self.gfx = pygame.transform.scale(pygame.image.load("Images/frost_nova.png"),
                                                (self.width, self.height))

        self.cooldown = 10  # IN SECONDS
        self.damage = 100  # IGNORES ENEMY DEFENSE


class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.gfx = pygame.transform.scale(pygame.image.load("Images/placeholder.png"), (128, 128))
        self.xPos = x
        self.yPos = y
        self.counter = 0
        self.attack_speed = 1
        self.currentHealth = 60
        self.maxHealth = 100
        self.targetHealth = 60
        self.isDead = False
        self.health_bar_length = 50
        self.health_ratio = self.targetHealth / self.health_bar_length
        self.health_change_speed = 1
        self.gold_reward = 10
        self.xp_reward = 20

    def die(self):
        player.gold += self.gold_reward
        player.currentXP += self.xp_reward
        if player.currentXP >= player.maxXP:
            remaining_xp = player.currentXP - player.maxXP
            player.level_up()
            player.currentXP += remaining_xp
        self.gfx = pygame.transform.scale(pygame.image.load("Images/placeholder.png"), (0, 0))

        if random.randint(1, 2) == 2:
            new_collectible = random.choice(COLLECTIBLE_PICKER)()
            new_collectible.xPos = self.xPos
            new_collectible.yPos = self.yPos
            COLLECTIBLE_LIST.append(new_collectible)

    def update(self):
        if (abs(self.xPos - player.xPos) < 100 and abs(self.yPos - player.yPos) < 100 and
                self.counter >= self.attack_speed):
            final_enemy_damage = self.attack - player.defense
            if final_enemy_damage < 0:
                final_enemy_damage = 0
            player.get_damage(final_enemy_damage)
            self.counter = 0

    def get_damage(self, amount):
        if self.targetHealth > 0:
            self.targetHealth -= amount
        if self.targetHealth <= 0:
            self.targetHealth = 0
            self.currentHealth = 0
            self.isDead = True


class Zombie(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.gfx = pygame.transform.scale(pygame.image.load("zombie.png"), (128, 128))
        self.attack_speed = 3
        self.currentHealth = 15
        self.maxHealth = 15
        self.targetHealth = 15
        self.attack = 5
        self.defense = 0
        self.gold_reward = 5
        self.xp_reward = 10
        self.health_ratio = self.maxHealth / 100


class Ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.gfx = pygame.transform.scale(pygame.image.load("Images/ghost_edit.png"), (128, 128))
        self.attack_speed = 1
        self.currentHealth = 80
        self.maxHealth = 80
        self.targetHealth = 80
        self.attack = 10
        self.defense = 4
        self.gold_reward = 50
        self.xp_reward = 100
        self.health_ratio = self.maxHealth / 100


class Vampire(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.gfx = pygame.transform.scale(pygame.image.load("Images/vampire.png"), (128, 192))
        self.attack_speed = 0.5
        self.currentHealth = 200
        self.maxHealth = 200
        self.targetHealth = 200
        self.attack = 20
        self.defense = 10
        self.gold_reward = 120
        self.xp_reward = 215
        self.health_ratio = self.maxHealth / 100


# TODO: TILE MAP CLASS
class TileMap(pygame.sprite.Sprite):
    def __init__(self, aSpriteSheet, aMap):
        super().__init__()
        self.file = open(aMap, "r")
        self.tiles = pygame.image.load(aSpriteSheet)

    def loadMap(self):
        tileMap = []
        tileSize = 24
        for row in range(0, 20):
            tileMap.append([])
            for column in range(0, 20):
                tileMap[row].append("")
            for x in range(0, 20):
                line = self.file.readline()
                print(line)
                for y in range(0, 20):
                    if line[y] == "0":
                        tileMap[x][y] = (0, 0, 24, 24)
                    if line[y] == "6":
                        tileMap[x][y] = (0, 48, 24, 24)
                    if line[y] == "7":
                        tileMap[x][y] = (48, 48, 24, 24)
                    if line[y] == "8":
                        tileMap[x][y] = (48, 0, 24, 24)
                    if line[y] == "4":
                        tileMap[x][y] = (0, 24, 24, 24)
                    if line[y] == "5":
                        tileMap[x][y] = (48, 24, 24, 24)
                    if line[y] == "1":
                        tileMap[x][y] = (24, 0, 24, 24)
                    if line[y] == "3":
                        tileMap[x][y] = (24, 48, 24, 24)
                    if line[y] == "2":
                        tileMap[x][y] = (24, 24, 24, 24)
                    if line[y] == "T":
                        tileMap[x][y] = (0, 72, 24, 24)
                    if line[y] == "Y":
                        tileMap[x][y] = (24, 72, 24, 24)
                    if line[y] == "X":
                        tileMap[x][y] = (48, 72, 24, 24)
        print(tileMap)
        return tileMap

    def draw(self, tileMap, window):
        for x in range(0, 20):
            for y in range(0, 20):
                window.blit(self.tiles, (y*24, x*24), tileMap[x][y])

class Button:

    def __init__(self, text, x_pos, y_pos, enabled, bg_color, fg_color, width, height):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color

    def draw(self):
        button_text = sans_font.render(self.text, True, self.fg_color)
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        pygame.draw.rect(window, self.bg_color, button_rect, 0, 5)
        pygame.draw.rect(window, 'black', button_rect, 2, 5)
        window.blit(button_text, (self.x_pos + self.width/2, self.y_pos - self.height/2))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            self.enabled = False
            cd = Timer(0.1, function=self.set_enabled)
            cd.start()
            return True
        else:
            return False

    def set_enabled(self):
        self.enabled = True

# TODO: CHARACTER SCREEN CLASS
class CharacterScreen:
    def __init__(self):
        self.isActive = False
        self.gfx = pygame.transform.scale(pygame.image.load("Images/ui_menu_bg.png"), (400, 600))
        self.rect = self.gfx.get_rect(center=(200, 300))
        self.skill_points_text = sans_font.render(f"Skill Points: {player.skill_points}",
                                                  True, (0, 0, 0))
        self.attack_text = sans_font.render(f"Attack: {player.attack}", True, (0, 0, 0))
        self.defense_text = sans_font.render(f"Defense: {player.defense}", True, (0, 0, 0))
        self.maxHealth_text = sans_font.render(f"Max Health: {player.maxHealth}", True, (0, 0, 0))
        self.maxMana_text = sans_font.render(f"Max Mana: {player.maxMana}", True, (0, 0, 0))

        self.skill_points_text_rect = self.skill_points_text.get_rect()
        self.attack_text_rect = self.attack_text.get_rect()
        self.defense_text_rect = self.defense_text.get_rect()
        self.maxHealth_text_rect = self.maxHealth_text.get_rect()
        self.maxMana_text_rect = self.maxMana_text.get_rect()

        # BUTTONS
        self.attack_increase_button = Button('+', 1800, 300, True, (0, 0, 0), (255, 255, 255), 30, 30)
        self.defense_increase_button = Button('+', 1800, 350, True, (0, 0, 0), (255, 255, 255), 30, 30)
        self.maxHealth_increase_button = Button('+', 1800, 400, True, (0, 0, 0), (255, 255, 255), 30, 30)
        self.maxMana_increase_button = Button('+', 1800, 450, True, (0, 0, 0), (255, 255, 255), 30, 30)

    def draw(self, window, x, y):
        window.blit(self.gfx, (x, y))

        window.blit(self.skill_points_text, (1650, 220))
        window.blit(self.attack_text, (1550, 300))
        window.blit(self.defense_text, (1550, 350))
        window.blit(self.maxHealth_text, (1550, 400))
        window.blit(self.maxMana_text, (1550, 450))

        self.attack_increase_button.draw()
        self.defense_increase_button.draw()
        self.maxHealth_increase_button.draw()
        self.maxMana_increase_button.draw()

        self.skill_points_text = sans_font.render(f"Skill Points: {player.skill_points}",
                                                  True, (0, 0, 0))
        self.attack_text = sans_font.render(f"Attack: {player.attack}", True, (0, 0, 0))
        self.defense_text = sans_font.render(f"Defense: {player.defense}", True, (0, 0, 0))
        self.maxHealth_text = sans_font.render(f"Max Health: {player.maxHealth}", True, (0, 0, 0))
        self.maxMana_text = sans_font.render(f"Max Mana: {player.maxMana}", True, (0, 0, 0))

    def check_buttons_clicked(self):
        # add a delay

        if self.attack_increase_button.check_click():
            if player.skill_points > 0:
                player.attack += 3
                player.skill_points -= 1
            else:
                pass # ui text warning
        if self.defense_increase_button.check_click():
            if player.skill_points > 0:
                player.defense += 1
                player.skill_points -= 1
            else:
                pass # ui text warning
        if self.maxHealth_increase_button.check_click():
            if player.skill_points > 0:
                player.maxHealth += 10
                player.skill_points -= 1
            else:
                pass # ui text warning
        if self.maxMana_increase_button.check_click():
            if player.skill_points > 0:
                player.maxMana += 2
                player.skill_points -= 1
            else:
                pass # ui text warning


# TODO: END OF CLASSES ---------------- END OF CLASSES --------------------- END OF CLASSES --------------


# TODO MAIN FUNCTION --------------------- MAIN FUNCTION ------------------ MAIN FUNCTION ----------------


vel = 10
FPS = 75
GAME_RESOLUTION = (1920, 1000)  # 720p for testing
sans_font = pygame.font.Font('Fonts/FreeSansBold.ttf', 26)
count = 0

window = pygame.display.set_mode(GAME_RESOLUTION)
pygame.display.set_caption('Crystal Souls')
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((1920, 1000))

save_manager = SaveManager()

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 500), (100, 100)),
                                                text="Say Hello", manager=manager)

ITEM_TEXT_LIST = []
item_text_enabled = False

ENEMY_LIST = []
ENEMY_PICKER = [Ghost, Zombie, Vampire]

COLLECTIBLE_LIST = []
COLLECTIBLE_PICKER = [Weapon, Tiara, ChestPlate, Cloak]  # Gloves, Amulet, Belt, Boots

ABILITY_LIST = []

# Update the display using flip
pygame.display.flip()

running = True

# level = TileMap("char_sprite.png", "map.txt")
# tiles = level.loadMap()

player = Player()

currentHealthData = 0
maxHealthData = 0
levelData = 0
attackData = 0
defenseData = 0
currentManaData = 0
maxManaData = 0
goldData = 0
currentXPData = 0
maxXPData = 0
skillPointsData = 0

(player.level, player.attack, player.defense, player.currentHealth, player.maxHealth,
player.currentMana, player.maxMana, player.gold, player.currentXP, player.maxXP, player.skill_points) = (save_manager.load(levelData, attackData,
defenseData, currentHealthData, maxHealthData, currentManaData, maxManaData, goldData, currentXPData, maxXPData, skillPointsData))
player.targetHealth = player.currentHealth

character_screen = CharacterScreen()

facing_left = True
facing_right = False
facing_back = True

# game loop
while running:

    time_delta = clock.tick(60)/1000.0
    manager.draw_ui(window)
    window.fill((61, 61, 61))
    # level.draw(tiles, window)

    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            currentHealthData = player.currentHealth
            maxHealthData = player.maxHealth
            levelData = player.level
            attackData = player.attack
            defenseData = player.defense
            currentManaData = player.currentMana
            maxManaData = player.maxMana
            goldData = player.gold
            currentXPData = player.currentXP
            maxXPData = player.maxXP
            skillPointsData = player.skill_points

            new_data_dict = {"level": {0: levelData}, "attack": {0: attackData}, "defense": {0: defenseData},
                             "currentHP": {0: currentHealthData}, "maxHP": {0: maxHealthData},
                             "currentMP": {0: currentManaData}, "maxMP": {0: maxManaData},
                             "gold": {0: goldData}, "currentXP": {0: currentXPData},
                             "maxXP": {0: maxXPData}, "skillPoints": {0: skillPointsData}}
            save_manager.save(new_data_dict)

            running = False
            sys.exit()

        # FOR TESTING --------------------------------------
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h and not player.isDead:
            player.get_health(10)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f and not player.isDead:
            player.get_damage(10)
        # FOR TESTING --------------------------------------

        # FROST NOVA KEY -----------------------------------
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not player.isDead:
            new_nova = FrostNova()
            ABILITY_LIST.append(new_nova)

        # ENABLE/DISABLE ITEMS KEY
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LALT or pygame.K_RALT:
            if item_text_enabled:
                item_text_enabled = False
            else:
                item_text_enabled = True

        # CHARACTER SCREEN KEY ----------------------------
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c and not player.isDead:
            if not character_screen.isActive:
                character_screen.isActive = True
            else:
                character_screen.isActive = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_LEFT and not player.isDead:
            for enemy in ENEMY_LIST:
                if (abs(enemy.xPos - player.xPos) < player.attack_range and
                        abs(enemy.yPos - player.yPos) < player.attack_range):
                    final_damage = player.attack - enemy.defense
                    if final_damage < 0:
                        final_damage = 0
                    player.basic_attack(target_enemy=enemy, damage=final_damage)

        manager.process_events(event)
    manager.update(time_delta)

    # TODO: ----------------------------PLAYER CONTROLLER------------------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and not player.isDead:
        player.xPos -= vel
        facing_back = False
        if not facing_left:
            player.gfx = pygame.transform.flip(player.gfx, flip_x=True, flip_y=False)
            facing_right = False
            facing_left = True
    if keys[pygame.K_w] and not player.isDead:
        player.yPos -= vel
        facing_back = True
    if keys[pygame.K_s] and not player.isDead:
        player.yPos += vel
        facing_back = False
        facing_right = False
        facing_left = True
    if keys[pygame.K_d] and not player.isDead:
        player.xPos += vel
        facing_back = False
        player.gfx = pygame.transform.flip(player.gfx, flip_x=True, flip_y=False)
        facing_right = True
        facing_left = False

    if facing_back and not player.isDead:
        player.gfx = pygame.transform.scale(pygame.image.load("Images/avatar_behind.png"), (128, 128))
    elif not facing_back and not player.isDead:
        player.gfx = pygame.transform.scale(pygame.image.load("Images/avatar.png"), (128, 128))

    if facing_right and not player.isDead:
        player.gfx = pygame.transform.flip(player.gfx, flip_x=True, flip_y=False)

    # TODO: ------------------------------END PLAYER CONTROLLER-----------------------------------------

    # TODO: ------------------------------PLAYER HEALTHBAR --------------------------------------------
    transition_width = 0
    transition_color = (255, 0, 0)

    # clamping health
    if player.currentHealth < 0:
        player.currentHealth = 0
        player.targetHealth = 0
    if player.currentHealth > player.maxHealth:
        player.currentHealth = player.maxHealth
        player.targetHealth = player.maxHealth

    # adding health
    if player.currentHealth < player.targetHealth:
        player.currentHealth += player.health_change_speed
        transition_width = int((player.targetHealth - player.currentHealth)/player.health_ratio)
        transition_color = pygame.Color("limegreen")

    # removing health
    if player.currentHealth > player.targetHealth:
        player.currentHealth -= player.health_change_speed
        transition_width = -(int((player.targetHealth - player.currentHealth)/player.health_ratio))
        transition_color = (255, 255, 0)

    health_bar_rect = pygame.Rect(player.xPos, player.yPos-25, player.currentHealth/player.health_ratio, 25)
    transition_bar_rect = pygame.Rect(health_bar_rect.right, player.yPos-25, transition_width, 25)

    pygame.draw.rect(window, (255, 0, 0), health_bar_rect)
    pygame.draw.rect(window, transition_color, transition_bar_rect)
    pygame.draw.rect(window, (255, 255, 255), (player.xPos, player.yPos-25,
                     player.maxHealth/player.health_ratio, 25), 4)

    # TODO: ------------------------------ END PLAYER HEALTHBAR ---------------------------------------

    # TODO: ------------------------------ ENEMY SPAWNER ---------------------------------------------
    if random.randint(1, 100) == 5 and not player.isDead:
        new_enemy = random.choice(ENEMY_PICKER)(random.randint(100, 1000), random.randint(100, 500))
        ENEMY_LIST.append(new_enemy)

    for enemy in ENEMY_LIST:
        enemy.counter += 2/FPS

        transition_width2 = 0
        transition_color2 = (255, 0, 0)

        if enemy.currentHealth < enemy.targetHealth and not enemy.isDead:
            enemy.currentHealth += enemy.health_change_speed
            transition_width2 = int((enemy.targetHealth - enemy.currentHealth) / enemy.health_ratio)
            transition_color2 = pygame.Color("limegreen")

        # removing health
        if enemy.currentHealth > enemy.targetHealth and not enemy.isDead:
            enemy.currentHealth -= player.health_change_speed
            transition_width2 = -(int((enemy.targetHealth - enemy.currentHealth) / enemy.health_ratio))
            transition_color2 = (255, 255, 0)
        if not enemy.isDead:
            health_bar_rect2 = pygame.Rect(enemy.xPos, enemy.yPos - 25, enemy.currentHealth / enemy.health_ratio, 25)
            transition_bar_rect2 = pygame.Rect(health_bar_rect2.right, enemy.yPos - 25, transition_width2, 25)

            pygame.draw.rect(window, (255, 0, 0), health_bar_rect2)
            pygame.draw.rect(window, transition_color2, transition_bar_rect2)
            pygame.draw.rect(window, (255, 255, 255), (enemy.xPos, enemy.yPos - 25,
                                                       enemy.maxHealth / enemy.health_ratio, 25), 4)

        if enemy.isDead:
            ENEMY_LIST.remove(enemy)
            enemy.die()

    # TODO: ------------------------------ END ENEMY SPAWNER ---------------------------------------------

    for collectible in COLLECTIBLE_LIST:
        collectible.draw(window, collectible.xPos, collectible.yPos)
        window.blit(collectible.rarity_text, (collectible.xPos-100, collectible.yPos-50))


    # TODO: ------------------------------ ENEMY AI ------------------------------------------------

    for enemy in ENEMY_LIST:
        if abs(enemy.xPos - player.xPos) > 50 and not enemy.isDead and not player.isDead:
            if enemy.xPos > player.xPos:
                enemy.xPos -= 1
            else:
                enemy.xPos += 1
        if abs(enemy.yPos - player.yPos) > 50 and not enemy.isDead and not player.isDead:
            if enemy.yPos > player.yPos:
                enemy.yPos -= 1
            else:
                enemy.yPos += 1
        enemy.draw(window, enemy.xPos, enemy.yPos)
        enemy.update()

    # TODO: ------------------------------ END ENEMY AI ---------------------------------------------

    # TODO: ----------------------- DISPLAY PLAYER DETAILS UI ----------------------------------------
    gold_xp_lv_text = sans_font.render(f"Gold: {player.gold} | LV: {player.level} | "
                            f" XP:{player.currentXP}/{player.maxXP}", True, (255, 255, 255))
    textRect = gold_xp_lv_text.get_rect()
    textRect.center = (200, GAME_RESOLUTION[1]-70)
    textRect.left = 10
    window.blit(gold_xp_lv_text, textRect)

    health_mana_text = sans_font.render(f"Health: {player.currentHealth}/{player.maxHealth} | "
                                         f"Mana: {player.currentMana}/{player.maxMana}",
                                        True, (255, 255, 255))
    health_mana_textRect = health_mana_text.get_rect()
    health_mana_textRect.center = (200, GAME_RESOLUTION[1]-30)
    health_mana_textRect.left = 10
    window.blit(health_mana_text, health_mana_textRect)

    for text in ITEM_TEXT_LIST:
        if item_text_enabled:
            item_text_rect = # rect here
            window.blit(text, item_text_rect)
    # TODO: ----------------------- END DISPLAY PLAYER DETAILS UI ------------------------------------

    # TODO : ------------------------ ABILITIES ------------------------------------------------------

    for ability in ABILITY_LIST:
        ability.draw(window, ability.xPos, ability.yPos)

        # INCREASE NOVA SIZES
        if ability.expands:
            ability.gfx = pygame.transform.scale(ability.gfx, (ability.width+1, ability.height+1))
            ability.width += 1
            ability.height += 1

    # TODO: -------------------------- END ABILITIES -------------------------------------------------

    player.draw(window, player.xPos, player.yPos)

    # TODO: ----------------------- CHARACTER SCREEN -------------------------------------------------

    if character_screen.isActive:
        character_screen.draw(window, GAME_RESOLUTION[0] - 400, GAME_RESOLUTION[1] / 2 - 300)
        character_screen.check_buttons_clicked()

    # TODO: ----------------------- CHARACTER SCREEN -------------------------------------------------

    pygame.display.update()
    clock.tick(FPS)

# TODO: ------------------- END MAIN FUNCTION ---------------------- END MAIN FUNCTION -----------------------

