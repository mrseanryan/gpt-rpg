import json

import config
import prompts
import service_chat
import util_wait

def get_initial_state(story_type, user_name):
    state = dict()
    state["story_type"] = story_type
    state["user_name"] = user_name
    return state

def get_initial_text(state):
    return prompts.get_initial_text(state["story_type"], state["user_name"])

def get_next(state, user_input):
    prompt = ""
    next_section_text = ""
    if user_input is None:
        initial_text = get_initial_text(state)
        prompt = prompts.get_first_prompt(state["story_type"], initial_text)
    else:
        next_section_text = state["next_section_text"]
        prompt = prompts.build_next_prompt(state["story_type"], state["user_name"], next_section_text, user_input)

    next_rsp_parsed = None
    retries_remaining = config.RETRY_COUNT
    while(not next_rsp_parsed and retries_remaining > 0):
        rsp = None
        try:
            rsp = service_chat.next_prompt(prompt)
            next_rsp_parsed = json.loads(rsp, strict=False)
        except Exception as error:
            print("!! error: ", error)
            print("REQ: ", prompt)
            print("RSP: ", rsp)
            util_wait.wait_seconds(config.RETRY_WAIT_SECONDS)
            prompt = prompts.build_next_prompt(state["story_type"], state["user_name"], next_section_text, user_input, prompts.OUTPUT_FORMAT_NO_ASCII)
            retries_remaining -= 1

    if next_rsp_parsed is None:
        print(f"!!! RETRIES EXPIRED !!!")
        return(next_section_text, "(unknown)")
    else:
        state["next_section_text"] = next_rsp_parsed["next_section_text"]

    return (next_rsp_parsed["next_section_text"], next_rsp_parsed["current_location_name"])
