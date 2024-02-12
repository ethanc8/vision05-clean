import datetime
import pathlib

class Target():
    def __init__(self, name: str, username: str, number: int):
        self.name = name
        self.username = username
        self.number = number
        try:
            self.firstVictimDay = datetime.date(2024, 2, 10+number)
        except:
            self.firstVictimDay = datetime.date(2024, 12, 31)
    
    def isVictim(self) -> bool:
        return datetime.date.today() <= self.firstVictimDay

TargetDirectoryButton = None
TargetPage = None