# Voice-based Task Tracker Usage Guide

This document provides detailed instructions on how to use the Voice-based Task Tracker application.

## Starting the Application

To start the application, run:
```
python voice_task_tracker.py
```

## GUI Interface

The application window contains:

1. **Task Entry Field**: Type in new task descriptions and add them with the "Add Task" button
2. **Voice Command Button**: Click to start listening for voice commands
3. **Task List**: Displays all tasks with their ID, description, and status
4. **Action Buttons**: "Mark Complete" and "Delete Task" buttons to act on selected tasks
5. **Status Bar**: Shows feedback messages and current application status

## Interacting with Tasks

### Using the GUI

- **Add a task**: Type the task description in the entry field and click "Add Task"
- **Complete a task**: Select a task and click "Mark Complete", or double-click the task to toggle its status
- **Delete a task**: Select a task and click "Delete Task"
- **View all tasks**: The task list automatically displays all tasks

### Using Voice Commands

Click the "Voice Command" button and speak your command clearly. The application will provide voice feedback.

Available voice commands:

1. **Adding tasks**
   - "Add buy groceries"
   - "Create finish report"

2. **Completing tasks**
   - "Complete 1" (completes task with ID 1)
   - "Mark done 3" (completes task with ID 3)
   - "Complete buy groceries" (tries to complete by matching description)

3. **Deleting tasks**
   - "Delete 2" (deletes task with ID 2)
   - "Remove 4" (deletes task with ID 4)
   - "Delete finish report" (tries to delete by matching description)

4. **Listing tasks**
   - "List tasks"
   - "Show tasks"

## Tips for Better Voice Recognition

1. **Speak clearly** and at a moderate pace
2. **Wait for feedback** before giving another command
3. **Use the task ID number** when possible for more accurate results
4. **Reduce background noise** for better recognition
5. **Position the microphone** properly (about 6-12 inches from your mouth)

## Troubleshooting

If you experience issues with voice recognition:

1. Check that your microphone is properly connected and working
2. Make sure you have granted the application permission to use your microphone
3. Try speaking more clearly and directly into the microphone
4. If in a noisy environment, try moving to a quieter location
5. Restart the application if voice recognition becomes unreliable

## Task Storage

Tasks are automatically saved to a `tasks.json` file in the same directory as the application. This ensures your tasks persist between sessions.