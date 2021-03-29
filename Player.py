class Player:
    def __init__(self):
        self.cash = 1000
        self.shares = 0
        self.bought_at = {}

    def add_to_bought_at(self, shares, price):
        if price not in self.bought_at:
            self.bought_at[price] = shares
        else:
            self.bought_at[price] += shares

    def get_avg_share_price(self):
        #bought_at[price] = shares
        share_prices = []
        avg = 0
        #for each price
            #append price * number of shares
        for price in self.bought_at.keys():
            for share in range(self.bought_at[price]):
                share_prices.append(price)
        if len(share_prices) > 0:
            avg = int(sum(share_prices) / len(share_prices))
        else:
            avg = 0
        return avg

    def reset(self):
        self.shares = 0
        self.cash = 1000
        self.bought_at = {}




