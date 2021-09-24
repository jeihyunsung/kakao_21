import requests
import json

class API:
    def __init__(self):
        self.BASE_URL = 'https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
        self.X_AUTH_TOKEN = 'e1a025cff1db630a09cbb197dadcb30d'
        self.AUTH_KEY = None
    
    def start(self, problem=1):
        self.problem = problem
        headers = {'X-Auth-Token': f'{self.X_AUTH_TOKEN}','Content-Type': f'application/json'}
        data = f'{{"problem": {problem} }}' #TODO
        response = requests.post(f'{self.BASE_URL}/start', headers=headers, data=data)
        token = response.json()

        self.AUTH_KEY = token['auth_key']
        self.problem = token['problem']
        self.time = token['time']
        print("Generated AUTH_KEY", self.AUTH_KEY, self.problem, self.time)
        return

    def locations(self):
        headers = {'Authorization': f'{self.AUTH_KEY}','Content-Type': 'application/json'}
        response = requests.get(f'{self.BASE_URL}/locations', headers=headers)
        token = response.json()

        return token

    def trucks(self):
        headers = {
            'Authorization': f'{self.AUTH_KEY}',
            'Content-Type': f'application/json',
        }
        response = requests.get(f'{self.BASE_URL}/trucks', headers=headers)
        token = response.json()

        return token

    def simulate(self, commands='[{ "truck_id": 0, "command": [2, 5, 4, 1, 6] }]'):
        headers = {
            'Authorization': f'{self.AUTH_KEY}',
            'Content-Type': 'application/json',
        }
        
        data = f'{{ "commands": {commands} }}'

        response = requests.put(f'{self.BASE_URL}/simulate', headers=headers, data=data)
        token = response.json()
        return token

    def score(self):
        headers = {
            'Authorization': f'{self.AUTH_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.get(f'{self.BASE_URL}/score', headers=headers)
        token = response.json()

        print(token) #TODO
        return token


if __name__ == "__main__":
    temp_api = API()
    temp_api.start()
    temp_api.locations()
    temp_api.trucks()
    temp_api.simulate()
    temp_api.simulate()
    temp_api.score()



