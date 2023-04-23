import os
import openai

"""
Copyright (c) 2023 Boris Burgarella

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


class chatGPT():

    def __init__(self):
        # Get the API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Load the system prompt from a file
        file = open("static/Prompts/Generic.pt", "r")
        self.systemPrompt = "".join(file.readlines())
        
        # Create an initial system message
        self.system_message = [
            {'role':"system", "content":self.systemPrompt}
        ]

    def thinkAbout(self, message, conversation):
        # Check if the user's message is valid using OpenAI's Moderation API
        response = openai.Moderation.create(
            input=message
        )
        valid_message = not response["results"][0]["flagged"]
        
        if valid_message:
            # Format the user's message and add it to the conversation
            FormattedMessage = {"role": "user", "content": message}
            conversation.append(FormattedMessage)
            
            # Generate a response using OpenAI's GPT-3 model
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0.5, messages=conversation)
            
            # Format the response and add it to the conversation
            conversation.append({"role": "assistant", "content":response['choices'][0]['message']['content']})
            
            # Write the conversation to a log file
            with open("logs.txt", "w") as file:
                for i in conversation:
                    file.write(str(i)+"\n")
                    
            return conversation
        
        else:
            # If the user's message is not valid, add an error message to the conversation
            FormattedMessage = {"role": "user", "content": message}
            conversation.append(FormattedMessage)
            conversation.append({"role": "assistant", "content":"Je suis désolé, ceci est un message non valide car contraire aux termes et conditions"})
        
        # Return the conversation with or without the response depending on whether the message was valid
        return conversation