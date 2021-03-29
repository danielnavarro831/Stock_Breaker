import random

class Stock:
    def __init__(self):
        self.current_price = 0
        self.previous_price = 0
        self.name = self.randomize_stock_name()

    def change_price(self, volatility):
        self.previous_price = self.current_price
        rando = 0
        if volatility == "High":
            rando = random.randint(1, 1000)
        elif volatility == "Medium":
            rando = random.randint(self.current_price - 100, self.current_price + 100)
        elif volatility == "Low":
            rando = random.randint(self.current_price - 10, self.current_price + 10)
        if rando <= 0:
            rando = 1
        elif rando > 1000:
            rando = 1000
        self.current_price = rando
        return rando

    def randomize_stock_name(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        banned_combos = ["FAG", "NIG", "DIK", "DIC", "DIX", "VAG", "FUC", "FUK", "FUX", 
                         "FOB", "SUK", "SUC", "SUX", "COC", "COK", "COX", "ASS", "AZZ",
                         "POO", "PEE", "KKK"]
        allowed = False
        while allowed == False:
            combo = ""
            a = 3
            while a > 0:
                rando = random.randint(0, len(letters)-1)
                combo += letters[rando]
                a -= 1
            if combo not in banned_combos:
                allowed = True
                return combo

    def reset(self):
        self.current_price = 0
        self.previous_price = 0
        self.name = self.randomize_stock_name()