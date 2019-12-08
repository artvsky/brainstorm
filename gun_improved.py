from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# создаёт холст
root=tk.Tk()
fr=tk.Frame(root)
root.geometry('800x600')
canv=tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

colors_of_rainbow=['red','orange','yellow','green','cyan','blue','violet'] # список цветов

class Shell(): # определяет класс снарядов

	def __init__(self, x=40, y=450):
		"""
		Конструктор класса снарядов
		Атрибуты:
		x - начальное положение снаряда по горизонтали
		y - начальное положение снаряда по вертикали
		r - радиус снаряда
		vx - начальная скорость снаряда по горизонтали
		vy - начальная скорость снаряда по вертикали
		color - цвет снаряда
		id - фигура из холста
		life - время жизни
		"""
		global colors
		self.x=x
		self.y=y
		self.r=10
		self.vx=0
		self.vy=0
		self.color=choice(colors_of_rainbow)
		self.id=canv.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color)
		self.live=30

	def set_coords(self): # обновляет координаты снаряда
		canv.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

	def move(self): # двигает снаряд
		"""
		Перемещает снаряд по прошествии единицы времени
		Метод описывает перемещение снаряда за один кадр перерисовки
		То есть, обновляет значения self.x и self.y с учетом скоростей self.vx и self.vy, гравитации и стен по краям окна
		Убивает снаряд, если тот вылетает за нижнюю или правую границу поля
		"""
		if self.y<=600:
			self.x+=self.vx
			self.y-=self.vy
			self.vy=self.vy-4.0
			self.set_coords()
		else:
			if self.live<0:
				balls.pop(balls.index(self))
				canv.delete(self.id)
			else:
				self.live=self.live-1
		if self.x>800:
			self.vx=-self.vx*0.8
			self.x=799
		elif self.y>600:
			canv.delete(self.id)

	def hittest(self, obj):
		"""
		Функция проверяет, сталкивается ли данный снаряд с целью, описываемой в обьекте obj
		Атрибуты:
		obj - объект, с которым проверяется столкновение
		return - возвращает True в случае столкновения мяча и цели, иначе возвращает False.
		"""
		if ((obj.x-self.x)**2+(obj.y-self.y)**2)<=((obj.r+self.r)**2):
			return True
		else:
			return False

class Gun(): # определяет класс пушек
	def __init__(self):
		"""
		Инициализация пушки
		"""
		self.f2_power=10
		self.f2_on=0
		self.an=1
		self.id=canv.create_line(20, 450, 50, 420, width=7)

	def fire2_start(self, event):
		self.f2_on=1

	def fire2_end(self, event):
		"""
		Выстрел снарядом
		Происходит при отпускании кнопки мыши
		Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
		balls - список всех снарядов
		bullet_1 - счёт снарядов, потраченных на первую цель (обнуляется после попадания)
		bullet_2 - счёт снарядов, потраченных на вторую цель (обнуляется после попадания)
		"""
		global balls, bullet_1, bullet_2
		bullet_1+=1
		bullet_2+=1
		new_ball=Shell()
		new_ball.r+=5
		self.an=math.atan((event.y-new_ball.y)/(event.x-new_ball.x))
		new_ball.vx=self.f2_power*math.cos(self.an)
		new_ball.vy=-self.f2_power*math.sin(self.an)
		balls+=[new_ball]
		self.f2_on=0
		self.f2_power=10

	def targetting(self, event=0):
		"""
		Прицеливание. Зависит от положения мыши
		"""
		if event:
			self.an=math.atan((event.y-450)/(event.x-20))
		if self.f2_on:
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')
		canv.coords(self.id, 20, 450, 20+max(self.f2_power, 20)*math.cos(self.an), 450+max(self.f2_power, 20)*math.sin(self.an))

	def power_up(self):
		if self.f2_on:
			if self.f2_power<100:
				self.f2_power+=1
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')

class Target():

	def __init__(self, color_new): # инициализация цели
		self.points=0 # points - баллов получено за убийство цели
		self.live=1 # атрибут, отвечающий за состояние цели (1 - жива, 0 - мертва)
		self.id=canv.create_oval(0, 0, 0, 0) # привязывает цель к холсту
		self.id_points=canv.create_text(30, 30, text=self.points, font='28')
		self.vx=rnd(-2, 2) # начальная скорость цели по горизонтали
		self.vy=rnd(-2, 2) # начальная скорость цели по вертикали
		self.color=color_new # ввод цвета
		self.new_target() # создаёт новую цель
		self.time=0 # колебание цели (параметр)
		self.hit_the_target=False # есть попадание или нет

	def new_target(self): # инициализация новой цели
		x=self.x=rnd(600, 780) # координата цели по горизонтали
		y=self.y=rnd(300, 550) # координата цели по вертикали
		r=self.r=rnd(2, 50) # радиус цели
		color=self.color # выбор цвета цели
		canv.coords(self.id, x-r, y-r, x+r, y+r) # положение новой цели
		canv.itemconfig(self.id, fill=color) # добавляет цвет новой цели

	def hit(self, points=1): # инициализация попадания в цель
		global total_score # глобальная переменная (общий счёт)
		canv.coords(self.id, -10, -10, -10, -10) # задаёт новые координаты цели при попадании
		total_score+=points # увеличение счёта при попадании
		canv.itemconfig(self.id_points, text=total_score) # меняет общий счёт

	def set_coords(self):
		if not self.is_hitted:
			canv.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

	def move(self): #инициализация шага
		if self.live==1: # если цель жива
			x1, y1, x2, y2=canv.coords(self.id)
			canv.move(self.id, self.vx, self.vy)
			self.x=self.x+self.vx
			self.y=self.y+self.vy
			if x2>=int(canv["width"]):
				self.vx=rnd(3,5)
			if x1<=0:
				self.vx=rnd(4,6)    
			if y2>=int(canv["height"]):
				self.vy=rnd(3,4)
			if y1<=0:
				self.vy=rnd(4,5)
			root.after(24, self.move)

t1=Target(color_new='red')
t2=Target(color_new='cyan')
screen1=canv.create_text(400, 300, text='', font='28')
screen2=canv.create_text(400, 300, text='', font='28')
g=Gun()
bullet_1=0
bullet_2=0
balls=[]
total_score=0

def new_game(event=''): # функция класса события
	global Gun, t1, t2, screen1, screen2, balls, bullet_1, bullet_2
	t1.new_target() # создание двух целей
	t2.new_target()
	bullet_1=0
	bullet_2=0
	balls=[] # список шаров
	canv.bind('<Button-1>', g.fire2_start) # вызывает функцию fire2_start при нажатии на ЛКМ
	canv.bind('<ButtonRelease-1>', g.fire2_end) # вызывает функцию fire2_end при отпускании ЛКМ
	canv.bind('<Motion>', g.targetting) # вызывает функцию targetting при движении ЛКМ

	z=0.03
	t1.live=1
	t2.live=1
	while t1.live or balls or t2.live: # пока цели живы - двигает цели
		t1.move()
		t2.move()
		for b in balls: # двигает шары из списка
			b.move()
			if b.hittest(t1) and t1.live: # если происходит столкновение с живой целью-1 - убивает её
				t1.live=0
				t1.hit() # увеличивает очки на единицу
				if (bullet_1==0): # сравнивает
					canv.itemconfig(screen1, text='Цель-1 погибла сразу. Капец!')
				elif ((bullet_1%10)==1) and (bullet_1!=11):
					canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' + str(bullet_1) + ' выстрел')
				elif ((bullet_1%10)<=4) and ((bullet_1%10)>=2) and ((bullet_1 <= 12) or (bullet_1 >= 14)):
					canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' + str(bullet_1) + ' выстрелa')
				else:
					canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' + str(bullet_1) + ' выстрелов')
				canv.update()
				bullet_1=0
			if b.hittest(t2) and t2.live: # если происходит столкновение с живой целью-2 - убивает её
				t2.live=0
				t2.hit()
				if (bullet_2==0): # сравнивает
					canv.itemconfig(screen2, text='Цель-2 погибла сразу. Капец!')
				elif ((bullet_2%10)==1) and (bullet_2!=11):
					canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' + str(bullet_2) + ' выстрел')
				elif ((bullet_2%10)<= 4) and ((bullet_2%10)>=2) and ((bullet_2<12) or (bullet_2>14)):
					canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' + str(bullet_2) + ' выстрелa')
				else:
					canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' + str(bullet_2) + ' выстрелов')
				canv.update()
				bullet_2=0
		if (t1.live==0): # если цель-1 метрва, запускает создание новой цели
			t1.new_target()
			t1.live=1
		if (t2.live==0): # если цель-2 метрва, запускает создание новой цели
			t2.new_target()
			t2.live=1
		canv.update()
		time.sleep(0.03)
		g.targetting()
		g.power_up()
	canv.itemconfig(screen1, text='')
	canv.itemconfig(screen2, text='')
	canv.delete(Gun)
	if (t1.live==0) and (t2.live==0): # если обе цели мертвы, перезапускает игру
		root.after(100, new_game())

new_game()
root.mainloop()