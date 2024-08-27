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

1. **Clone the Repository (Requires Git to be installed on the machine, but recommended)**: Clone the repository from GitHub.

   ```sh
   git clone https://github.com/BAXTOR95/non-steam-game-adder.git
   cd non-steam-game-adder
   ```

2. **Download the Repository (Optional)**: You can download the latest stable release (version 1.0) from the [Releases](https://github.com/BAXTOR95/non-steam-game-adder/releases) page.

   1. **Download the Source Code**:

      - Go to the [Releases](https://github.com/BAXTOR95/non-steam-game-adder/releases) page.
      - Download the `Source code (zip)` or `Source code (tar.gz)` for version 1.0.

   2. **Extract the Archive**:

      - Extract the downloaded zip or tar.gz file to a directory on your computer (ex. non-steam-game-adder).

   3. **Open a terminal and navigate to the extracted directory**

      ```sh
      cd non-steam-game-adder
      ```

3. **Set up a Python Virtual Environment (Optional but recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

4. **Install Required Packages**: Use pip to install the necessary packages.

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
   - Enter the game name and your Steam ID (17-digit number).
   - Browse and select the game directory.
   - Browse and select the executable file for the game.
   - (Optional) The application will try to extract the game icon. If it fails, you can manually set an icon path.
   - Click "Add Game".

2. **Finding Your Steam ID**:
   - Log in to your Steam account in a web browser.
   - Go to your profile page.
   - Your Steam ID is the 17-digit number in the URL of your profile page.
   - Example: If your profile URL is `https://steamcommunity.com/profiles/78901234567890123`, your Steam ID is `78901234567890123`.

3. **Manual App ID**:
   - If the application can't find the app ID for your game, it will open a browser window with SteamDB.
   - Find the app ID on SteamDB and enter it in the application when prompted.

## Troubleshooting

- **Invalid Steam ID**: Make sure you're entering a valid 17-digit Steam ID. The application will show an error if the format is incorrect.
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

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- Thanks to [u/filipebranth](https://www.reddit.com/user/filipebranth/) for the idea.
