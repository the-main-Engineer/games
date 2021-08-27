import random
from typing import Text
import pygame
import threading
import sys
#<globals>
global_running=True
internal_msg=False
global_settings=[]
global_map=None
global_player=None
global_envoirement=None
global_colors=None
global_command=[]
window_draw=[]
mesh_stage=[]
window_measures=[
    1200,     #multiplyer x
    900       #  " "      y
]
#</globals>
def map_draw_up(cord_x,cord_y,ctyp,upscale,doors,door):
    global mesh_stage
    for i in range(0,upscale):
        if doors:
            if i!=upscale/2 and cord_y-i>-1:
                mesh_stage[cord_y-i][cord_x]= ctyp
                #print(1,cord_x,cord_y-i)
            else:
                mesh_stage[cord_y - i][cord_x] = door
        else:
            mesh_stage[cord_y - i][cord_x] = ctyp
def map_draw_down(cord_x,cord_y,ctyp,upscale,doors,door):
    global mesh_stage
    for i in range(0,upscale):
        if doors:
            if i!=upscale/2 and cord_y+i>-1:
                mesh_stage[cord_y+i][cord_x]=ctyp
            else:
                mesh_stage[cord_y+i][cord_x]=door
        else:
            mesh_stage[cord_y + i][cord_x] = ctyp
def map_draw_left(cord_x,cord_y,ctyp,upscale,doors,door):
    global mesh_stage
    for i in range(0,upscale):
        if doors:
            if i!=upscale/2 and cord_x-i>-1:
                mesh_stage[cord_y][cord_x-i]=ctyp
                #print(3,cord_x-i, cord_y)
            else:
                mesh_stage[cord_y][cord_x-i]=door
        else:
            mesh_stage[cord_y][cord_x - i] = ctyp
def map_draw_right(cord_x,cord_y,ctyp,upscale,doors,door):
    global mesh_stage
    for i in range(0,upscale):
        if doors:
            if i!=upscale/2 and cord_x+i>-1:
                mesh_stage[cord_y][cord_x+i]=ctyp
            else:
                mesh_stage[cord_y][cord_x+i]=door
        else:
            mesh_stage[cord_y][cord_x + i] = ctyp
def create_map(name="",geometry=[5,5],upscale=6,materials=1,random_doors=True,types="0123"):
    global mesh_stage
    door=materials+1
    materials+=1
    if upscale%2!=0:
        upscale+=1
    symbolic_stage=[]
    for y in range(0,geometry[1]-1):
        temp=[]
        for x in range(0,geometry[0]-1):
            temp+=[[random.choice(types),random.randrange(0,4),random.randrange(1,materials)]] #0 is ang
        symbolic_stage+=[temp]
    #print(symbolic_stage)
    mesh_stage=[]
    mesh_geometry=[geometry[0]*upscale,geometry[1]*upscale]
    for y in range(0,mesh_geometry[1]-1):
        temp=[]
        for x in range(0,mesh_geometry[0]-1):
            temp+=[" "]
        mesh_stage+=[temp]
    for cy, y in enumerate(symbolic_stage):
        for cx,x in enumerate(y):
            ang,styp,ctyp=x[0],x[1],x[2]
            cord_x,cord_y=cx*upscale+upscale-1,cy*upscale+upscale-1
            if styp==0:
                if ang==0:
                    map_draw_right(cord_x,cord_y,ctyp,upscale,random_doors,door)
                elif ang==1:
                    map_draw_left(cord_x,cord_y,ctyp,upscale,random_doors,door)
                elif ang==2:
                    map_draw_up(cord_x,cord_y,ctyp,upscale,random_doors,door)
                else:
                    map_draw_down(cord_x,cord_y,ctyp,upscale,random_doors,door)
            elif styp==1:
                if ang==0:
                    map_draw_right(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_left(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_up(cord_x,cord_y,ctyp,upscale,random_doors,door)
                elif ang==1:
                    map_draw_right(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_left(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_down(cord_x,cord_y,ctyp,upscale,random_doors,door)
                elif ang==2:
                    map_draw_right(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_up(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_down(cord_x,cord_y,ctyp,upscale,random_doors,door)
                else:
                    map_draw_left(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_up(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_down(cord_x,cord_y,ctyp,upscale,random_doors,door)
            elif styp==2:
                map_draw_up(cord_x,cord_y,ctyp,upscale,random_doors,door)
                map_draw_down(cord_x,cord_y,ctyp,upscale,random_doors,door)
                map_draw_right(cord_x,cord_y,ctyp,upscale,random_doors,door)
                map_draw_left(cord_x,cord_y,ctyp,upscale,random_doors,door)
            else:
                if ang==0 or  ang==1:
                    map_draw_up(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_down(cord_x,cord_y,ctyp,upscale,random_doors,door)
                else:
                    map_draw_right(cord_x,cord_y,ctyp,upscale,random_doors,door)
                    map_draw_left(cord_x,cord_y,ctyp,upscale,random_doors,door)
            mesh_stage[cord_y][cord_x]="*"
    #print(mesh_stage)
    return mesh_stage
def material_selector():
    pass
def imsg(text): #use for internal messages of module
    global internal_msg
    if internal_msg:
        print(text)
def msg(text): #use for interaction with player
    print(text)
def pygame_window():  #pygame window
    global global_running, window_draw, window_measures
    imsg("window_module      started")
    pygame.init()
    screen=pygame.display.set_mode(window_measures)
    a=0
    while global_running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                global_running=False
                break
        a+=1
        screen.fill((0,0,0))
        for cy,y in window_draw:
            for cx,x in y:
                pygame.draw.rect(screen, material_selector(), (200, 150, 100, 50))
        pygame.display.update()
        pygame.time.Clock().tick(30)
        imsg(str(a)+str(a))
    imsg("window_module      stoped")
def init_map(path="main.map",returnVal=True):
    global global_map
    with open(path,"r")as mapFile:
        map_raw=mapFile.read().split("\n")
    map_splitted=[]
    for x_pos in map_raw:
        map_splitted+=[x_pos.split(" ")]
    if returnVal:
        return(map_splitted)
    else:
        global_map = map_splitted
def calc_vision():
    global global_running
    imsg("calc_vision_module started")
    #<test>
    #</test>
    imsg("calc_vision_module stoped")
class cmd():
    def add(cmd_id:int,direction:int):
        global global_command
        global_command += [[cmd_id,direction]]
    def get():
        global global_command
        out=global_command[0]
        if len(global_command)>1:
            global_command=global_command[1:len(global_command)]
        return out[0]
def getInt(some:str):
    return(int(some))
def game_selectors():
    pass
def start_game():
    pass
def uinput():
    global global_running
    while global_running:
        uinput=input(str(settings.get(ID=5))+str(settings.get(ID=7))+"> ")
        if uinput=="help" or uinput=="h":
            msg("help:")
            msg("    direction:")
            msg("      8   1   2")
            msg("          /\   ")
            msg("      7 < # > 3")
            msg("          \/   ")
            msg("      6   5   4")
            msg("      ")
            msg("    w /\ ")
            msg("    a < ")
            msg("    s \/ ")
            msg("    d >")
            msg("    move <direction> ")
            msg("    look <direction>")
            msg("    help or h")
            msg("    quit or q")
        elif uinput=="quit" or uinput=="q":
            global_running=False
            break
        elif uinput[0:3]=="move":
            cmd.add(1,getInt(uinput[4:len(uinput)]))
        elif uinput[0:4]=="start":
            if len(uinput>5):
                game_selectors(uinput[5:len(uinput)])
            start_game()
def calc_map():
    global global_running
    imsg("calc_map_module    started")
    #<test>
    #</test>
    imsg("calc_map_module    stoped")
class opt_thread(threading.Thread):
    def __init__(self,id,name):
        threading.Thread.__init__(self)
        self.id=id
        self.name=name
    def run(self):
        if self.name=="display":
            pygame_window()
        elif self.name=="calc_vision":
            calc_vision()
        elif self.name=="calc_map":
            calc_map()
        elif self.name=="uinput":
            uinput()
        elif self.name=="stage":
            manage_stage()
        else:
            imsg("no thread specified")
def game():
    thread_calc_map     = opt_thread(1,"calc_map")
    thread_calc_vision  = opt_thread(2,"calc_vision")
    thread_display      = opt_thread(3,"display")
    thread_uinput       = opt_thread(4,"uinput")
    thread_manage_stage = opt_thread(5,"stage")

    thread_calc_map     .start()
    thread_calc_vision  .start()
    thread_display      .start()
    thread_uinput       .start()
    thread_manage_stage .start()
def manage_stage():
    pass
def savestr(i,spacer="\n"):
    a=type(i)
    if a == int:
        temp=f'int-{i}{spacer}'
    elif a == str:
        temp=f'str-{i}{spacer}'
    elif a == list:
        temp=f'::la{spacer}'
        for p in i:
            #input(f'{p}of{i}')
            temp+=f'{savestr(p)}'
        temp+=f'::le{spacer}'
    elif a == bool:
        temp=f'bool{i}{spacer}'
    imsg(temp)
    return temp
def loadstr(inpt:str):
    out=[]
    in_1=inpt.split("\n")
    in_2=[]
    lst=False
    tmplst=""
    for i in in_1:
        a=i[0:4]
        b=i[4:len(i)]
        temp=""
        print(f'   {a};{b}--')
        if a=="str-":
            temp=str(b)
        elif a=="int-":
            temp=int(b)
        elif a=="::la":
            lst=True
        elif a=="::le":
            temp=loadstr(tmplst)
            tmplst=""
            lst=False
        elif a=="bool":
            temp=bool(b)
        if lst:
            tmplst+=f'{temp}\n'
        else:
            in_2+=[temp]
    return in_2
class settings():
    global global_settings
    def get(ID=0):
        print(ID,len(global_settings))
        return global_settings[ID]
    def load(name="main.conf"):
        global global_settings
        pass
    def save(name="main.conf"):
        global global_settings
        out=""
        for i in global_settings:
            out+=savestr(i)
        with open(name,"w")as f:
            f.write(out)
    def defaults():
        global global_settings
        global_settings=[                                          #id
            False,      #systemfeedback                             0
            "main.map", #current map                                1
            "main.map", #start map
            [],         #userspecific saved setting files
            "player",   #default username                           4
            "",         #current username                           5
            "$",        #default usergreeting                       6
            "$",        #current user greeting                      7
            [           #player settings
                20,     #playerspeed
                20,     #playerhealth
                [],     #inventory ids
                []      #achecvement ids
            ],
            [           #item ids mapped to items and propertys
                [       #speed upgrade
                    1,  #id
                    2,  #multiplyer
                    "speed x2",#name
                    0,  #id of changed player value, if value = list, id = -1
                    []  #only use if player value is list e.g. [1,2] means first list, second value etc.
                ]
            ],
            [

            ]
        ]
def main():
    settings.defaults()
if __name__=="__main__":
    main()
#only for testing
#settings.defaults()
#settings.save()
#game()
#create_map(name="test_test.map")
