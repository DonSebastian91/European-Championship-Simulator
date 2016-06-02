import numpy as np
import pandas as pd

runtimes = 10
df_winner = {'Germany': 0,
                 'Spain': 0,
                 'France': 0,
                 'England': 0,
                 'Belgium': 0,
                 'Portugal': 0,
                 'Italy': 0,
                 'Ukraine': 0,
                 'Croatia': 0,
                 'Turkey': 0,
                 'Austria': 0,
                 'Poland': 0,
                 'Slovakia': 0,
                 'Russia': 0,
                 'Switzerland': 0,
                 'Ireland': 0,
                 'Czechia': 0,
                 'Sweden': 0,
                 'Romania': 0,
                 'Hungary': 0,
                 'Iceland': 0,
                 'Wales': 0,
                 'Albania': 0,
                 'Northern Ireland': 0
                }
# Team Strenght
teams_elo = {'Germany': 2009,
             'Spain': 1983,
             'France': 1948,
             'England': 1941,
             'Belgium': 1905,
             'Portugal': 1889,
             'Italy': 1850,
             'Ukraine': 1805,
             'Croatia': 1795,
             'Turkey': 1795,
             'Austria': 1766,
             'Poland': 1762,
             'Slovakia': 1748,
             'Russia': 1747,
             'Switzerland': 1744,
             'Ireland': 1735,
             'Czechia': 1730,
             'Sweden': 1729,
             'Romania': 1725,
             'Hungary': 1670,
             'Iceland': 1647,
             'Wales': 1638,
             'Albania': 1591,
             'Northern Ireland': 1589
            }

# Average Goals per Game
average_goals = 2.6

# Average Team Strenght
elo_values = list(teams_elo.values())
elo_average = sum(elo_values)/len(elo_values)

# Team Strenght compared to the Average Team Strenght
team_strenght = {key: teams_elo[key] - elo_average for key in teams_elo.keys()}

# Strenght Multiplicator
team_strenght_goals = {key: team_strenght[key] * 0.0045 for key in team_strenght.keys()}

for i in range(runtimes):
    # Groups
    group_a = ['Albania', 'France', 'Romania', 'Switzerland']
    group_b = ['England', 'Russia', 'Slovakia', 'Wales']
    group_c = ['Germany', 'Ukraine', 'Poland', 'Northern Ireland']
    group_d = ['Croatia', 'Spain', 'Czechia', 'Turkey']
    group_e = ['Belgium', 'Ireland', 'Italy', 'Sweden']
    group_f = ['Iceland', 'Portugal', 'Poland', 'Austria']

    # Groups as Data Frame
    df_group_a = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1, 2, 3])
    df_group_b = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1, 2, 3])
    df_group_c = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1, 2, 3])
    df_group_d = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1, 2, 3])
    df_group_e = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1, 2, 3])
    df_group_f = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1, 2, 3])

    # Groups as List
    groups = [group_a, group_b, group_c, group_d, group_e, group_f]
    df_groups = [df_group_a, df_group_b, df_group_c, df_group_d, df_group_e, df_group_f]

    # Groups to Data Frame
    def groups_to_df(group, df_group):
        for i in range(len(group)):
            df_group['Country'][i] = group[i]
            df_group['Points'][i] = 0
            df_group['Goals'][i] = 0
            df_group['Clean Sheet'][i] = 0

    for i in range(len(groups)):
        groups_to_df(groups[i], df_groups[i])

    # Set Index
    df_group_a = df_group_a.set_index('Country')
    df_group_b = df_group_b.set_index('Country')
    df_group_c = df_group_c.set_index('Country')
    df_group_d = df_group_d.set_index('Country')
    df_group_e = df_group_e.set_index('Country')
    df_group_f = df_group_f.set_index('Country')

    # Necessary
    df_groups = [df_group_a, df_group_b, df_group_c, df_group_d, df_group_e, df_group_f]

    def calculate_game(player_1, player_2, df_group):
        goal_difference = team_strenght_goals[player_1] - team_strenght_goals[player_2]
        player_2_goals = (average_goals - goal_difference)/2
        player_1_goals = average_goals - player_2_goals

        # Dice
        player_1_dice = player_1_goals * 6
        player_2_dice = player_2_goals * 6

        # Game Time
        player_1_win = 0
        player_2_win = 0
        for i in range(3):
            goals_player_1 = 0
            goals_player_2 = 0
            for i in range(int(player_1_dice)):
                dice = np.random.randint(1, 6 + 1)
                if dice == 6:
                    goals_player_1 += 1

            for i in range(int(player_2_dice)):
                dice = np.random.randint(1, 6 + 1)
                if dice == 6:
                    goals_player_2 += 1

            df_group.loc[player_1]['Goals'] += goals_player_1
            df_group.loc[player_1]['Clean Sheet'] += goals_player_2
            df_group.loc[player_2]['Goals'] += goals_player_2
            df_group.loc[player_2]['Clean Sheet'] += goals_player_1

            if goals_player_1 >= goals_player_2:
                player_1_win += 1

            if goals_player_1 <= goals_player_2:
                player_2_win += 1

        if player_1_win > player_2_win:
            df_group.loc[player_1]['Points'] += 3
            return player_1

        if player_1_win < player_2_win:
            df_group.loc[player_2]['Points'] += 3
            return player_2

        if player_1_win == player_2_win:
            return player_2

    # Group Phase
    def group_phase(group, df_group):
        calculate_game(group[0], group[1], df_group)
        calculate_game(group[0], group[2], df_group)
        calculate_game(group[0], group[3], df_group)
        calculate_game(group[1], group[2], df_group)
        calculate_game(group[1], group[3], df_group)
        calculate_game(group[2], group[3], df_group)

    for i in range(len(groups)):
        group_phase(groups[i], df_groups[i])

    df_group_a = df_group_a.sort_values('Points')
    df_group_b = df_group_b.sort_values('Points')
    df_group_c = df_group_c.sort_values('Points')
    df_group_d = df_group_d.sort_values('Points')
    df_group_e = df_group_e.sort_values('Points')
    df_group_f = df_group_f.sort_values('Points')
    df_groups = [df_group_a, df_group_b, df_group_c, df_group_d, df_group_e, df_group_f]

    df_achtel_1 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_2 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_3 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_4 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_5 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_6 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_7 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel_8 = pd.DataFrame(columns = ['Country', 'Points', 'Goals', 'Clean Sheet'], index = [0, 1])
    df_achtel = [df_achtel_1, df_achtel_2, df_achtel_3, df_achtel_4, df_achtel_5, df_achtel_6, df_achtel_7, df_achtel_8]

    df_achtel_1['Country'][0] = df_group_a.iloc[3].name
    df_achtel_1['Country'][1] = df_group_c.iloc[2].name
    df_achtel_2['Country'][0] = df_group_a.iloc[3].name
    df_achtel_2['Country'][1] = df_group_c.iloc[2].name
    df_achtel_3['Country'][0] = df_group_a.iloc[3].name
    df_achtel_3['Country'][1] = df_group_c.iloc[2].name
    df_achtel_4['Country'][0] = df_group_a.iloc[3].name
    df_achtel_4['Country'][1] = df_group_c.iloc[2].name
    df_achtel_5['Country'][0] = df_group_a.iloc[3].name
    df_achtel_5['Country'][1] = df_group_c.iloc[2].name
    df_achtel_6['Country'][0] = df_group_a.iloc[3].name
    df_achtel_6['Country'][1] = df_group_c.iloc[2].name
    df_achtel_7['Country'][0] = df_group_a.iloc[3].name
    df_achtel_7['Country'][1] = df_group_c.iloc[2].name
    df_achtel_8['Country'][0] = df_group_a.iloc[3].name
    df_achtel_8['Country'][1] = df_group_c.iloc[2].name

    # New Function -> No Data Frames
    def calculate_game_2(player_1, player_2):
        goal_difference = team_strenght_goals[player_1] - team_strenght_goals[player_2]
        player_2_goals = (average_goals - goal_difference)/2
        player_1_goals = average_goals - player_2_goals

        # Dice
        player_1_dice = player_1_goals * 6
        player_2_dice = player_2_goals * 6

        # Game Time
        player_1_win = 0
        player_2_win = 0
        for i in range(3):
            goals_player_1 = 0
            goals_player_2 = 0
            for i in range(int(player_1_dice)):
                dice = np.random.randint(1, 6 + 1)
                if dice == 6:
                    goals_player_1 += 1

            for i in range(int(player_2_dice)):
                dice = np.random.randint(1, 6 + 1)
                if dice == 6:
                    goals_player_2 += 1

            if goals_player_1 >= goals_player_2:
                player_1_win += 1

            if goals_player_1 <= goals_player_2:
                player_2_win += 1

        if player_1_win > player_2_win:
            return player_1

        if player_1_win < player_2_win:
            return player_2

        if player_1_win == player_2_win:
            return player_2

    # Round of Last 8
    achtel_1 = calculate_game_2(df_group_a.iloc[2].name, df_group_c.iloc[2].name)
    achtel_2 = calculate_game_2(df_group_b.iloc[3].name, df_group_a.iloc[1].name)
    achtel_3 = calculate_game_2(df_group_d.iloc[3].name, df_group_b.iloc[1].name)
    achtel_4 = calculate_game_2(df_group_a.iloc[2].name, df_group_c.iloc[1].name)
    achtel_5 = calculate_game_2(df_group_c.iloc[3].name, df_group_f.iloc[1].name)
    achtel_6 = calculate_game_2(df_group_f.iloc[3].name, df_group_e.iloc[2].name)
    achtel_7 = calculate_game_2(df_group_e.iloc[3].name, df_group_d.iloc[2].name)
    achtel_8 = calculate_game_2(df_group_b.iloc[2].name, df_group_f.iloc[2].name)

    # Quarter Finals
    viertel_1 = calculate_game_2(achtel_1, achtel_3)
    viertel_2 = calculate_game_2(achtel_2, achtel_6)
    viertel_3 = calculate_game_2(achtel_5, achtel_7)
    viertel_4 = calculate_game_2(achtel_4, achtel_8)

    # Semi Finals
    halb_1 = calculate_game_2(viertel_1, viertel_2)
    halb_2 = calculate_game_2(viertel_3, viertel_4)

    # Final
    final = calculate_game_2(halb_1, halb_2)
    df_winner[final] += 1
    
for team in df_winner:
    print('Probability for ' + team + ' : ' + str(((df_winner[team]/runtimes))*100) + '.')
