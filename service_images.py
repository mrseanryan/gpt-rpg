import openai

import service_api_key

openai.api_key = service_api_key.get_openai_key()

def generate_image(last_text, story_type):
    image_url = None

    prompt = f"""
        Generate an image to match the short story genre:{story_type}.
        The image must be as realistic as possible.

        Image description:
    {last_text}
    """

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512" # "1024x1024",
    )

    image_url = response["data"][0]["url"]
    return image_url

def is_image_prompt(user_input):
    # TODO could ask LLM to classify this - like gpt-command
    IMAGE_PROMPTS = ["image", "show", "view"]
    return user_input.lower() in IMAGE_PROMPTS
