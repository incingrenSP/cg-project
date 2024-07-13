frames = {
        'fireball' : 1,
        'slash' : 2
    }

for name, items in frames.items():
    items += 1
    frames[name] = items

print(frames)