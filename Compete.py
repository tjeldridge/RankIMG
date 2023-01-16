from OpenDir import OpenDir, checkslash
from GUI import GUI
from time import time
from random import shuffle
from JSON import jsondata


class Compete:
    def __init__(self, directory: str, json_file: str = "data.json", **tags):
        self.directory = OpenDir(directory)
        self.json = jsondata(json_file)
        self.tags = dict(**tags)
        # Organize Competitors
        self.competitors = self.json.competitors
        self.competition_log = self.json.competition_log
        self.total_competitors = len(self.competitors)
        self.add_competitors(**tags)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_competitors(self, **kwargs):
        for img in self.directory.allfiles:
            if img in kwargs.keys():
                tags = kwargs[img]
            else:
                tags = {}
            if img not in self.competitors:
                self.total_competitors += 1
                self.competitors[img] = {
                    "ID": self.total_competitors,
                    "competitions": 0,
                    "wins": 0,
                    "losses": 0,
                    "ties": 0,
                    "total score": 0.0,
                    "average score": 0.0,
                    "tags": {**tags}
                }
            if img not in self.competition_log:
                self.competition_log[img] = {}
        self.json.update_data()

    def random_competition(self, manual_list: list = None):
        if manual_list is not None:
            shuffle(manual_list)
            random_files = manual_list
        else:
            random_files = self.directory.randomize()
        winners = []
        losers = []
        if len(random_files) % 2 != 0:
            winners.append(random_files[-1])
        notatend = True
        i = 0
        while notatend:
            try:
                img1 = random_files[i]
                img2 = random_files[i + 1]
                img1_result, img2_result = self.compete(img1, img2)
                if img1_result == "Win" or img1_result == "Tie":
                    winners.append(img1)
                elif img1_result == "Loss":
                    losers.append(img1)
                else:
                    raise KeyError
                if img2_result == "Win" or img2_result == "Tie":
                    winners.append(img2)
                elif img2_result == "Loss":
                    losers.append(img2)
                else:
                    raise KeyError
            except IndexError:
                notatend = False
            i += 2
        self.json.update_data()
        return winners, losers

    def random_bracket(self):
        eliminated = []
        winners, losers = self.random_competition()
        loserwinners, elim = self.random_competition(manual_list=losers)
        eliminated.extend(elim)
        while len(winners) > 1:
            winners, winnerlosers = self.random_competition(manual_list=winners)
            loserwinners.extend(winnerlosers)
            loserwinners, elim = self.random_competition(manual_list=loserwinners)
            eliminated.extend(elim)
        while len(loserwinners) > 1:
            loserwinners, elim = self.random_competition(manual_list=loserwinners)
            eliminated.extend(elim)
        finalists = winners + loserwinners
        champion, runnerup = self.random_competition(manual_list=finalists)
        return champion, runnerup, list(reversed(eliminated))

    def compete(self, img1, img2):
        img1_path = checkslash(self.directory.directory) + img1
        img2_path = checkslash(self.directory.directory) + img2
        img1_data = self.competitors[img1]
        img2_data = self.competitors[img2]
        img1_log = self.competition_log[img1]
        img2_log = self.competition_log[img2]
        with GUI(img1_path, img2_path) as gooey:
            winner = gooey.button_pressed
            if winner == "One":
                img1_data["wins"] += 1
                img2_data["losses"] += 1
                img1_data["total score"] += 1
                img1_result = "Win"
                img2_result = "Loss"
            elif winner == "Two":
                img2_data["wins"] += 1
                img1_data["losses"] += 1
                img2_data["total score"] += 1
                img1_result = "Loss"
                img2_result = "Win"
            elif winner == "Three":
                img1_data["ties"] += 1
                img2_data["ties"] += 1
                img1_data["total score"] += 0.5
                img2_data["total score"] += 0.5
                img1_result = "Tie"
                img2_result = "Tie"
            else:
                raise KeyError("Somehow the buttons are not mapped to output one among"
                               " 'One', 'Two', or 'Three'.")
            img1_data["competitions"] += 1
            img2_data["competitions"] += 1
            img1_data["average score"] = img1_data["total score"] / img1_data["competitions"]
            img2_data["average score"] = img2_data["total score"] / img2_data["competitions"]
            timestamp = "%d" % time()
            img1_log[timestamp] = {
                "competitor": img2,
                "result": img1_result
            }
            img2_log[timestamp] = {
                "competitor": img1,
                "result": img2_result
            }
        return img1_result, img2_result

    def sort_by_avg(self):
        d = {key: value["average score"] for key, value in self.competitors.items()}
        a = sorted(d.items(), key=lambda x: x[1], reverse=True)
        return a

    def top(self, x):
        ranks = self.sort_by_avg()
        for i in range(x):
            filename = ranks[i][0]
            score = ranks[i][1]
            print("#%d: %s \t Score: %.3f" % (i + 1, filename, score))

# End
