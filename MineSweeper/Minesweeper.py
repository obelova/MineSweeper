from tkinter import *
import random
import sys
GRID_SIZE = 10
SQUARE_SIZE = 50
MINES_NUM = 20
mines = set(random.sample(range(1, GRID_SIZE**2+1), MINES_NUM))
clicked = set()
global a
def pris1(x):
    a=1
    return root.destroy
def pris0(x):
    a=0
    return root.destroy
def check_mines(neighbors):
    return len(mines.intersection(neighbors))
def generate_neighbors(square):
    # Левая верхняя клетка
    if square == 1:
        data = {GRID_SIZE + 1, 2, GRID_SIZE + 2}
    # Правая нижняя 
    elif square == GRID_SIZE ** 2:
        data = {square - GRID_SIZE, square - 1, square - GRID_SIZE - 1}
    # Левая нижняя
    elif square == GRID_SIZE:
        data = {GRID_SIZE - 1, GRID_SIZE * 2, GRID_SIZE * 2 - 1}
    # Верхняя правая
    elif square == GRID_SIZE ** 2 - GRID_SIZE + 1:
        data = {square + 1, square - GRID_SIZE, square - GRID_SIZE + 1}
    # Клетка в левом ряду
    elif square < GRID_SIZE:
        data = {square + 1, square - 1, square + GRID_SIZE,
                square + GRID_SIZE - 1, square + GRID_SIZE + 1}
    # Клетка в правом ряду
    elif square > GRID_SIZE ** 2 - GRID_SIZE:
        data = {square + 1, square - 1, square - GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1}
    # Клетка в нижнем ряду
    elif square % GRID_SIZE == 0:
        data = {square + GRID_SIZE, square - GRID_SIZE, square - 1,
                square + GRID_SIZE - 1, square - GRID_SIZE - 1}
    # Клетка в верхнем ряду
    elif square % GRID_SIZE == 1:
        data = {square + GRID_SIZE, square - GRID_SIZE, square + 1,
                square + GRID_SIZE + 1, square - GRID_SIZE + 1}
    # Любая другая клетка
    else:
        data = {square - 1, square + 1, square - GRID_SIZE, square + GRID_SIZE,
                square - GRID_SIZE - 1, square - GRID_SIZE + 1,
                square + GRID_SIZE + 1, square + GRID_SIZE - 1}
    return data
def clearance(ids):
    clicked.add(ids) 
    ids_neigh = generate_neighbors(ids)
    around = check_mines(ids_neigh) 
    c.itemconfig(ids, fill="green") 
    if around == 0:
        # Создаем список соседних клеток
        neigh_list = list(ids_neigh)
        # Пока в списке соседей есть клетки
        while len(neigh_list) > 0:
            item = neigh_list.pop()
            c.itemconfig(item, fill="green")
            # соседение клетки данной клетки
            item_neigh = generate_neighbors(item)
            #  количество мин в соседних клетках
            item_around = check_mines(item_neigh)
            # Если в соседних клетках есть мины
            if item_around > 0:
                # Делаем эту проверку, чтобы писать по нескольку раз на той же клетке
                if item not in clicked:
                    # Получаем координаты этой клетки
                    x1, y1, x2, y2 = c.coords(item)
                    # Пишем на клетке количество мин вокруг
                    c.create_text(x1 + SQUARE_SIZE / 2,
                                  y1 + SQUARE_SIZE / 2,
                                  text=str(item_around),
                                  font="Arial {}".format(int(SQUARE_SIZE / 2)),
                                  fill='yellow')
            # Если в соседних клетках мин нету
            else:
                # Добавляем соседние клетки данной клетки в общий список
                neigh_list.extend(set(item_neigh).difference(clicked))
                # Убираем повторяющиеся элементы из общего списка
                neigh_list = list(set(neigh_list))
            # Добавляем клетку в нажатые
            clicked.add(item)
    else:
        x1, y1, x2, y2 = c.coords(ids)
        c.create_text(x1 + SQUARE_SIZE / 2,
                      y1 + SQUARE_SIZE / 2,
                      text=str(around),
                      font="Arial {}".format(int(SQUARE_SIZE / 2)),
                      fill='yellow')
def click(event):
    ids = c.find_withtag(CURRENT)[0]
    if ids in mines:
        c.itemconfig(CURRENT, fill="red")
        button = Button(root, text='Вы проиграли. Если хотите начать заново, нажмите на эту кнопку!', width=60, height=5,
                        bg='white', fg='black', font='arial 13',
                        command=pris1(1))
        button1 = Button(root, text='Вы проиграли. Если хотите закрыть, нажмите на эту кнопку!', width=60, height=5,
                        bg='white', fg='black', font='arial 13',
                        command=exit)
        button.pack()
        button1.pack()
        root.mainloop()
    elif ids not in clicked:
        clearance(ids)
        c.itemconfig(CURRENT, fill="green")
    c.update()


def mark_mine(event):
    ids = c.find_withtag(CURRENT)[0]
    if ids not in clicked:
        clicked.add(ids)
        x1, y1, x2, y2 = c.coords(ids)
        c.itemconfig(CURRENT, fill="yellow")
    else:
        clicked.remove(ids)
        c.itemconfig(CURRENT, fill="gray")
        
a=1
while a:        
    root = Tk()
    root.title("MineSweeper")
    c = Canvas(root, width=GRID_SIZE * SQUARE_SIZE, height=GRID_SIZE * SQUARE_SIZE)
    c.bind("<Button-1>", click)
    c.bind("<Button-3>", mark_mine)
    c.pack()
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
          c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                             i * SQUARE_SIZE + SQUARE_SIZE,
                             j * SQUARE_SIZE + SQUARE_SIZE, fill='gray')
    root.mainloop()
