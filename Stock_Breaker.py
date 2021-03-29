from tkinter import *
from Player import *
from Stock import *
import random

class Game:
    def __init__(self):
        self.version = "1.01"
        self.app = Tk()
        self.app.title("Stock Breaker")
        self.app.resizable(False, False)
        #self.app.iconbitmap("./nine_lives_32.ico")
        self.game_over = False
        self.volatility = "High"
        self.high_scores = {}
        self.player = Player()
        self.stock = Stock()
        self.stock_name_label = Label(self.app, text=self.stock.name)
        self.stock_price_label = Entry(self.app, width=20, justify="center")
        self.shares_label = Label(self.app, text="Shares: 0")
        self.cash_display = Label(self.app, text="Cash: $" + str(self.stock.current_price))
        self.avg_share_price_label = Label(self.app, text="Avg cost per share: $" + str(self.player.get_avg_share_price()))
        self.stock_graph = Text(self.app, height=10, width=32, state="disabled")
        self.news_feed = Entry(self.app, width=43, state="disabled")
        self.news_feed_text = ""
        self.buy_button = Button(self.app, text="Buy", pady=10, padx=55, command=lambda: self.buy_stock(self.get_max_buy()))
        self.sell_button = Button(self.app, text="Sell", pady=10, padx=53, command=lambda: self.sell_stock(self.player.shares))
        self.play_again_button = Button(self.app, text="Play Again", pady=10, padx=104, command=self.reset_game)
        self.version_label = Label(self.app, text="Ver: " + self.version + " ", bd=1, relief=SUNKEN, anchor=E)
        #Menus
        self.menu = Menu(self.app)
        self.app.config(menu=self.menu)
        #File
        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label="Reset Game", command=self.menu_reset)
        self.file_menu.add_command(label="Exit", command=self.app.quit)
        #Volatility
        self.volatility_menu = Menu(self.menu)
        self.volatility_menu.add_command(label="Low", command=lambda: self.set_volatility("Low"))
        self.volatility_menu.add_command(label="Medium", command=lambda: self.set_volatility("Medium"))
        self.volatility_menu.add_command(label="* High", command=lambda: self.set_volatility("High"))

        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Volatility", menu=self.volatility_menu)
        self.row1=""
        self.row2=""
        self.row3=""
        self.row4=""
        self.row5=""
        self.row6=""
        self.row7=""
        self.row8=""
        self.row9=""
        self.row10=""
        self.quarter = "Q1"
        self.quarter_time = 30000
        self.default_time = 30000
        self.quarter_label = Label(self.app, text=self.quarter)
        self.quarter_timer_label = Label(self.app, text="")
        self.stock_name_label.grid(row=0, column=0, columnspan=2)
        self.stock_price_label.grid(row=1, column=0, columnspan=2)
        self.quarter_label.grid(row=2, column=0)
        self.quarter_timer_label.grid(row=2, column=1)
        self.stock_graph.grid(row=3, column=0, columnspan=2)
        self.news_feed.grid(row=4, column=0, columnspan=2)
        self.cash_display.grid(row=5, column=0)
        self.shares_label.grid(row=5, column=1)
        self.avg_share_price_label.grid(row=6, column=0, columnspan=2)
        self.buy_button.grid(row=7, column=0)
        self.sell_button.grid(row=7, column=1)
        self.version_label.grid(row=8, column=0, columnspan=2, sticky=W+E)
        self.update_stock_price()
        self.update_cash_display()
        self.update_news_reel()
        self.update_quarter_timer()
        self.app.mainloop()

    def set_volatility(self, setting):
        self.volatility = setting
        #Set display in menu
        vol_dict = {"Low": 1, "Medium": 2, "High": 3}
        vol_str = {1: "Low", 2: "Medium", 3: "High"}
        for a in range(1, 4):
            if a == vol_dict[setting]:
                self.volatility_menu.entryconfig(a, label="* " + vol_str[a])
            else:
                self.volatility_menu.entryconfig(a, label=vol_str[a])
        self.game_over = True
        self.stock_graph.delete(1.0, END)
        self.stock_graph.insert(1.0, "Restarting...")
        self.app.after(5000, self.reset_game)

    def menu_reset(self):
        self.game_over = True
        self.stock_graph["state"] = "normal"
        self.stock_graph.delete(1.0, END)
        self.stock_graph.insert(1.0, "Restarting...")
        self.stock_graph["state"] = "disabled"
        self.app.after(5000, self.reset_game)

    def reset_game(self):
        #Reset game vars
        self.game_over = False
        self.quarter = "Q1"
        self.quarter_time = self.default_time
        self.buy_button.grid(row=7, column=0)
        self.sell_button.grid(row=7, column=1)
        self.play_again_button.grid_remove()
        self.row1 = ""
        self.row2 = ""
        self.row3 = ""
        self.row4 = ""
        self.row5 = ""
        self.row6 = ""
        self.row7 = ""
        self.row8 = ""
        self.row9 = ""
        self.row10 = ""
        #Clear stock graph
        self.stock_graph.delete(1.0, END)
        #Clear news feed
        self.news_feed_text = ""
        #Reset stock and player
        self.player.reset()
        self.stock.reset()
        #Reset all labels
        self.stock_name_label["text"] = self.stock.name
        self.quarter_label["text"] = self.quarter
        self.update_shares_count()
        self.update_stock_price()
        self.update_cash_display()
        self.update_news_reel()
        self.update_avg_price()
        self.update_quarter_timer()

    def update_stock_price(self):
        if self.game_over == False:
            new_cost = self.stock.change_price(self.volatility)
            self.add_to_news_feed()
            self.draw_graph()
            rando = random.randint(1, 5)
            rando *= 1000
            self.app.after(rando, self.update_stock_price)
        else:
            self.display_epilogue()

    def display_epilogue(self):
        if self.game_over == True:
            self.add_to_news_feed()
            self.app.after(1000, self.display_epilogue)

    def draw_graph(self):
        amnt = int(self.stock.current_price/100)
        if amnt < 1:
            amnt = 1
        prev_amnt = int(self.stock.previous_price / 100)
        if prev_amnt < 1:
            prev_amnt = 1
        for a in range(1, 11):
            if a != amnt:
                if a > prev_amnt and a < amnt:
                    self.update_row(a, "|")
                elif a < prev_amnt and a > amnt:
                    self.update_row(a, "|")
                else:
                    self.update_row(a, " ")
            else:
                self.update_row(a, "|")
        lines = {1:self.row1, 2:self.row2, 3:self.row3, 4:self.row4, 5:self.row5,
            6:self.row6, 7:self.row7, 8:self.row8, 9:self.row9, 10:self.row10}
        rows=10
        self.stock_graph["state"] = "normal"
        for b in range(1, 11):
            self.stock_graph.insert(float(b), lines[rows][-32:] + "\n")
            rows -= 1
        self.stock_graph["state"] = "disabled"
        self.update_stock_price_label()

    def update_row(self, row, str):
        if row == 1:
            self.row1 += str
        elif row == 2:
            self.row2 += str
        elif row == 3:
            self.row3 += str
        elif row == 4:
            self.row4 += str
        elif row == 5:
            self.row5 += str
        elif row == 6:
            self.row6 += str
        elif row == 7:
            self.row7 += str
        elif row == 8:
            self.row8 += str
        elif row == 9:
            self.row9 += str
        elif row == 10:
            self.row10 += str

    def update_shares_count(self):
        self.shares_label["text"] = "Shares: " + str(self.player.shares)

    def update_stock_price_label(self):
        self.stock_price_label.delete(0, END)
        self.stock_price_label.insert(0, "$" + str(self.stock.current_price))

    def update_cash_display(self):
        self.cash_display["text"] = "Cash: $" + str(self.player.cash)

    def update_avg_price(self):
        self.avg_share_price_label["text"] = "Avg. cost per share: $" + str(self.player.get_avg_share_price())

    def update_quarter_timer(self):
        self.quarter_time -= 1000
        nums = str(int(self.quarter_time / 1000))
        if len(nums) == 1:
            nums = "0" + nums
        self.quarter_timer_label["text"] = ":" + nums
        if self.quarter_time == 0:
            if self.quarter == "Q1":
                self.quarter = "Q2"
            elif self.quarter == "Q2":
                self.quarter = "Q3"
            elif self.quarter == "Q3":
                self.quarter = "Q4"
            elif self.quarter == "Q4":
                self.quarter = "Game Over!"
                self.news_feed_text = "      "
                self.game_over = True
                self.end_game()
            if self.game_over == False:
                self.quarter_time = self.default_time
            self.quarter_label["text"] = self.quarter
        if self.game_over == False:
            self.app.after(1000, self.update_quarter_timer)

    def buy_stock(self, shares):
        if self.player.cash >= self.stock.current_price * shares:
            self.player.cash -= self.stock.current_price * shares
            self.player.shares += shares
            self.player.add_to_bought_at(shares, self.stock.current_price)
            self.update_avg_price()
            self.update_shares_count()
            self.update_cash_display()

    def sell_stock(self, shares):
        if self.player.shares > 0:
            self.player.shares -= shares
            self.player.cash += self.stock.current_price * shares
            self.update_shares_count()
            self.update_cash_display()
            self.player.bought_at = {}
            self.update_avg_price()

    def get_max_buy(self):
        num = int(self.player.cash / self.stock.current_price)
        return num

    def update_news_reel(self):
        self.news_feed_text = self.news_feed_text[1:]
        self.news_feed["state"] = "normal"
        self.news_feed.delete(0, END)
        self.news_feed.insert(0, self.news_feed_text)
        self.news_feed["state"] = "disabled"
        self.app.after(200, self.update_news_reel)

    def add_to_news_feed(self):
        if self.game_over == False:
            news = ["People are talking about " + self.stock.name + ".",
                    "See what " + self.stock.name + " has planned this year in our exclusive interview!",
                    self.stock.name + " has new products coming to stores!", 
                    self.stock.name + " creates new business deal with partner company " + self.stock.randomize_stock_name() + ".",
                    "Thinking about trading " + self.stock.name + "? Here's what you need to know!",
                    "What in the world is going on with " + self.stock.name + " today?",
                    self.stock.name + ": Buy or Sell? We ask investors the important questions!"]
            if self.stock.current_price > self.stock.previous_price:
                news.append("How high will " + self.stock.name + " go?")
                news.append("People are buying up " + self.stock.name + "! Find out why!")
                news.append("What does " + self.stock.name + " know that puts them ahead of competitors?")
                news.append("What's the secret behind " + self.stock.name + "'s impressive growth?")
                news.append(self.stock.name + " blows the competition away with its latest move!")
            else:
                news.append("Investors say " + self.stock.name + " is a risky buy!")
                news.append("Is outdated tech to blame for " + self.stock.name + "'s latest decline?")
                news.append(self.stock.name + " says it may be closing some of its stores this year!")
                news.append("When it comes to " + self.stock.name + ", investors have 1 tip: SELL!")
                news.append("'Tremendous potential being wasted at " + self.stock.name + "' says investors.")
            rando = random.randint(0, len(news) - 1)
            self.news_feed_text += " "
            self.news_feed_text += news[rando]
        else:
            self.news_feed_text += " "
            self.news_feed_text += self.get_score_epilogue(self.player.cash)

    def end_game(self):
        self.buy_button.grid_remove()
        self.sell_button.grid_remove()
        stock = self.stock.name
        score = self.player.cash
        if stock not in self.high_scores:
            self.high_scores[stock] = score
        else:
            if self.high_scores[stock] < score:
                self.high_scores[stock] = score
        self.stock_graph["state"] = "normal"
        self.stock_graph.delete(1.0, END)
        sorted_hs = {k:v for k, v in sorted(self.high_scores.items(), key=lambda x:x[1], reverse=True)}
        line = 1
        for key in sorted_hs.keys():
            dots = 29 - len(str(sorted_hs[key]))
            entry = str(key)
            for a in range(dots):
                entry += "."
            entry += str(sorted_hs[key])
            self.stock_graph.insert(float(line), entry)
            line += 1
            if line > 10:
                break
        self.stock_graph["state"] = "disabled"
        self.play_again_button.grid(row=7, column=0, columnspan=2)

    def get_score_epilogue(self, score):
        epilogue = ""
        if score <= 1000:
            epilogue = "Maybe you're not cut out for this investing stuff..."
        elif score >= 2000 and score < 5000:
            epilogue = "Not bad. You doubled your money! You can afford a downpayment on a cheap car."
        elif score >= 5000 and score < 10000:
            epilogue = "You make enough to pay for rent for a few months. Nice!"
        elif score >= 10000 and score < 50000:
            epilogue = "Time to go get the latest phone and game consoles! It's nice to have some extra spending money!"
        elif score >= 50000 and score < 100000:
            epilogue = "You treat yourself to a new car! Vroom vroom! Zoom zoom! It has a nice paint job!"
        elif score >= 100000 and score < 500000:
            epilogue = "You get yourself a decent home! It has room for guests and a nice kitchen!"
        elif score >= 500000 and score < 1000000:
            epilogue = "You treat yourself to a nice vacation! You're able to travel the world to beautiful locations and you have plenty of spending money!"
        elif score >= 1000000 and score < 50000000:
            epilogue = "Who wants to be a millionaire? You do, obviously! You get yourself a nice home, nice car, treat yourself to a fancy dinner with a good bottle of wine!"
        elif score >= 50000000 and score < 100000000:
            epilogue = "You buy yourself a small island and a yacht that you can land your helicopter on. What a nice vacation home!"
        elif score >= 100000000 and score < 1000000000:
            epilogue = "You can't even keep track of how much money you have. It's spilling out of your pockets!"
        elif score >= 1000000000:
            epilogue = "You own all the money. All of it. Every last cent. It's all yours!"
        return epilogue

game = Game()