import random

def create_falaise(posx, posy):
    pos_falaises = []
    rand = random.randint(0, 3)
    if rand == 0:
        pos_falaises += forme_falaiseA(posx, posy)

    elif rand == 1:
        pos_falaises += forme_falaiseB(posx, posy)
    
    elif rand == 2:
        pos_falaises += forme_falaiseC(posx, posy)

    elif rand == 3:
        pos_falaises += forme_falaiseD(posx, posy)
    
    return pos_falaises

def forme_falaiseA(posx, posy):
    pos_falaises = []
    current_x, current_y = posx, posy

    pos_falaises.append((current_x, current_y))

    for i in range(1, 13):
        pos_falaises.append((current_x + i, current_y))
    current_x += 12

    for i in range(1, 4):
        pos_falaises.append((current_x, current_y + i))
    current_y += 3

    for i in range(1, 10):
        pos_falaises.append((current_x + i, current_y))
    current_x += 9

    for i in range(1, 8):
        pos_falaises.append((current_x, current_y + i))
    current_y += 7

    for i in range(1, 4):
        pos_falaises.append((current_x + i, current_y))
    current_x += 3

    for i in range(1, 12):
        pos_falaises.append((current_x, current_y + i))
    current_y += 11

    for i in range(1, 8):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 7

    for i in range(1, 4):
        pos_falaises.append((current_x, current_y - i))
    current_y -= 3

    for i in range(1, 12):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 11

    for i in range(1, 4):
        pos_falaises.append((current_x, current_y - i))
    current_y -= 3

    for i in range(1, 7):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 6

    for i in range(1, 15):
        pos_falaises.append((current_x, current_y - i))

    # Passages
    del pos_falaises[5:8]
    del pos_falaises[34:37]

    return pos_falaises

def forme_falaiseB(posx, posy):
    pos_falaises = []
    current_x, current_y = posx, posy
    
    pos_falaises.append((current_x, current_y))
    
    for i in range(1, 12):
        pos_falaises.append((current_x + i, current_y))
    current_x += 11
    
    for i in range(1, 5):
        pos_falaises.append((current_x, current_y + i))
    current_y += 4
    
    for i in range(1, 4):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 3
    
    for i in range(1, 8):
        pos_falaises.append((current_x, current_y + i))
    current_y += 7
    
    for i in range(1, 10):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 9
    
    for i in range(1, 12):
        pos_falaises.append((current_x, current_y - i))

        # Passages
    del pos_falaises[5:8]
    del pos_falaises[34:37]
    
    return pos_falaises

def forme_falaiseC(posx, posy):
    pos_falaises = []
    current_x, current_y = posx, posy

    pos_falaises.append((current_x, current_y))

    for i in range(1, 12):
        pos_falaises.append((current_x, current_y + i))
    current_y += 11

    for i in range(1, 4):
        pos_falaises.append((current_x + i, current_y))
    current_x += 3

    for i in range(1, 3):
        pos_falaises.append((current_x, current_y + i))
    current_y += 2

    for i in range(1, 7):
        pos_falaises.append((current_x + i, current_y))
    current_x += 6

    for i in range(1, 5):
        pos_falaises.append((current_x, current_y - i))
    current_y -= 4

    for i in range(1, 7):
        pos_falaises.append((current_x + i, current_y))
    current_x += 6

    for i in range(1, 10):
        pos_falaises.append((current_x, current_y - i))
    current_y -= 9

    for i in range(1, 15):
        pos_falaises.append((current_x - i, current_y))

        # Passages
    del pos_falaises[5:8]
    del pos_falaises[34:37]

    return pos_falaises

def forme_falaiseD(posx, posy):
    pos_falaises = []
    current_x, current_y = posx, posy

    pos_falaises.append((current_x, current_y))

    for i in range(1, 16):
        pos_falaises.append((current_x + i, current_y))
    current_x += 15

    for i in range(1, 14):
        pos_falaises.append((current_x, current_y + i))
    current_y += 13

    for i in range(1, 8):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 7

    for i in range(1, 3):
        pos_falaises.append((current_x, current_y + i))
    current_y += 2

    for i in range(1, 13):
        pos_falaises.append((current_x - i, current_y))
    current_x -= 12

    for i in range(1, 7):
        pos_falaises.append((current_x, current_y - i))
    current_y -= 6

    for i in range(1, 5):
        pos_falaises.append((current_x + i, current_y))
    current_x += 4

    for i in range(1, 9):
        pos_falaises.append((current_x, current_y - i))

    del pos_falaises[5:8]
    del pos_falaises[18:21]

    return pos_falaises




# Test pour voir la forme de la falaise
falaises = forme_falaiseB(0, 0)

xs = [x for x, y in falaises]
ys = [y for x, y in falaises]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

grid = []
for y in range(min_y, max_y + 1):
    row = []
    for x in range(min_x, max_x + 1):
        if (x, y) in falaises:
            row.append('F')
        else:
            row.append('_')
    grid.append(''.join(row))

print("\nForme de la falaise :\n")
for row in grid:
    print(row)

print(f"\nNombre de tuiles : {len(falaises)}")
print(f"Doublons : {len(falaises) - len(set(falaises))}")
    

print(falaises)

    

