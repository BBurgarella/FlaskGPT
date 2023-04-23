# Flask ChatGPT App with PyWebview GUI

This is a simple Flask application that allows anyone to use the OpenAI ChatGPT API with a Graphical User Interface (GUI) built with PyWebview. This app uses SQLite to store user login credentials.

The release .exe was built using  [Bat2Exe](https://github.com/islamadel/bat2exe)

## Dependencies

This app requires the following dependencies:

- sqlite3
- Flask
- Werkzeug
- PyWebview

## Installation

1. Clone this repository: `git clone https://github.com/<your-username>/<your-repo-name>.git`
2. Install the required dependencies by running `pip install -r requirements.txt` from the root directory.
3. Register for an OpenAI API key and paste it in the `API_KEY` and create an environement variable named "OPENAI_API_KEY"
4. Run the app by executing `python app.py` from the command line.

## Usage

1. Upon starting the app, you will be prompted to create an account. Follow the instructions to create a new account.
2. After logging in, you will be directed to the chat interface. Type in your message and hit 'Send' to get a response from the OpenAI ChatGPT API.

## Future Improvements

- Allow users to select from a systemprompt library

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



