#!/usr/bin/env python3
"""elo_rating: Elo rating system for competitive rankings."""
import math, sys

class EloSystem:
    def __init__(self, k=32, default_rating=1500):
        self.k = k; self.default = default_rating
        self.ratings = {}
        self.history = {}

    def get_rating(self, player):
        return self.ratings.get(player, self.default)

    def expected(self, ra, rb):
        return 1 / (1 + 10 ** ((rb - ra) / 400))

    def update(self, winner, loser, draw=False):
        ra = self.get_rating(winner)
        rb = self.get_rating(loser)
        ea = self.expected(ra, rb)
        eb = self.expected(rb, ra)
        if draw:
            sa, sb = 0.5, 0.5
        else:
            sa, sb = 1, 0
        new_ra = ra + self.k * (sa - ea)
        new_rb = rb + self.k * (sb - eb)
        self.ratings[winner] = new_ra
        self.ratings[loser] = new_rb
        self.history.setdefault(winner, []).append(new_ra)
        self.history.setdefault(loser, []).append(new_rb)
        return new_ra, new_rb

    def rankings(self):
        return sorted(self.ratings.items(), key=lambda x: -x[1])

    def win_probability(self, a, b):
        return self.expected(self.get_rating(a), self.get_rating(b))

def test():
    elo = EloSystem(k=32)
    ra, rb = elo.update("Alice", "Bob")
    assert ra > 1500  # Winner gains
    assert rb < 1500  # Loser loses
    assert abs((ra - 1500) + (rb - 1500)) < 0.001  # Zero-sum
    # Multiple games
    for _ in range(10):
        elo.update("Alice", "Bob")
    assert elo.get_rating("Alice") > elo.get_rating("Bob")
    # Draw
    elo2 = EloSystem()
    ra2, rb2 = elo2.update("X", "Y", draw=True)
    assert abs(ra2 - rb2) < 0.001  # Equal after draw from same start
    # Rankings
    elo.update("Charlie", "Bob")
    ranks = elo.rankings()
    assert ranks[0][0] == "Alice"  # Alice should be #1
    # Win probability
    prob = elo.win_probability("Alice", "Bob")
    assert prob > 0.5
    # History
    assert len(elo.history["Alice"]) > 0
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: elo_rating.py test")
