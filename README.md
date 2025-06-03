A simple web-based chatbot application that utilizes a cleaned dataset to provide responses. This project combines a Python backend with a frontend built using HTML, CSS, and JavaScript.

## Features

- **Interactive Chat Interface**: Engage in conversations through a user-friendly web interface.
- **Python Backend**: Processes user inputs and generates appropriate responses.
- **Cleaned Dataset**: Utilizes `copbot_dataset_cleaned.csv` for response generation.
- **Modular Design**: Separation of concerns between frontend and backend components.

## Project Structure

chatbot/

├── backend.py                 # Python backend handling user queries

├── copbot_dataset_cleaned.csv # Dataset used for generating responses

├── index.html                 # Main HTML page

├── script.js                  # JavaScript for frontend interactions

├── styles.css                 # Styling for the chatbot interface

├── static/                    # Directory for static assets (if any)

└── .gitignore                 # Specifies files to ignore in version control


## Prerequisites

- Python 3.x installed on your system
- Required Python packages (if any; specify here)

## Installation & Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Asar007/chatbot.git
   cd chatbot
   ```

2. **Install Dependencies**:

   *(If there are any Python dependencies, list them here. For example:)*

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Backend Server:

   ```bash
   python backend.py
   ```

   *Ensure that the server starts without errors.*

4. Access the Chatbot Interface:

   Open `index.html` in your preferred web browser to start interacting with the chatbot.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


