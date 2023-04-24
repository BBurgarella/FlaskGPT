# A Flask ChatGPT App with PyWebview GUI

<img src="https://github.com/BBurgarella/FlaskGPT/blob/main/static/images/logo.png" width=50% height=50%>

This is a simple Flask application that allows anyone to use the OpenAI ChatGPT API with a Graphical User Interface (GUI) built with PyWebview. This app uses SQLite to store user login credentials.

The release .exe was built using  [Bat2Exe](https://github.com/islamadel/bat2exe)

## Dependencies

This app requires the following dependencies:

- sqlite3
- Flask
- Werkzeug
- PyWebview
- openai

## Installation

1. Clone this repository: `git clone https://github.com/BBurgarella/FlaskGPT.git`
2. Install the required dependencies by running `pip install -r requirements.txt` from the root directory.
3. Register for an OpenAI API key and and create an environement variable named "OPENAI_API_KEY" with the key in it
4. Run the app by executing `python app.py` from the command line.

## Usage

![Demo image](https://github.com/BBurgarella/FlaskGPT/blob/main/static/images/Demo_image.png)

To start the chatbot, run the following command:
```
python chatbot.py [agent_name]
```
Replace `[agent_name]` with the name of the agent you want the chatbot to use (optional). If no agent name is provided, the chatbot will use the default agent.
Example:
```
python chatbot.py Funny
```
This will start the chatbot using the `Funny` example agent. If you want to use the default agent, simply run:
```
python chatbot.py
```
to customize agents or add your own, use json format as per the examples in the agent folder, your new agents should always be in this folder

1. Upon starting the app, you will be prompted to create an account. Follow the instructions to create a new account. (this account is local and stored on your disk)
2. After logging in, you will be directed to the chat interface. Type in your message and hit 'Send' to get a response from the OpenAI ChatGPT API.

-> if you are unfamiliar with python and on windows, you can download the latest release to directly access to the GUI through a .exe file

## Known issues

- if running on mac OC with conda, some user seems to experience the keyboard being captured by the terminal instead of the app window, this is a known issue from the PyWebView library [Link to the issue](https://github.com/r0x0r/pywebview/issues/66) the solution is to run:
```>>> conda install python.app ``` and then run the app using ```>>> pythonw app.py ```

## Future Improvements

- Allow users to select from a systemprompt library
- avoid having to re-create a username and password if using the compiled version

## License

This project is licensed under the MIT License.

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



