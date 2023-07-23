import prompts
import util_pick

import main_service
import service_images

user_name = input("What is your name? >>")

# note: sci-fi seems more 'grown up' than RPG
story_type = util_pick.pick_one_by_prompt(prompts.get_story_types())

def handle_image_prompt(last_text):
    global story_type
    image_url = service_images.generate_image(last_text, story_type)
    print(image_url)

def main_loop(story_type, user_name):
    state = main_service.get_initial_state(story_type, user_name)

    initial_text = main_service.get_initial_text(state)
    print(initial_text)

    user_input = None

    def next_input():
        return input(f"What next, {user_name}? >>")

    is_playing = True
    last_text = initial_text
    while (is_playing):
        if user_input is not None:
            if service_images.is_image_prompt(user_input):
                handle_image_prompt(last_text)
                user_input = next_input()
                continue

        (next_section_text, current_location_name) = main_service.get_next(state, user_input)

        print(f"LOCATION: " + current_location_name)
        print(next_section_text)

        last_text = next_section_text
        user_input = next_input()

main_loop(story_type, user_name)
