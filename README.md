# Non-Steam Game Adder

Welcome to the Non-Steam Game Adder project! This application allows you to add your favorite non-Steam games to your Steam library, making it easier to launch and manage all your games from one place.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- Add non-Steam games to your Steam library
- Automatically extract and set game icons
- Save and load user configurations
- Simple and user-friendly interface

## Prerequisites

Before you can run this application, you'll need to have the following installed on your computer:

1. **Python**: You can download and install Python from [python.org](https://www.python.org/downloads/).
2. **pip**: Python's package installer, which is included with Python installations.

## Installation

1. **Clone the Repository**: Download the repository from GitHub.

   ```sh
   git clone https://github.com/BAXTOR95/SteamGameAutomator.git
   cd SteamGameAutomator
   ```

2. **Set up a Python Virtual Environment (Optional but recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Required Packages**: Use pip to install the necessary packages.

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **Get a Steam API Key**:

   - Visit the [Steam API key registration page](https://steamcommunity.com/dev/apikey).
   - Log in with your Steam account.
   - Follow the instructions to register a domain (you can use `localhost` if you're not sure).
   - Copy the API key provided.

2. **Create a `.env` File**:

   - In the root directory of the project, create a file named `.env`.
   - Add your Steam API key to the file:

     ```plaintext
     STEAM_API_KEY=your_api_key_here
     ```

## Running the Application

1. **Launch the Application**:

   ```sh
   python main.py
   ```

   This will start the Non-Steam Game Adder application.

## Usage

1. **Add a Game**:

   - Open the application.
   - Enter the game name and your Steam username.
   - Browse and select the game directory.
   - Browse and select the executable file for the game.
   - (Optional) The application will try to extract the game icon. If it fails, you can manually set an icon path.
   - Click "Add Game".

2. **Manual App ID**:
   - If the application can't find the app ID for your game, it will open a browser window with SteamDB.
   - Find the app ID on SteamDB and enter it in the application when prompted.

## Troubleshooting

- **Steam is Running**: If Steam is running, the application will prompt you to close it. Make sure to close Steam manually if the application fails to do so.
- **Configuration Issues**: If the application fails to load or save configurations, check the `config.json` file in the project directory for errors.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.

## Acknowledgments

- Thanks to [u/filipebranth](https://www.reddit.com/user/filipebranth/) for the idea.
