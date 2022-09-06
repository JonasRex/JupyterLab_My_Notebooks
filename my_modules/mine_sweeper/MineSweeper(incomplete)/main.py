import tkinter as tk
import settings
import utils
from cell import *

root = tk.Tk()
root.configure(bg='black')
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title('Minesweeper game')
root.resizable(False,False)



top_frame = tk.Frame(
 root,
 bg='red',
 width=utils.get_width(100),
 height=utils.get_height(25)
)
top_frame.place(x=0, y=0)


left_frame = tk.Frame( 
    root,
    bg='orange', 
    width=utils.get_width(25), 
    height=utils.get_height(75) 
) 
left_frame.place(x=0,y=utils.get_height(25)) 



center_frame = tk.Frame( 
    root, 
    bg='grey', 
    width=utils.get_width(75), 
    height=utils.get_height(75) 
)
center_frame.place(x=utils.get_width(25),y=utils.get_height(25))


for x in range(33):
    for y in range(20):
        c = Cell()
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x, row=y
        )


root.mainloop() # This runs the window.