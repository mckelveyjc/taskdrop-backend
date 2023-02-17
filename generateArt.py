import os
# import openai
import random
from getTasksFromDB import getTasksForPrompt

# this function takes three random tasks from the "recently_completed" table and generates an 
#   prompt for the AI art generator based on that prompt
def createPrompt():
    # first, let's get three random tasks from the database
    # this is the specific task since they look like this:
    # [('feed the dog',), ('eat veggies',), ('c',)]
    # print(getTasksForPrompt()[0][0])

    randomTaskList = []
    prompt = ""
    randomTasksAsTuples = getTasksForPrompt()
    for task in randomTasksAsTuples:
        randomTaskList.append(randomTasksAsTuples[0][0])
        prompt += randomTasksAsTuples[0][0] + ", "

    randomArtStyleList = [
        "picasso", 
        "van gogh", 
        "rembrandt", 
        "cyber punk",
        "medieval",
        "wild west"
        # any other crazy shit we can think of
    ]

    prompt += "in the style of " + random.choice(randomArtStyleList)
    return prompt

# this function takes the prompt and sends a request for an AI generated image to openAI
def openAIArtRequest():
    # openai.api_key = os.getenv("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")
    openai.api_key = "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"
    image = openai.Image.create(
        prompt="A cute baby sea otter",
        n=1,
        size="1024x1024"
    )
    print(image)

print(createPrompt())