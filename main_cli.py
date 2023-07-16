import prompts
import util_pick
import main

user_name = input("What is your name? >>")

# note: short seems more 'grown up' than RPG
story_type = util_pick.pick_one_by_prompt(prompts.get_story_types())

main.main_loop(story_type, user_name)
