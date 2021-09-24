from lib import *
import json

class TRUCK():

    location_token = None
    trucks_loc = None
    trucks_bikes = None
    zero_role = {}
    minute = 0

    with open('past_record_half.json', 'r') as f:
        past_record = json.load(f)

    def __init__(self, id, api, size):
        self.location = 0
        self.api = api
        self.id = id
        self.size = size
        self.bikes = 0

    def get_around_loc(self, curr_loc):
        if curr_loc != None:
            up = curr_loc+1 if curr_loc%self.size != self.size-1 else None
            down = curr_loc-1 if curr_loc%self.size != 0 else None
            right = curr_loc+self.size if curr_loc//self.size != self.size-1 else None 
            left = curr_loc-self.size if curr_loc//self.size != 0 else None

            upr = curr_loc+self.size+1 if curr_loc//self.size != self.size-1 and curr_loc%self.size != self.size-1 else None 
            upl = curr_loc-self.size+1 if curr_loc//self.size != 0 and curr_loc%self.size != self.size-1 else None
            dor = curr_loc+self.size-1 if curr_loc//self.size != self.size-1 and curr_loc%self.size != 0 else None
            dol = curr_loc-self.size-1 if curr_loc//self.size != 0 and curr_loc%self.size != 0 else None
            move_list = [up, down, right, left, upr, upl, dor, dol]
        else:
            move_list = []
        return move_list

    def compare_around(self):

        move_list = self.get_around_loc(self.location)

        # Check the higher id is exist in move_list
        other_truck_loc = list(TRUCK.trucks_loc.values())[:self.id]
        for idx, x in enumerate(move_list):
            next_move_list = self.get_around_loc(x)
            for y in next_move_list:
                if y in other_truck_loc:
                    move_list[idx] = None
                    break
        
        half_minute = (TRUCK.minute//30)*30
        bikes = {}

        bikes[self.location] = TRUCK.location_token[self.location]*(1-TRUCK.past_record[str(half_minute)][str(self.location)])
        for x in move_list:
            if x != None:
                bikes[x] = TRUCK.location_token[x]*(1-TRUCK.past_record[str(half_minute)][str(x)])

        average = sum(bikes.values())/len(bikes.keys())
        bike_max = max(bikes.keys(), key=(lambda x:bikes[x]))
        bike_min = min(bikes.keys(), key=(lambda x:bikes[x]))

        return bike_max, bike_min

    def get_order(self, next_loc, need_bike):
        '''
        0: 6초간 아무것도 하지 않음
        1: 위로 한 칸 이동
        2: 오른쪽으로 한 칸 이동
        3: 아래로 한 칸 이동
        4: 왼쪽으로 한 칸 이동
        5: 자전거 상차
        6: 자전거 하차
        '''

        diff = next_loc - self.location
        decisions = []
        if diff == 0:
            decisions.append(0)
        elif 1 <= diff <= 2:
            for _ in range(diff):
                decisions.append(1)
        elif -2 <= diff <= -1:
            for _ in range(-diff):
                decisions.append(3)
        elif 4 <= diff <= 6:
            decisions.append(2)
            if diff == 4:
                decisions.append(3)
            elif diff == 6:
                decisions.append(1)
        elif -6 <= diff <= -4:
            decisions.append(4)
            if diff == -6:
                decisions.append(3)
            elif diff == -4:
                decisions.append(1)

        if need_bike > 0:
            if TRUCK.location_token[next_loc] < 2:
                for _ in range(2-TRUCK.location_token[next_loc]):
                    decisions.append(6)
            else:
                decisions.append(6)
        elif need_bike < 0:
            if self.location_token[next_loc] > 3:
                for _ in range(TRUCK.location_token[next_loc]-3):
                    decisions.append(5)
            else:
                decisions.append(5)
            
        return decisions

    def generate_decisions(self):

        self.get_current_status()
        decisions = []

        if self.location == 0 and self.id != 0:
            for i in range(self.id):
                decisions.append(2)
            return decisions

        # else:    
        max_loc, min_loc = self.compare_around()        

        decisions += self.get_order(max_loc, -1)
        self.location = max_loc

        if self.id in TRUCK.zero_role and TRUCK.location_token[min_loc] != 0:
            next_loc = TRUCK.zero_role[self.id]
            decisions += self.calcurate_move(next_loc)
            for _ in range(2):
                decisions.append(6)
        else:
            decisions += self.get_order(min_loc, 1)
            self.location = min_loc

        if len(decisions) > 10:
            decisions = decisions[:10]

        return decisions

    def calcurate_move(self, next_loc):

        decisions = []
        nrow = self.size-1-next_loc%self.size
        ncol = next_loc//self.size

        crow = self.size-1-self.location%self.size
        ccol = self.location//self.size

        if nrow-crow > 0:
            for _ in range(nrow-crow):
                decisions.append(1)
        elif nrow-crow < 0:
            for _ in range(crow-nrow):
                decisions.append(3)

        if ncol-ccol > 0:
            for _ in range(ncol-ccol):
                decisions.append(2)
        elif ncol-ccol < 0:
            for _ in range(ccol-ncol):
                decisions.append(4)

        return decisions

    def get_current_status(self):
        self.location = TRUCK.trucks_loc[self.id]
        self.bikes = TRUCK.trucks_bikes[self.id]


    
