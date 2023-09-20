import json
import os

def load_report_card(directory, student_number):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, f"{student_number}.json")
    path = os.path.join(base_path, file_path)

    try:
        with open(path, "r") as file:
            report_card = json.load(file)
    except FileNotFoundError:
        return {}

    return report_card

class Report():
    def __init__(self, students):
        self.total_mark = 0
        self.students = students
        self.subject_total = {"math":0, "science":0, "history":0, "english":0, "geography":0}
        self.grades = {1:[0,0],2:[0,0],3:[0,0],4:[0,0],5:[0,0],6:[0,0],7:[0,0],8:[0,0]}
        self.best = [0,0]
        self.worst = [0,100]
    def load(self,id):
        x = load_report_card("students", id)
        total = 0
        for i in ["math", "science", "history", "english", "geography"]:
            total += x[i]
            self.subject_total[i] += x[i]
        self.grades[x["grade"]][1] += total
        self.grades[x["grade"]][0] += 1
        if total/5 > self.best[1]:
            self.best = (x["id"], total/5)
        if total/5 < self.worst[1]:
            self.worst = (x["id"], total/5)
        self.total_mark += total/5
    def fetch(self):
        for i in range(self.students):
            self.load(i)
    def _sort_stuff(self, stuff):
        stuff = list(stuff.items())
        stuff.sort(reverse=True, key=lambda x: x[1]/self.students)
        return stuff
    def _sort_stuff_tup(self, stuff):
        stuff = list(stuff.items())
        stuff.sort(reverse=True, key=lambda x: x[1][1]/x[1][0])
        return stuff
    def print(self):
        print(f"Average Student Mark: {round(self.total_mark/self.students, 2)}")
        print(f"Hardest Subject: {self._sort_stuff(self.subject_total)[-1][0]}")
        print(f"Easiest Subject: {self._sort_stuff(self.subject_total)[0][0]}")
        print(f"Best Performing Grade: {self._sort_stuff_tup(self.grades)[0][0]}")
        print(f"worst Performing Grade: {self._sort_stuff_tup(self.grades)[-1][0]}")
        print(f"Best Student ID: {self.best[0]}")
        print(f"Worst Student ID: {self.worst[0]}")

report = Report(1000)
report.fetch()
report.print()