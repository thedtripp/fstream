# fStream - Ephemeral Text Streaming App

## Introduction
fStream is a groundbreaking ephemeral text streaming application built with Flask and Socket.IO. It is inspired by the fleeting nature of Snapchat and text-based apps like Twitter and Threads. The app challenges traditional online communication by introducing a unique approach to content sharing – one message at a time, in real-time. This revolutionary social media platform, named "fStream," embraces minimalism and engages users through a live-streaming experience that doesn't support replays.

![fstreamv0 1-demo](https://github.com/thedtripp/fstream/assets/38776199/e786bc7f-b918-48e3-82f8-9663a2e3c9b1)

## Table of Contents
- [Introduction](#introduction)
- [Key Features](#key-features)
- [Why fStream](#why-fstream)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **Real-time Text Streaming:** Users share content one word per second, creating an immersive and engaging experience.
  
- **Ephemeral Nature:** No replays are supported, emphasizing the exclusivity and urgency of the content.

- **Follower/Following Model:** Connect with your audience in real-time, fostering a direct and immediate connection between content creators and consumers.

- **Minimalistic Design:** Focus on the message without distractions, setting fStream apart from traditional social media platforms.

- **No Endless Feeds:** Ideal for busy individuals, the real-time text stream keeps users updated without the need for extended browsing sessions.

- **Dynamic Message Display:** Incoming messages are displayed with a dynamic scrolling effect for an engaging user experience.

## Why fStream?

fStream isn't just a social media platform; it's a revolution in communication. It offers:

- **Simplicity:** Minimalist design puts the focus on the message rather than flashy graphics.

- **Utility:** Stay informed without spending hours scrolling through feeds.

- **Exclusivity:** No replays create a sense of urgency and exclusivity, driving user engagement.

Join the revolution today and be part of a new way to communicate, consume, and connect with like-minded individuals. fStream - where the message matters.


## Installation

To run the **fstream** application locally, follow these steps:

1. Clone the GitHub repository:

   ```bash
   git clone https://github.com/thedtripp/fstream.git
   ```

2. Navigate to the project directory:

   ```bash
   cd fstream
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python server.py
   ```

2. Open your web browser and go to [http://localhost:5000](http://localhost:5000).

3. Start fStreaming!

## Technologies Used

- [Flask](https://flask.palletsprojects.com/en/3.0.x/): A micro web framework for Python.
- [Socket.IO](https://socket.io/): A library for real-time web applications.

## Contributing

If you'd like to contribute to **fstream**, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Description of your changes'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
