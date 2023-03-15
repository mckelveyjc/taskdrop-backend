import os
import openai
import random
from getTasksFromDB import getTasksForPrompt

# this function takes three random tasks from the "recently_completed" table and generates an 
#   prompt for the AI art generator based on that prompt
def createPrompt():
    # get random tasks from the database
    prompt = ""
    randomTasksAsTuples = getTasksForPrompt()
    for taskIndex in range(len(randomTasksAsTuples)):
        prompt += randomTasksAsTuples[taskIndex][0] + ", "

    randomArtStyleList = [
        "picasso", 
        "van gogh", 
        "cyber punk",
        "medieval",
        "wild west", 
        "a 90s sitcom",
        "salvador dali",
        "star wars"
        # add any other crazy stuff here
    ]

    # generate a prompt based on the random tasks & a random art style
    #   eg. return "feed the cat, tea with grandma, buy groceries in the style of picasso"
    prompt += "in the style of " + random.choice(randomArtStyleList)
    return prompt

# this function takes the prompt and sends a request for an AI generated image to openAI
def openAIArtRequest():
    generatedPrompt = createPrompt()
    openai.api_key = "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"
    generatedImageData = openai.Image.create(
        prompt= generatedPrompt,
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )
    return generatedImageData