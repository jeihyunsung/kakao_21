import json
from API import *
from truck import *
import sys

class Truck_Control():
    def __init__(self):
        self.api = API()
        self.api.start()
        self.get_scenario_status()
        self.init_trucks()

    def get_scenario_status(self):
        self.trucks = 5 if self.api.problem == 1 else 10
        self.size = 5 if self.api.problem == 1 else 60

    def get_current_status(self):
        token = self.api.locations()
        self.location_info = parse_location_token(token)

        token = self.api.trucks()
        self.trucks_loc, self.trucks_bikes = parse_trucks_token(token)

        TRUCK.location_token = self.location_info
        TRUCK.trucks_loc = self.trucks_loc
        TRUCK.trucks_bikes = self.trucks_bikes
        

    def init_trucks(self):
        self.truck_list = []
        for truck_id in range(self.trucks):
            self.truck_list.append(TRUCK(truck_id, self.api, self.size))
    
    def simulate(self):
        simulation_run = True
        curr_idx = 0
        while(simulation_run):
            curr_idx += 1

            curr_run = []
            self.get_current_status()
            # self.control_to_zero()
            for truck_id in range(self.trucks):
                # curr_dict = {"truck_id":truck_id, "command":self.truck_list[truck_id].generate_decisions()}
                curr_dict = {"truck_id":truck_id, "command":[0]}
                curr_run.append(curr_dict)
            curr_run_json = json.dumps(curr_run)
            status = self.api.simulate(curr_run_json)
            TRUCK.minute = status['time']
            if status['status'] == 'finished':
                simulation_run = False
                print(status)
            elif curr_idx%10 == 0:
            # else:
                sys.stdout.flush()
                print(curr_idx, status)
                self.print_map()
        self.api.score()
    
    def detect_zero(self):
        zero_list = []
        for i in self.location_info:
            if self.location_info[i] == 0:
                zero_list.append(i)

        return zero_list
    
    def control_to_zero(self):
        zero_list = self.detect_zero()
        avail_list = [i for i in self.trucks_bikes if self.trucks_bikes[i] > 0]
        # print("zero_list", zero_list, avail_list, self.trucks_bikes)
        if len(zero_list) <= len(avail_list):
            for i in range(len(zero_list)):
                TRUCK.zero_role[avail_list[i]] = zero_list[i]
        else:
            for i in range(len(avail_list)):
                TRUCK.zero_role[avail_list[i]] = zero_list[i]
        
        # print("zero", TRUCK.zero_role)

    def print_map(self):
        print_map = [[0]*self.size for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                this_id = col*self.size+(self.size-1-row)
                print_map[row][col] = str(self.location_info[this_id])
        
        truck_map = [['*']*self.size for _ in range(self.size)]
        for i in range(self.trucks):
            row = self.size-1-self.trucks_loc[i]%self.size
            col = self.trucks_loc[i]//self.size
            truck_map[row][col] = str(i)
        
        for row in range(self.size):
            print(print_map[row], truck_map[row], sep=' ')


if __name__ == "__main__":
    main_control = Truck_Control()
    main_control.simulate()



