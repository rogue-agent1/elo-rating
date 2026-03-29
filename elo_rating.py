#!/usr/bin/env python3
"""Elo Rating - Calculate ratings for competitive matchups."""
import sys, math

class EloSystem:
    def __init__(self, k=32, default=1500):
        self.k = k; self.default = default; self.players = {}
    def add(self, name, rating=None):
        self.players[name] = rating or self.default
    def expected(self, ra, rb):
        return 1 / (1 + 10 ** ((rb - ra) / 400))
    def update(self, winner, loser, draw=False):
        ra = self.players.get(winner, self.default)
        rb = self.players.get(loser, self.default)
        ea = self.expected(ra, rb); eb = 1 - ea
        sa = 0.5 if draw else 1.0; sb = 0.5 if draw else 0.0
        self.players[winner] = ra + self.k * (sa - ea)
        self.players[loser] = rb + self.k * (sb - eb)
    def rankings(self):
        return sorted(self.players.items(), key=lambda x: -x[1])

def main():
    elo = EloSystem()
    for p in ["Alice", "Bob", "Charlie", "Diana"]: elo.add(p)
    matches = [("Alice","Bob"),("Charlie","Diana"),("Alice","Charlie"),("Bob","Diana"),("Diana","Alice"),("Charlie","Bob")]
    print("=== Elo Rating System ===\n")
    for w, l in matches:
        elo.update(w, l)
        print(f"  {w} beats {l}: {w}={elo.players[w]:.0f}, {l}={elo.players[l]:.0f}")
    print("\nRankings:")
    for i, (name, rating) in enumerate(elo.rankings(), 1):
        print(f"  {i}. {name}: {rating:.0f}")

if __name__ == "__main__":
    main()
