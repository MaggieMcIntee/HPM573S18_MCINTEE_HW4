from enum import Enum  # to access the class already implemented in python
import numpy as np  # this is to get access to the numpy package for random number generator


class CoinFlip(Enum):
    """
    Outcome of the game, win or lose
    """
    HEAD = 1
    TAIL = 0


class Game:
    def __init__(self, id):
        self._id = id
        self._rnd = np.random  # random number generator for this coin
        self._rnd.seed(id)  # specifying the seed of random number generator for this coin
        self._coinFlip = CoinFlip.HEAD  # assuming you start out the game not winning
        self._countTails = 0
        self._countWin = 0
        self._totalFlips = 20
        self._flipNumber = 1

    def nextFlip(self):
        if self._coinFlip == CoinFlip.HEAD:
            if self._rnd.sample() > 0.6:
                self._coinFlip = CoinFlip.HEAD
            elif self._rnd.sample() < 0.6:
                self._coinFlip = CoinFlip.TAIL
                self._countTails = 1
        elif self._coinFlip == CoinFlip.TAIL:
            if self._rnd.sample() < 0.6:
                self._coinFlip = CoinFlip.TAIL
                self._countTails += 1
            if self._rnd.sample() > 0.6:
                self._coinFlip = CoinFlip.HEAD
                if self._countTails >= 2:
                   self._countWin += 1
                self._countTails = 0

        self._flipNumber += 1

    def play(self):
        for i in range(1, self._totalFlips+1):
            self._rnd = np.random
            self._seed = (self._id * self._flipNumber)
            self.nextFlip()

    def get_reward(self):
        self.play()
        self._reward = -250 + self._countWin*100
        return self._reward


class Cohort:
    def __init__(self, id, num_realization):  # id is the id of the cohort
        #self.id = id
       # self._num_realization = num_realization
        self._players = []  # number of trials
        n = 1  # counter

        while n <= num_realization:
            player = Game(id=id*num_realization +n)
            self._players.append(player)
            n += 1

    def simulate(self):
        gameReward = []
        for player in self._players:
            gameReward.append(player.get_reward())
        return sum(gameReward) / len(gameReward)


NUM_REALIZATION = 1000

# create a cohort
Trial = Cohort(id=1, num_realization=NUM_REALIZATION)
print(Trial.simulate())
