import pandas as pd


class Ranking:
    top = []  # top 10 scores
    csv_file = "../data/ranking.csv"

    def __init__(self):
        df = pd.read_csv(self.csv_file)
        df = df.sort_values(by=["score"], ascending=False)
        df = df.reset_index(drop=True)
        # df to array of dictionaries
        self.top = df.head(10).to_dict("records")

    def readRanking(self):
        df = pd.read_csv(self.csv_file)
        df = df.sort_values(by=["score"], ascending=False)
        df = df.reset_index(drop=True)
        self.top = df.head(10).to_dict("records")
        return

    def willInsertScore(self, score):
        if len(self.top) < 10:
            return True

        return score > int(self.top[-1]["score"])

    def insertScore(self, name, score, draw):
        if name != "":
            df = pd.read_csv(self.csv_file)
            df.loc[len(df)] = [name, score, draw]
            df = df.sort_values(by=["score"], ascending=False)
            df = df.reset_index(drop=True)
            df.to_csv(self.csv_file, index=False)
            self.top = df.head(10).to_dict("records")
            print(self.top)
