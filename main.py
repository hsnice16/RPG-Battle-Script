from classes.RPGgame import Person, bcolors
from classes.magic import Spell
from classes.Inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 45, 600, "black")
thunder = Spell("Thunder", 45, 600, "black")
blizzard = Spell("Blizzard", 45, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 44, 140, "black")

# Create White Magic
cure = Spell("Cure", 544, 720, "white")
cura = Spell("Cura", 778, 1500, 'white')


# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spell = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spell = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Valos   ", 4460, 844, 900, 34, player_spell, player_items)
player2 = Person("LocalMan", 2460, 844, 900, 34, player_spell, player_items)
player3 = Person("Robot   ", 5460, 844, 900, 34, player_spell, player_items)

enemy1 = Person("Imp     ", 1249, 714, 755, 345, enemy_spell, [])
enemy2 = Person("Magus   ", 11200, 923, 966, 25, enemy_spell, [])
enemy3 = Person("Imp     ", 1249, 714, 755, 345, enemy_spell, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("======================================")
    print("\a\a")
    print("Name                      Hp                                      Mp")

    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    print("\a\a")

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_dmg()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_dmg(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage. ")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_dmg(dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deal", str(magic_dmg), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name.replace(" ", "") + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name.replace(" ", "") + " fully restores HP/Mp" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(bcolors.FAIL + "\n" + item.name.replace(" ", "") + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # check if battle is over
    defeated_enemies = 0
    defeated_player = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_player += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    # check if player is won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win" + bcolors.ENDC)
        running = False

    # check if enemy is won
    elif defeated_player == 2:
        print(bcolors.FAIL + "Your enemies has defeated you!" + bcolors.ENDC)
        running = False

    # enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            # choose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_dmg()

            players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg, ".")
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name.replace(" ", "") + " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deal", str(magic_dmg),
                      "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
