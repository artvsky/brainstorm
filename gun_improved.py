from random import randrange as rnd, choice
import tkinter as tk
import math
import time

print (dir(math))

root=tk.Tk()
fr=tk.Frame(root)
root.geometry('800x600')
canv=tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

class ball():
	def __init__(self, x=40, y=450):
		"""
		Конструктор класса ball
		Args:
		x - начальное положение мяча по горизонтали
		y - начальное положение мяча по вертикали
		"""
		self.x=x
		self.y=y
		self.r=10
		self.vx=0
		self.vy=0
		self.color=choice(['blue', 'green', 'red', 'brown'])
		self.id=canv.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color)
		self.live=30

	def set_coords(self):
		canv.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

	def move(self):
		"""
		Переместить мяч по прошествии единицы времени.
		Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
		self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
		и стен по краям окна (размер окна 800х600).
		"""
		if self.y<=550:
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
		if self.x>780:
			self.vx=-self.vx*0.8
			self.x=779

	def hittest(self, obj):
		"""
		Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
		Args:
		obj: Обьект, с которым проверяется столкновение.
		Returns: Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
		"""
		if ((obj.x-self.x)**2+(obj.y-self.y)**2)<=((obj.r+self.r)**2):
			return True
		else:
			return False

class gun():
	def __init__(self):
		self.f2_power=10
		self.f2_on=0
		self.an=1
		self.id=canv.create_line(20, 450, 50, 420, width=7)

	def fire2_start(self, event):
		self.f2_on=1

	def fire2_end(self, event):
		"""
		Выстрел мячом.
		Происходит при отпускании кнопки мыши.
		Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
		"""
		global balls, bullet
		bullet+=1
		new_ball=ball()
		new_ball.r+=5
		self.an=math.atan((event.y-new_ball.y)/(event.x-new_ball.x))
		new_ball.vx=self.f2_power*math.cos(self.an)
		new_ball.vy=-self.f2_power*math.sin(self.an)
		balls+=[new_ball]
		self.f2_on=0
		self.f2_power=10

	def targetting(self, event=0):
		"""Прицеливание. Зависит от положения мыши."""
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

class target():
	def __init__(self, color_new): #инициализация цели
		self.points=0 #points - баллов получено за цель
		self.live=1
		self.id=canv.create_oval(0, 0, 0, 0)
		self.id_points=canv.create_text(30, 30, text=self.points, font='28')
		self.vx=rnd(-2, 2) #начальная скорость мяча по горизонтали
		self.vy=rnd(-2, 2) #начальная скорость мяча по вертикали
		self.color=color_new #ввод цвета
		self.new_target() #создаёт новую цель
		self.time=0 #колебание цели (параметр)
		self.hit_the_target=False #есть попадание или нет

	def new_target(self): #инициализация новой цели
		x=self.x=rnd(600, 780) #координата цели по горизонтали
		y=self.y=rnd(300, 550) #координата цели по вертикали
		r=self.r=rnd(2, 50) #радиус цели
		color=self.color='red'
		canv.coords(self.id, x-r, y-r, x+r, y+r)
		canv.itemconfig(self.id, fill=color)

	def hit(self, points=1): #инициализация попадания в цель
		global total_score #глобальная переменная (общий счёт)
		canv.coords(self.id, -10, -10, -10, -10)
		total_score+=points #увеличение счёта при попадании
		canv.itemconfig(self.id_points, text=total_score)
	def move(self): #инициализация шага
		if self.live==1:
			x1, y1, x2, y2=canv.coords(self.id)
			canv.move(self.id, self.vx, self.vy)
			self.x=self.x+self.vx
			self.y=self.y+self.vy
			if x2>=int(canv["width"]):
				self.vx=rnd(1,2)*-1
			if x1<=0:
				self.vx=rnd(2,3)    
			if y2>=int(canv["height"]):
				self.vy=rnd(3,4)*-1
			if y1<=0:
				self.vy=rnd(4,5)
			root.after(24, self.move)

t1=target(color_new='red')
t2=target(color_new='green')
screen1=canv.create_text(400, 300, text='', font='28')
g1=gun()
bullet=0
balls=[]
total_score=0

def new_game(event=''):
	global gun, t1, t2, screen1, screen2, balls, bullet_1, bullet_2
	t1.new_target() # создание двух целей
	t2.new_target()
	bullet_1=0
	bullet_2=0
	balls=[]
	canv.bind('<Button-1>', g1.fire2_start)
	canv.bind('<ButtonRelease-1>', g1.fire2_end)
	canv.bind('<Motion>', g1.targetting)

	z=0.03
	t1.live=1
	t2.live=1
	while t1.live or balls or t2.live:
		t1.move()
		t2.move()
		for b in balls:
			b.move()
			if b.hittest(t1) and t1.live:
				t1.live=0
				t1.hit()
				if (bullet_1==0):
					canv.itemconfig(screen1, text='Цель-1 погибла сразу. Капец!')
				elif ((bullet_1%10)==1) and (bullet_1!=11):
					canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' + str(bullet_1) + ' выстрел')
				elif ((bullet_1%10)<=4) and ((bullet_1%10)>=2) and ((bullet_1 <= 12) or (bullet_1 >= 14)):
					canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' + str(bullet_1) + ' выстрелa')
				else:
					canv.itemconfig(screen1, text='Вы уничтожили цель-1 за ' + str(bullet_1) + ' выстрелов')
				canv.update()
				bullet_1=0
			if b.hittest(t2) and t2.live:
				t2.live=0
				t2.hit()
				if (bullet_2==0):
					canv.itemconfig(screen2, text='Цель-2 погибла сразу. Капец!')
				elif ((bullet_2%10)==1) and (bullet_2!=11):
					canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' + str(bullet_2) + ' выстрел')
				elif ((bullet_2%10)<= 4) and ((bullet_2%10)>=2) and ((bullet_2<12) or (bullet_2>14)):
					canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' + str(bullet_2) + ' выстрелa')
				else:
					canv.itemconfig(screen2, text='Вы уничтожили цель-2 за ' + str(bullet_2) + ' выстрелов')
				canv.update()
				bullet_2=0
		if (t1.live==0):
			t1.new_target()
			t1.live=1
		if (t2.live==0):
			t2.new_target()
			t2.live=1
		canv.update()
		time.sleep(0.03)
		g1.targetting()
		g1.power_up()
	canv.itemconfig(screen1, text='')
	canv.itemconfig(screen2, text='')
	canv.delete(gun)
	if (t1.live==0) and (t2.live==0):
		root.after(100, new_game())

new_game()
root.mainloop()