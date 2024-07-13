import os

item_data = {
    'potion' : {'cooldown' : 200, 'heal' : 50, 'graphics' : os.path.join('graphics', 'icons', 'potion.png')},
    'hi-potion' : {'cooldown' : 200, 'heal' : 150, 'graphics' : os.path.join('graphics', 'icons', 'hi_potion.png')},
    'elixir' : {'cooldown' : 200, 'heal' : 1000, 'graphics' : os.path.join('graphics', 'icons', 'elixir.png')}
}
item_name = list(item_data.keys())[0]
heals = list(item_data.values())[0]['heal']
print(item_name)
print(heals)