from random import randint
import numpy as np

def to_str(num): #converts int to 2 places string
        if num < 10:
                str_num = '0'+str(num)
        else:
             str_num = str(num)
        return str_num 


def ActRobot(robot):
     inisig = robot.GetInitialSignal()
     robo_id = int(inisig[0:2])
     base_x = int(inisig[2:4])
     base_y = int(inisig[4:6])
     canvas_size = (robot.GetDimensionX(), robot.GetDimensionY())

     curr_pos = robot.GetPosition() #tuple
     goal = get_goal(robo_id, (base_x,base_y), canvas_size)
     out = move_to(goal, curr_pos)
     
     
     return out

   


def ActBase(base):
 
 x,y = base.GetPosition()
 str_x = to_str(x)
 str_y = to_str(y)
 id = 0
 str_id = to_str(id)
 while base.GetElixir()>500:
         base.create_robot(str_id + str_x + str_y) #id(2)+baselocation(4) eg. robot1 at(19,9) so id = 01199
 #10 defenders, rest attackers
 #id 1-10 defenders >10 attackers

 return

def in_canvas(pos, canvas_size):
        if pos[0]<0 or pos[0]>=canvas_size[0]:
                return False
        if pos[1]<0 or pos[1]>=canvas_size[1]:
                return False
        return True        

def get_goal(id, base_pos, canvas_size):
        if id < 10:
                #Defender
                add_x = randint(-10,10)
                add_y = randint(-10,10)
                x,y = np.array(base_pos) + np.array([add_x, add_y])
        while not in_canvas((x,y), canvas_size):
                 add_x = randint(-10,10)
                 add_y = randint(-10,10)
                 x,y = np.array(base_pos) + np.array({add_x, add_y})
        else:
                x,y = np.array(canvas_size) - np.array(base_pos)
                return (x,y)

def move_to(goal, curr_pos):
         pos=goal
         if (np.array(pos) ==curr_pos).all() :
                return 0
         if pos[0] == curr_pos[0]:
                return 2 - np.sign(curr_pos[1]+pos[1])
         if pos[1] == curr_pos[1]:
                return 3 + np.sign(curr_pos[1]-pos[1])       
         if randint(0,1):
                 return 2 - np.sign(curr_pos[1]-pos[1])
         else:
                 return 3 + np.sign(curr_pos[0]-pos[0])