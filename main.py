import json
import random
from util_chat import send_prompt

INITIAL_WORD_COUNT = 120
NEXT_SECTION_WORD_COUNT = 80

def pick_one(texts):
    return random.choice(texts)

def pick_one_by_prompt(texts):
    valid_selection = None
    while (not valid_selection):
        print(texts)
        selected = input("Please pick one >>")
        if (selected in texts):
            valid_selection = selected
    return valid_selection

user_name = input("What is your name? >>")

# Sometimes ASCII art breaks the JSON response (overflow?)
OUTPUT_FORMAT=f"""
The output format must be JSON, with the fields: next_section_text, current_location_name, current_map_ascii_art.
The field current_map_ascii_art should be ASCII art map, max 20 lines, showing the location of {user_name} and surrounding objects.
"""
OUTPUT_FORMAT_NO_ASCII=f"""
The output format must be JSON, with the fields: next_section_text, current_location_name.
"""
# The field scene_ascii_art should be ASCII art based on a person or object of field next_section_text, max 20 lines.
# ASCII ART is un-reliable:
OUTPUT_FORMAT = pick_one([OUTPUT_FORMAT, OUTPUT_FORMAT_NO_ASCII])

# short seems more 'grown up' than RPG
story_type = pick_one_by_prompt(['short', 'RPG', 'zombie', 'medieval', 'vampire', 'romance-fem'])

if story_type == "short":
    initial_text = f"""
    {user_name} awoke from the ice cold grip of the cryo chamber, their body and mind aching from the trauma of a deep and un-natural sleep.
    Unsure of where they were, and how much of their mind was still of human flesh, {user_name} struggled to sit up.
    In the darkness beyond, light flickered and {user_name} could hear something approach.
    """
elif story_type == "RPG":
    initial_text = f"""
    In the dark forest, a lone warrior named {user_name} stood, a sword gleaming in the moonlight. {user_name} had journeyed far, seeking the ancient artifact that
    held the power to save the kingdom. The air was thick with tension as they cautiously moved forward, their senses alert for any sign of danger. 
    Suddenly, a horde of goblins emerged from the shadows, their eyes filled with malice. 
    With a swift swing of their blade, {user_name} the warrior engaged in a fierce battle, determined to protect their land and fulfill their destiny.
    """
elif story_type == "zombie":
    initial_text = f"""
    The world had changed. The dead walked among the living, their hunger insatiable. Survivors huddled in abandoned buildings, barricading themselves from the horrors outside. Fear was their constant companion. {user_name} was one of them. They had lost everything – their family, their home. Now, {user_name} fought to stay alive. Every day was a battle, a struggle for survival. {user_name} had become numb to the violence, the bloodshed. But deep down, a flicker of hope remained. Hope that one day, the world would be free from the clutches of the undead
    """
elif story_type == "medieval":
    initial_text = f"""
    In a small village nestled amidst rolling hills, a young blacksmith named {user_name} toiled day and night. Their strong hands crafted swords and armor, their skill renowned throughout the land. One fateful day, a mysterious traveler arrived, bearing news of a legendary sword hidden deep within the enchanted forest. Intrigued, {user_name} embarked on a perilous journey, armed with only determination. As they ventured deeper into the forest, the air grew thick with magic, and the path ahead became treacherous. Little did they know, their destiny awaited them within those ancient woods.
    """
elif story_type == "vampire":
    initial_text = f"""
    In the dimly lit alley, a figure, {user_name}, emerged from the shadows. Pale skin, sharp fangs glinting in the moonlight. A vampire. Their eyes, blood-red and hungry, scanned the deserted streets. A prey was near. He moved swiftly, silently, like a predator stalking its prey. The scent of fear filled the air as he closed in on the victim. With a swift motion, he sank their fangs into the soft flesh, drinking the life force. The victim's body went limp, drained of all vitality. Another night, another feast for the vampire
    """
elif story_type == "romance-fem":
    initial_text = f"""
    She, {user_name}, walked into the café, her eyes scanning the room.
    And then she saw him. He was sitting alone at a table by the window, sipping his coffee. She couldn't help but notice his tousled hair and the way he absentmindedly tapped his fingers on the table. Their eyes met, and in that moment, everything else faded away. It was as if time stood still. She took a deep breath and mustered up the courage to approach him. Little did she know, this chance encounter would change their lives forever.
    """
else:
    raise(f"Unhandled story_type {story_type}")

prompt = f"""
Your task is to analyze the given beginning of a {story_type} story,
and generate a complete {story_type} story.

The given text is delimited by triple backticks. 

The {story_type} story should be in a minamalist and low context style, similar to the given text.

The length should be {INITIAL_WORD_COUNT} words.

{OUTPUT_FORMAT}

text: ```{initial_text}```
"""

is_debug = False

def next_prompt(prompt):
    global is_debug
    # 0 would be same each time. 0.7 or 1 would be difference each time, and less likely words can be used:
    temperature = 0.7
    if is_debug:
        return send_prompt(prompt,temperature=temperature)
    return send_prompt(prompt, False, False, temperature=temperature)

print(initial_text)

is_playing = True

def build_next_prompt(rsp_parsed, user_input, format = OUTPUT_FORMAT):
    return f"""
        Analyze the given {story_type} story text, and use the next-actions to generate the next part of the {story_type} story.
        The next-actions are what {user_name} does next.
        The output text must be a continuation of the short story, using the same names, location and style.
        
        The input text and the next-actions are delimited by triple backticks.
        The output text length should be {NEXT_SECTION_WORD_COUNT} words.

        {format}

    text: ```{rsp_parsed["next_section_text"]}```

    {user_name}'s next-actions: ```{user_input}```
    """

while (is_playing):
    next_rsp_parsed = None
    while(not next_rsp_parsed):
        try:
            rsp = next_prompt(prompt)
            if is_debug:
                print(rsp)
            next_rsp_parsed = json.loads(rsp, strict=False)
        except Exception as error:
            print("!! error: ", error)
            print("REQ: ", prompt)
            print("RSP: ", rsp)
            input("Try again? >>")
            # turn off ASCII art:
            OUTPUT_FORMAT = OUTPUT_FORMAT_NO_ASCII
            prompt = build_next_prompt(rsp_parsed, user_input, OUTPUT_FORMAT_NO_ASCII)
    rsp_parsed = next_rsp_parsed
    if("current_map_ascii_art" in rsp_parsed):
        print(rsp_parsed["current_map_ascii_art"])
    print(f"LOCATION: " + rsp_parsed['current_location_name'])
    # print(rsp_parsed["scene_ascii_art"])
    print(rsp_parsed["next_section_text"])

    user_input = input(f"What next, {user_name}? >>")
    prompt = build_next_prompt(rsp_parsed, user_input)
