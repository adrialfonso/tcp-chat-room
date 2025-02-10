# TCP Chat Application

This is a simple TCP-based localhost chat application implemented in Python using sockets and threads. The application includes both a server and a client component, allowing users to connect to the server, choose a nickname, and engage in real-time text-based communication with other connected clients.

## Features

- Multi-client chat server.
- Color-coded messages for a better user experience.
- Simple and easy-to-understand implementation.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- [colorama](https://pypi.org/project/colorama/) library

  To install the required dependencies, use the following command:

  ```bash
  pip install -r requirements.txt

## Chat Setup

1. **Server Setup:**

   Run the server script:
   ```bash
   python server.py

2. **Client Setup:**

   Run the client script:
   ```bash
   python client.py

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please feel free to open an issue or submit a pull request, specially to enable out of LAN communication.

## Acknowledgments
Thanks to Neuralnine's and his content on Youtube tutorials for transmiting very useful python sockets & threading knowledge. The base code is from one of his videos, thanks to him I've relearned some OS concepts and use it in a totally practical context.
