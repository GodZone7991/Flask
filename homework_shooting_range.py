import random
import pandas as pd


class Gun:
    shot_sound = 'BAM'

    def __init__(self, mag_size=0):
        self.mag_size = mag_size
        self.q_bullet = mag_size

    def shot(self):
        if self.q_bullet == 0:
            self.reload()
        else:
            self.q_bullet -= 1

    def reload(self):
        self.q_bullet = self.mag_size


class Shotgun(Gun):
    type = "shotgun"
    accuracy = 0.20

    def __init__(self, mag_size=10):
        super().__init__(mag_size)


class Pistol(Gun):
    type = "pistol"
    accuracy = 0.60

    def __init__(self, mag_size=10):
        super().__init__(mag_size)


class Bow(Gun):
    type = "bow"
    accuracy = 0.90
    shot_sound = 'Whoosh'

    def __init__(self, mag_size=10):
        super().__init__(mag_size)


class Target:
    score = 0
    sections = range(0, 11)

    def hit(self):
        score = random.choice(self.sections)
        return score


class Player:
    score_bow = 0
    score_pistol = 0
    score_shotgun = 0

    def __init__(self, name):
        self.name = name

    def hit(self, gun, target):
        wpn_type = gun.type
        score_str = 'score_{}'.format(wpn_type)

        for i in range(gun.mag_size):
            gun.shot()
            self.__setattr__(score_str, self.__getattribute__(score_str) + target.hit())

        print(wpn_type, self.__getattribute__(score_str))


def competition():
    names = ['Jill', 'Tommy', 'Harry', 'Tomm', 'Susan', 'Mark', 'Timothy', 'Tamara', 'Pavel', 'Jared']
    l_players = []
    dictionary = {}
    for i in names:
        player = Player(i)
        l_players.append(player)
    weapon_list = (Bow(), Pistol(), Shotgun())
    target = Target()
    for player in l_players:
        dictionary.update({player.name: [0, 0, 0]})
        for i, gun in enumerate(weapon_list):
            player.hit(gun, target)
            dictionary[player.name][i] += player.__getattribute__('score_' + gun.type)
    return dictionary


def display_winner(data):
    df = pd.DataFrame(data)
    df_n = df.rename(index={0: "bow", 1: "pistol", 2: "shotgun"})
    df_t = df_n.T
    df_t["sum"] = df_t.sum(axis=1)


    sort_by_sum = df_t.sort_values(by='sum', ascending=False)
    sort_bow = df_t.sort_values(by="bow", ascending=False)
    sort_pistol = df_t.sort_values(by="pistol", ascending=False)
    sort_shotgun = df_t.sort_values(by="shotgun", ascending=False)

    winner_bow = sort_bow[["bow"]].idxmax().values[0]
    winner_pistol = sort_pistol[["pistol"]].idxmax().values[0]
    winner_shotgun = sort_shotgun[["shotgun"]].idxmax().values[0]
    winner_sum = sort_by_sum[['sum']].idxmax().values[0]

    winner_list = [winner_sum, winner_bow,winner_pistol,winner_shotgun,]


    winner_list_f = []
    for i, table in enumerate([sort_by_sum,sort_bow,sort_pistol,sort_shotgun]):

        winner_list_f.append(table.rename(index={winner_list[i]: winner_list[i] + "is a winner"}))



    return winner_list_f


if __name__ == "__main__":
    display_winner(competition())
