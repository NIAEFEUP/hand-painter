import pandas as pd

class Ranking:
    top = []  # top 10 scores

    def __init__(self):
        df = pd.read_csv("data/ranking.csv")
        df = df.sort_values(by=["score"], ascending=False)
        df = df.reset_index(drop=True)
        # df to array of dictionaries
        self.top = df.head(10).to_dict("records")

    def readRanking(self):
        df = pd.read_csv("data/ranking.csv")
        df = df.sort_values(by=["score"], ascending=False)
        df = df.reset_index(drop=True)
        self.top = df.head(10).to_dict("records")
        return

    def willInsertScore(self, score):
        if len(self.top) < 10:
            return True

        return score > int(self.top[-1]["score"])

    def insertScore(self, name, score, draw):
        if(name != ''):
            df = pd.read_csv('data/ranking.csv')
            df = df.append({'name':name, 'score':score, 'draw':draw}, ignore_index=True)
            df = df.sort_values(by=['score'], ascending=False)
            df = df.reset_index(drop=True)
            df.to_csv("data/ranking.csv", index=False)
            self.top = df.head(10).to_dict("records")
            print(self.top)
