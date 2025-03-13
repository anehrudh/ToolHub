# Tool Hub

## Overview
Tool Hub is a multi-functional desktop application built using Python Tkinter. It integrates seven essential tools in a single platform, enhancing productivity and convenience for users.

## Features
- **YouTube Downloader** - Download videos from YouTube by providing a URL.
- **Wikipedia Summary** - Fetch summarized information from Wikipedia.
- **Bulk Mail Sender** - Send bulk emails with customizable content.
- **Text-to-Speech** - Convert text into speech and save it as an audio file.
- **Dictionary** - Get word definitions and meanings instantly.
- **Video Compressor** - Compress video files without significant quality loss.
- **Image Converter** - Convert images between different formats.

## Tech Stack
- **Language:** Python
- **GUI Framework:** Tkinter
- **Backend:** SQLite (for storing usage reports and tracking metrics)
- **APIs Used:** YouTube API, Wikipedia API, SMTP for mail sending, and Google Text-to-Speech

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/anehrudh/toolhub.git
   ```
2. Navigate to the project directory:
   ```sh
   cd toolhub
   ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python main.py
   ```

## Database Schema
The SQLite database stores:
- **Usage Reports:** Logs each tool usage with timestamps.
- **User Metrics:** Tracks entry, exit times, and duration for each tool.

## Contribution
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any issues or inquiries, contact anirudhbhatka@gmail.com.

