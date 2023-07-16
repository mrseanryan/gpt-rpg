import prompts
import util_pick

import main_service

user_name = input("What is your name? >>")

# note: short seems more 'grown up' than RPG
story_type = util_pick.pick_one_by_prompt(prompts.get_story_types())

def main_loop(story_type, user_name):
    state = main_service.get_initial_state(story_type, user_name)

    initial_text = main_service.get_initial_text(state)
    print(initial_text)

    user_input = None

    is_playing = True
    while (is_playing):
        (next_section_text, current_location_name) = main_service.get_next(state, user_input)

        print(f"LOCATION: " + current_location_name)
        print(next_section_text)

        user_input = input(f"What next, {user_name}? >>")

main_loop(story_type, user_name)
