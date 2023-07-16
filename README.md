# gpt-rpg README
A simple RPG game built on Chat-GPT

## Dependencies

- Python3
- Chat GTP 3.5 Turbo

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
