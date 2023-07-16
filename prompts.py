import config

OUTPUT_FORMAT_NO_ASCII = f"""
The output format must be JSON, with the fields: next_section_text, current_location_name.
"""
# ASCII ART is un-reliable, so removed it.
OUTPUT_FORMAT = OUTPUT_FORMAT_NO_ASCII

def _get_SHORT_STORY_PROMPT(user_name):
    return f"""
    {user_name} awoke from the ice cold grip of the cryo chamber, their body and mind aching from the trauma of a deep and un-natural sleep.
    Unsure of where they were, and how much of their mind was still of human flesh, {user_name} struggled to sit up.
    In the darkness beyond, light flickered and {user_name} could hear something approach.
    """

def _get_RPG_PROMPT(user_name):
    return f"""
    In the dark forest, a lone warrior named {user_name} stood, a sword gleaming in the moonlight. {user_name} had journeyed far, seeking the ancient artifact that
    held the power to save the kingdom. The air was thick with tension as they cautiously moved forward, their senses alert for any sign of danger. 
    Suddenly, a horde of goblins emerged from the shadows, their eyes filled with malice. 
    With a swift swing of their blade, {user_name} the warrior engaged in a fierce battle, determined to protect their land and fulfill their destiny.
    """

def _get_ZOMBIE_PROMPT(user_name):
    return f"""
    The world had changed. The dead walked among the living, their hunger insatiable. Survivors huddled in abandoned buildings, barricading themselves from the horrors outside. Fear was their constant companion. {user_name} was one of them. They had lost everything – their family, their home. Now, {user_name} fought to stay alive. Every day was a battle, a struggle for survival. {user_name} had become numb to the violence, the bloodshed. But deep down, a flicker of hope remained. Hope that one day, the world would be free from the clutches of the undead
    """

def _get_MEDIEVAL(user_name):
    return f"""
    In a small village nestled amidst rolling hills, a young blacksmith named {user_name} toiled day and night. Their strong hands crafted swords and armor, their skill renowned throughout the land. One fateful day, a mysterious traveler arrived, bearing news of a legendary sword hidden deep within the enchanted forest. Intrigued, {user_name} embarked on a perilous journey, armed with only determination. As they ventured deeper into the forest, the air grew thick with magic, and the path ahead became treacherous. Little did they know, their destiny awaited them within those ancient woods.
    """

def _get_VAMPIRE_PROMPT(user_name):
    return f"""
        In the dimly lit alley, a figure, {user_name}, emerged from the shadows. Pale skin, sharp fangs glinting in the moonlight. A vampire. Their eyes, blood-red and hungry, scanned the deserted streets. A prey was near. He moved swiftly, silently, like a predator stalking its prey. The scent of fear filled the air as he closed in on the victim. With a swift motion, he sank their fangs into the soft flesh, drinking the life force. The victim's body went limp, drained of all vitality. Another night, another feast for the vampire
        """

def build_next_prompt(story_type, user_name, rsp_parsed, user_input, format = OUTPUT_FORMAT):
    return f"""
        Analyze the given {story_type} story text, and use the next-actions to generate the next part of the {story_type} story.
        The next-actions are what {user_name} does next.
        The output text must be a continuation of the short story, using the same names, location and style.
        
        The input text and the next-actions are delimited by triple backticks.
        The output text length should be {config.NEXT_SECTION_WORD_COUNT} words.

        {format}

    text: ```{rsp_parsed["next_section_text"]}```

    {user_name}'s next-actions: ```{user_input}```
    """

def get_initial_text(story_type, user_name):
    if story_type == "short":
        return _get_SHORT_STORY_PROMPT(user_name)
    elif story_type == "RPG":
        return _get_RPG_PROMPT(user_name)
    elif story_type == "zombie":
        return _get_ZOMBIE_PROMPT(user_name)
    elif story_type == "medieval":
        return _get_MEDIEVAL(user_name)
    elif story_type == "vampire":
        return _get_VAMPIRE_PROMPT(user_name)
    else:
        raise (f"Unhandled story_type {story_type}")

def get_first_prompt(story_type, initial_text):
    return f"""
    Your task is to analyze the given beginning of a {story_type} story,
    and generate a complete {story_type} story.

    The given text is delimited by triple backticks. 

    The {story_type} story should be in a minamalist and low context style, similar to the given text.

    The length should be {config.INITIAL_WORD_COUNT} words.

    {OUTPUT_FORMAT}

    text: ```{initial_text}```
    """

def get_story_types():
    return ['short', 'RPG', 'zombie', 'medieval', 'vampire']
