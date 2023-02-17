import os
import openai

# this function takes three random tasks from the "recently_completed" table and generates an 
#   prompt for the AI art generator based on that prompt
def createPrompt():
    # first, let's 
    pass

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
