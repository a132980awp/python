import tkinter
import tkinter.messagebox
import time
import random
from PIL import Image,ImageTk  
import os

def handlerAdaptor(fun, **kwds):
	'''事件处理函数的适配器，相当于中介'''
	return lambda fun=fun,kwds=kwds: fun( **kwds)

def create_food():
	global food_x,food_y,food
	canvas.delete(food)
	temp = []
	for i in range(1,15):
		for j in range(1,15):
			temp.append((i,j))
	for body in data:
		temp.remove((body.x,body.y))
	food_x,food_y = random.choice(temp)
	food = canvas.create_image(food_x*20,food_y*20,image = cardimg[8])
	print("新食物坐标",food_x,food_y)


def time_limit():
	global time_now,toward,point
	if(time.time()-time_now>(1.5/(point/3+1))):
		time_now = time.time()
		snack_x(toward)
	if(start_game == 0):
		return
	root.after(30, time_limit)
	
def snack_x(op):
	print("操作：",op)
	global toward,x,y,food_x,food_y,point
	if(op == 1):
		if(toward == 3):
			return
		else:
			toward = 1
			y = y - 1
	if(op == 3):
		if(toward == 1):
			return
		else:
			toward = 3
			y = y + 1
	if(op == 4):
		if(toward == 2):
			return
		else:
			toward = 4
			x = x - 1
	if(op == 2):		
		if(toward == 4):
			return
		else:
			toward = 2
			x = x + 1
	canvas.itemconfig(draw[-1],image = cardimg[toward+3])
	for body in data:
		if(body.x == x and body.y == y):
			print("dead")
			button_hit(4)
	if(x<=0 or x>=15 or y<=0 or y>=15):
		print("dead")
		button_hit(4)
	data.append(Snack(x,y,toward)) 
	draw.append(canvas.create_image(data[-1].x*20,data[-1].y*20,image = cardimg[toward-1]))
	wall.append((x,y))
	if(not(data[-1].x == food_x and data[-1].y == food_y)):#没吃到食物
		print("当前头部位置",data[-1].x,data[-1].y)
		canvas.delete(draw[0])
		wall.remove((data[0].x,data[0].y))
		del draw[0]
		del data[0]

	else:
		print("eat!")
		point = point + 1
		create_food()
		canvas.itemconfig(text_p,text = "point : "+str(point))
	root.update()
	#dx = 1
def snack_move(event):
	global start_game
	print(event.keysym)
	global time_now
	time_now = time.time()
	global toward,x,y
	if(event.keysym == "Up"):
		snack_x(1)
	if(event.keysym == "Down"):
		snack_x(3)
	if(event.keysym == "Left"):
		snack_x(4)
	if(event.keysym == "Right"):		
		snack_x(2)
	if(event.keysym == "space"):
		start_game=(start_game+1)%2
		if(start_game == 1):
			time_limit()

def snack_csh():
	global x,y,toward,draw,data,point
	for im in draw:
		canvas.delete(im)
	del draw[:]
	del wall[:]
	del data[:]
	x,y = 8,3
	toward = 2
	point = 0
	for i in range(5):
		data.append(Snack(i+3,3,2))
		draw.append(canvas.create_image(data[i].x*20,data[i].y*20,image = cardimg[5]))
		wall.append((i+3,3))
	data.append(Snack(5+3,3,2))
	draw.append(canvas.create_image(data[5].x*20,data[i].y*20,image = cardimg[1]))
	wall.append((5+3,3))
	for i in range(16):
		wall.append((i,0))
		wall.append((0,i))
		wall.append((15,i))
		wall.append((i,15))
	create_food()


#事件
def button_hit(id):
	global start_game
	print(id)
	if(id == 0):
		for i in range(3):
			buttons[i].pack_forget()
		snack_csh()
		canvas.place(x=0, y=0, relwidth=1, relheight=1)
		start_game = 1
		root.after(1000, time_limit)#定时器启动！！

	if(id == 1):
		print("nothing")
	if(id == 2):
		if(tkinter.messagebox.askokcancel('关闭', '是否关闭程序？')):
			root.quit()
			root.destroy()
	if(id == 4):
		print(wall)
		for body in data:
			print(body.x,body.y)
		for i in range(3):
			buttons[i].pack(side='top',pady = '10px')
		canvas.place_forget()
		start_game = 0

#创建控件
root = tkinter.Tk()
root.title('Snack!')
root.geometry('400x300')
root.resizable(0,0)

buttons = []
temp = 0
time_now = 0
food_x = 0
food_y = 0

for button in ['开始游戏','速度设置','退出游戏']:
	buttons.append(tkinter.Button(root,text=button,height = 3,width = 20,command = handlerAdaptor(button_hit, id = temp)))
	temp = temp + 1

canvas = tkinter.Canvas(root,
	width = 200,      # 指定Canvas组件的宽度  
	height = 150,      # 指定Canvas组件的高度  
	bg = 'white')      # 指定Canvas组件的背景色  
	
canvas.create_line((3,3),(3,297),fill='black',width=3)
canvas.create_line((3,3),(297,3),fill='black',width=3)
canvas.create_line((3,297),(297,297),fill='black',width=3)
canvas.create_line((297,3),(297,297),fill='black',width=3)

button_return = tkinter.Button(canvas,text="返回菜单",height = 2,width = 12,command = handlerAdaptor(button_hit, id = 4))
point = 0
text_p = canvas.create_text((350,100),text = "point : "+str(point),fill = "black",font =('Arial', 12))
text_info = canvas.create_text((350,150),text = "按空格暂停",fill = "black",font =('Arial', 11))

#canvas.create_line((10,10),(10,20),fill='black',width=10)
#绑定控件以及事件
for i in range(3):
	buttons[i].pack(side='top',pady = '10px')
button_return.pack(anchor = 'se',padx = '3px',pady = '3px')
canvas.bind_all("<KeyPress>",snack_move)

#加载图片
card = []
cardimg = []
for i in range(9):
	card.append(Image.open(os.path.abspath(os.path.dirname(__file__))+'/src/'+str(i+1)+'.jpg'))
	cardimg.append(ImageTk.PhotoImage(card[i]))

#snack 相关数据或控件
class Snack():
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z	#取值 1 - 8 上 - 左上 顺时针
		
data = []
draw = []
wall = []
food = 0

toward = 2 #↑ → ↓ ←
start_game = 0# 1表示游戏状态中
x,y = 8,3
#canvas.place(x=0, y=0, relwidth=1, relheight=1)
root.mainloop()