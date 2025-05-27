# Voice-based Task Tracker

A Python application that allows users to manage a to-do list using voice commands. It utilizes speech recognition to understand voice commands, text-to-speech for feedback, and a Tkinter GUI for visual interaction.

## Features

- **Voice Commands**: Add, delete, and complete tasks using voice commands
- **Voice Feedback**: Get voice responses confirming actions and reading back tasks
- **Graphical Interface**: View and manage tasks through an intuitive GUI
- **Task Management**: Add, update, complete, and delete tasks
- **Persistent Storage**: Tasks are saved to a JSON file for persistence

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `speech_recognition`: For capturing and processing voice input
  - `pyttsx3`: For text-to-speech functionality
  - `tkinter`: For the graphical user interface (typically included with Python)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/siddjoshi-org-a/Voice-based-task-tracker.git
   cd Voice-based-task-tracker
   ```

2. Install the required packages:
   ```
   pip install SpeechRecognition pyttsx3
   ```

3. You may need to install additional dependencies for `speech_recognition`:
   - For Windows, you might need PyAudio: `pip install pyaudio`
   - For Linux: `sudo apt-get install python3-pyaudio portaudio19-dev`
   - For macOS: `brew install portaudio && pip install pyaudio`

## Usage

Run the application:
```
python voice_task_tracker.py
```

### Voice Commands

- **Add a task**: Say "add [task description]" or "create [task description]"
- **Complete a task**: Say "complete [task number]" or "mark done [task number]"
- **Delete a task**: Say "delete [task number]" or "remove [task number]"
- **List tasks**: Say "list tasks" or "show tasks"

You can also perform these actions using the GUI buttons and controls.

## License

This project is open source and available under the MIT License.