from Target import *

targets = [
    Target(name="ethanc8",
           username="ethanc8",
           number=1),
# !!! page_home_newPerson NEW TARGET !!!
]

if TargetDirectoryButton:
       target_buttons = [TargetDirectoryButton(target) for target in targets]
       target_pages = [TargetPage(target) for target in targets]

targets2 = targets.copy()

targets2.append(Target(name="", username="Unknown", number="unknown"))

nameForTarget = {target.username:target.name for target in targets2}
numberForTarget = {target.username:target.number for target in targets2}