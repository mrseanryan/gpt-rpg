# gpt-rpg README

A simple RPG game built on Chat-GPT

## Dependencies

- Python3
- Chat GTP 3.5 Turbo

## Example Games

### [zombie storyline]

```
What is your name? >>Sean
['short', 'RPG', 'zombie', 'medieval', 'vampire']
Please pick one >>zombie

    The world had changed. The dead walked among the living, their hunger insatiable. Survivors huddled in abandoned buildings,
    barricading themselves from the horrors outside. Fear was their constant companion. Sean was one of them. They had lost everything
    – their family, their home. Now, Sean fought to stay alive. Every day was a battle, a struggle for survival. Sean had become numb
    to the violence, the bloodshed. But deep down, a flicker of hope remained. Hope that one day, the world would be free from the clutches
    of the undead

LOCATION: Underground Bunker
Sean ventured out of the safehouse, his heart pounding in his chest. He navigated the desolate streets, his eyes scanning for any signs of
movement. Suddenly, a group of zombies emerged from the shadows, their milky white eyes fixed on him. Sean sprinted, adrenaline fueling his
every step. He ducked into an alley, narrowly avoiding their grasp. As he caught his breath, he noticed a flicker of light in the distance.
Curiosity pulled him closer, and he discovered a hidden underground bunker. Inside, a group of survivors had established a thriving community.
Sean finally felt a glimmer of hope, knowing he had found a place to call home.
What next, Sean? >>call home
LOCATION: underground bunker
Sean took out his phone and dialed the familiar number.
```

### [RPG storyline]

```
In the dark forest, a lone warrior named Sean stood, a sword gleaming in the moonlight. Sean had journeyed far, seeking the ancient artifact
that held the power to save the kingdom. The air was thick with tension as they cautiously moved forward, their senses alert for any sign of
danger. Suddenly, a horde of goblins emerged from the shadows, their eyes filled with malice. With a swift swing of their blade, Sean the warrior
engaged in a fierce battle, determined to protect their land and fulfill their destiny.
---
What's next, Sean? >> Take the path to the temple.
---
LOCATION: Dark Forest
---
>> As the goblins fell one by one, Sean could see the path ahead leading to an ancient temple. They knew deep inside that the artifact awaited
them there. With adrenaline coursing through their veins, they made their way towards the temple, their heart pounding with anticipation.
---
What's next, Sean? >> Enter the temple
---
LOCATION: Ancient Temple
---
>> As Sean stepped through the ancient doors of the temple, a wave of ancient energy washed over them. The air inside was heavy with the scent
of incense and the sound of distant chanting echoed through the halls. Sean felt a mix of excitement and trepidation as they ventured deeper
into the temple, the artifact calling out to them. The flickering torches along the walls cast eerie shadows, adding to the mystique of their journey.
---
```

## Set up

1. Install openai Python client.

```
pip install openai
```

2. Get an Open AI key

3. Copy paste file `api-key.chatgpt.example.py` to `api-key.chatgpt.local.py`

4. Edit the local config file so that it contains your API key

## Test

```
./go.sh
```

or

```
python3 main_cli.py
```

## Chat-GPT Notes

### Principle 1 - Write Clear and Specific Instructions

- tactic 1: use delimiters, to denote what is the 'data input'
- tactic 2: ask for structured input (as opposed to journalist style or casual informal style)
- tactic 3: ask to check whether conditions are satisfied.
- tactic 4: few-shot prompting -> give successful examples of completing tasks, then ask the model to perform the task.

### Principle 2 - Give the model time to think.

- tactic 1: Instuct the model to spend more time! (outline specific steps to take)
- tactic 2: Instruct the model to work out its own solution before rushing to a conclusion

### Iterative prompt developement

- analyze errors, try to improve the prompt
- try include context (if too big, can use summaries?)

### Model Capabilities

- Summarizing
- Inferring
- Transforming (language, tone, format)
- Expanding

### Model Limitations

- does not know the boundary of its knowledge -> if asked on topic it has little knowledge of, it makes plausible but false statements -> hallucinations!

mitigations:

- asking the model to include a warning if it is not sure
- ask to use relevant information
- (ask to provide links to the source of the information)

## Related

Inspired by an excellent DeepLearning.ai course: [Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
