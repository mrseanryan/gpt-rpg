import json

import config
import prompts
from util_chat import send_prompt
import util_wait

def next_prompt(prompt):
    if config.is_debug:
        return send_prompt(prompt, temperature=config.TEMPERATURE)
    return send_prompt(prompt, False, False, temperature=config.TEMPERATURE)

def main_loop(story_type, user_name):
    initial_text = prompts.get_initial_text(story_type, user_name)
    prompt = prompts.get_first_prompt(story_type, initial_text)
    print(initial_text)

    is_playing = True

    rsp = None
    rsp_parsed = None
    user_input = ""
    while (is_playing):
        next_rsp_parsed = None
        retries_remaining = config.RETRY_COUNT
        while(not next_rsp_parsed and retries_remaining > 0):
            try:
                rsp = next_prompt(prompt)
                if config.is_debug:
                    print(rsp)
                next_rsp_parsed = json.loads(rsp, strict=False)
            except Exception as error:
                print("!! error: ", error)
                print("REQ: ", prompt)
                print("RSP: ", rsp)
                util_wait.wait_seconds(config.RETRY_WAIT_SECONDS)
                prompt = prompts.build_next_prompt(story_type, user_name, rsp_parsed, user_input, prompts.OUTPUT_FORMAT_NO_ASCII)
                retries_remaining -= 1
        rsp_parsed = next_rsp_parsed

        print(f"LOCATION: " + rsp_parsed['current_location_name'])
        print(rsp_parsed["next_section_text"])

        user_input = input(f"What next, {user_name}? >>")
        prompt = prompts.build_next_prompt(story_type, user_name, rsp_parsed, user_input)
