class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.last=0
        self.brake=0
        self.computer_cars = []
        self.coins_pos = []
        self.coin_x=0
        self.coin_new=[]
        self.coin_new_last=0
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        car_ypos=[0,0,0,0,0,0,0,0,0,0]
        car_id=[0,0,0,0,0,0,0,0,0,0]
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] < 65: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] > 565: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :     #同一道 
                        if y > 0 and y < 300:     #正前方
                            grid.add(2)
                            car_ypos[2]=y
                            car_id[2]=car["id"]
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5)
                                car_ypos[5]=y
                                car_id[5]=car["id"]
                        elif y < 0 and y > -200: #正後方
                            grid.add(8)
                            car_ypos[8]=y
                            car_id[8]=car["id"]
                    if x > -80 and x < -40 :
                        if y > 80 and y < 250: #右前方
                            grid.add(3)
                            car_ypos[3]=y
                            car_id[3]=car["id"]
                        elif y < -80 and y > -200: #右後方
                            grid.add(9)
                            car_ypos[9]=y
                            car_id[9]=car["id"]
                        elif y < 80 and y > -80: #右邊
                            grid.add(6)
                            car_ypos[6]=y
                            car_id[6]=car["id"]
                    if x < 80 and x > 40:
                        if y > 80 and y < 250: #左前方
                            grid.add(1)
                            car_ypos[1]=y
                            car_id[1]=car["id"]
                        elif y < -80 and y > -200: #左後方
                            grid.add(7)
                            car_ypos[7]=y
                            car_id[7]=car["id"]
                        elif y < 80 and y > -80: #左方
                            grid.add(4)
                            car_ypos[4]=y
                            car_id[4]=car["id"]
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            if self.player_no == 0:
                print(grid)
            self.coin_new=[]
            for coin in self.coins_pos:
                #print(coin[0])
                count=0
                if coin[1]<self.car_pos[1]+40:
                    if(coin[0]-self.car_pos[0]<0):
                        self.coin_new.append(coin[0]-self.car_pos[0]+10)
                    else:
                        self.coin_new.append(coin[0]-self.car_pos[0]+10)
            self.coin_new=sorted(self.coin_new, key=abs)
            if(self.player_no==0):
                print("sort")
            for coin in self.coin_new:
                count=0
                if(self.player_no==0):
                    print(coin)
                if(abs(coin)<=15):
                    if(5 in grid) and speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead):
                       #self.last=0
                       if(self.player_no==0):
                            print("break")
                       break
                    else:
                        self.last=0
                        return ["SPEED"]
                elif (coin<-15):
                    if(5 in grid) and speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead):
                       #self.last=0
                       if(self.player_no==0):
                            print("break")
                       break
                    elif(4 in grid) or (1 in grid):
                        continue
                    else:
                        self.last=1
                        self.brake=0
                        #print("left")
                        return ["SPEED", "MOVE_LEFT"]
                elif (coin>15):
                    if(5 in grid) and speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead):
                        #self.last=0
                        if(self.player_no==0):
                            print("break")
                        break
                    elif (6 in grid) or (3 in grid):
                        #print("6 in grid")
                        continue
                    else:
                        self.last=2
                        self.brake=0
                        #print("right")
                        return ["SPEED", "MOVE_RIGHT"]

            if len(grid) == 0:
                return ["SPEED"]
            else:
                if (2 not in grid) or ((1 in grid) and (3 in grid) and (4 in grid) and (6 in grid)): # Check forward 
                    # Back to lane center
                    self.brake=0
                    if self.car_pos[0] > self.lanes[self.car_lane]and (self.last!=2):
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]and (self.last!=1):
                        return ["SPEED", "MOVE_RIGHT"]
                    else :
                        self.last=0
                        return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        '''if (4 not in grid) and (7 not in grid): # turn left 
                            #if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) and (9 not in grid): # turn right
                            #if self.car_vel < speed_ahead:
                            return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]'''
                        if (1 not in grid) and (4 not in grid)and (self.last!=2): # turn left 
                            self.last=1
                            if  speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead)and self.brake==0:
                                self.brake=1
                                return ["BRAKE","MOVE_LEFT"]
                            elif speed_ahead!=0 and car_ypos[5]<(1600/speed_ahead):
                                self.brake=0
                                return ["NONE","MOVE_LEFT"]
                            else:
                                self.brake=0
                                return ["SPEED", "MOVE_LEFT"]
                        elif (3 not in grid) and (6 not in grid) and (self.last!=1): # turn right
                            self.last=2
                            if speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead) and self.brake==0:
                                self.brake=1
                                return ["BRAKE","MOVE_RIGHT"]
                            elif speed_ahead!=0 and car_ypos[5]<(1600/speed_ahead):
                                self.brake=0
                                return ["NONE","MOVE_RIGHT"]
                            else:
                                self.brake=0
                                return ["SPEED", "MOVE_RIGHT"]
                        if (1 in grid) and (4 not in grid) and (car_ypos[1]>car_ypos[5]):
                            '''if (3 in grid) and (6 not in grid) and (car_ypos[3]>car_ypos[1]):
                                return ["SPEED", "MOVE_RIGHT"]
                            else:'''
                            self.last=1
                            if speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead) and self.brake==0:
                                self.brake=1
                                return ["BRAKE","MOVE_LEFT"]
                            elif speed_ahead!=0 and car_ypos[5]<(1600/speed_ahead):
                                self.brake=0
                                return ["NONE","MOVE_LEFT"]
                            else:
                                self.brake=0
                                return ["SPEED", "MOVE_LEFT"]
                        elif (3 in grid) and (6 not in grid) and (car_ypos[3]>car_ypos[5]):
                            self.last=2
                            if speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead) and self.brake==0:
                                self.brake=1
                                return ["BRAKE","MOVE_RIGHT"]
                            elif speed_ahead!=0 and car_ypos[5]<(1600/speed_ahead):
                                self.brake=0
                                return ["NONE","MOVE_RIGHT"]
                            else:
                                self.brake=0
                                return ["SPEED", "MOVE_RIGHT"]
                        elif (1 in grid) and (3 in grid) and (car_ypos[1]<=car_ypos[5])and (car_ypos[3]<=car_ypos[5]):
                            if speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead) and self.brake==0:
                                self.brake=1
                                return ["BRAKE"]
                            else:
                                self.brake=0
                                return ["NONE"]
                        if(4 in grid) and (6 in grid) : 
                            if speed_ahead!=0 and car_ypos[5]<(1500/speed_ahead) and self.brake==0:
                                self.brake=1
                                return ["BRAKE"]
                            else:
                                self.brake=0
                                return ["NONE"]
                    '''if (3 not in grid) and (6 in grid):
                        if(car_id[6]<=4) and (car_id[6]!=0) :'''

                    if (self.car_pos[0] < 60 ):
                        self.brake=0
                        return ["SPEED", "MOVE_RIGHT"]
                    
                    if (1 not in grid) and (4 not in grid) and (7 not in grid) and (self.last!=2): # turn left 
                        self.last=1
                        self.brake=0
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid) and (self.last!=1): # turn right
                        self.last=2
                        self.brake=0
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (self.last!=2): # turn left 
                        self.last=1
                        self.brake=0
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (self.last!=1): # turn right
                        self.last=2
                        self.brake=0
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid) and(car_ypos[1]>=100): # turn left 
                        self.last=1
                        self.brake=0
                        return ["MOVE_LEFT","SPEED"]    
                    if (6 not in grid) and (9 not in grid) and(car_ypos[3]>=100): # turn right
                        self.last=2
                        self.brake=0
                        return ["MOVE_RIGHT","SPEED"]
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
                self.coin_num = car["coin_num"]
        self.computer_cars = scene_info["computer_cars"]
        if scene_info.__contains__("coins"):
            self.coins_pos = scene_info["coins"]
        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
