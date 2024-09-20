import json


def get_data(file):
    with open(file, 'r') as file_pointer:
        data = json.load(file_pointer)
        return data


def save_data(data, file):
    with open(f'{file}', 'w') as file_pointer:
        json.dump(data, file_pointer)


def add_sport(file):
    sport_name = input("enter sport name: ")
    data = get_data(file)
    if sport_name not in data['games']:
        data['games'].append(sport_name)
        participants = data['participants']
        if participants:
            for team in participants.keys():
                if sport_name not in participants[team].keys():
                    participants[team][sport_name] = 0
        data['participants'] = participants
        save_data(data, file)
    else:
        print('sport already exists')


def add_team(file):
    team_name = input("enter team name->")
    data = get_data(file)
    games = data['games']
    participants = data['participants']
    if team_name not in participants.keys():
        team_games = {}
        for games in games:
            team_games[games] = 0
        data['participants'][team_name] = team_games
    else:
        print("Team already exist")
    save_data(data, 'sport_data.json')


def add_point(file):
    data = get_data(file)
    participants = data['participants']
    team = input("enter team name->")
    if team in participants.keys():
        sport = input('enter sport name->')
        if sport in participants[team].keys():
            try:
                point = int(input("enter point->"))
                participants[team][sport] += point
                data['participants'] = participants
                save_data(data, file)
            except ValueError as v:
                print('not a valid score')
        else:
            print(f'{team} has participated in this sport')
    else:
        print('team not found')


def get_total(file):
    team = input("enter team name: ")
    data = get_data(file)
    participants = data['participants']
    if team not in participants.keys():
        print('Team not exist')
    else:
        print(f'{team} has scored->{sum(participants[team].values())}')


def menu():
    user_options = """
1.Add sport
2.Add team
3.Add score
4.Get total score
5.exit    
"""
    print(user_options)
    option = input("enter your choice ")
    if option == '1':
        add_sport('sport_data.json')
    elif option == '2':
        add_team('sport_data.json')
    elif option == '3':
        add_point('sport_data.json')
    elif option == '4':
        get_total('sport_data.json')
    elif option == '5':
        exit()
    menu()


menu()
