#!/usr/bin/env python3
"""
Voice-based Task Tracker

A Python application that allows users to manage a to-do list using voice commands.
It utilizes speech recognition to understand voice commands, text-to-speech for feedback,
and a Tkinter GUI for visual interaction.
"""

import os
import json
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk, messagebox


class Task:
    """A class representing a task in the to-do list."""
    
    def __init__(self, task_id, description, completed=False):
        """
        Initialize a task with an ID, description, and completion status.
        
        Args:
            task_id (int): The unique ID of the task.
            description (str): A description of the task.
            completed (bool, optional): Whether the task is completed. Defaults to False.
        """
        self.id = task_id
        self.description = description
        self.completed = completed
    
    def to_dict(self):
        """Convert the task to a dictionary for serialization."""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed
        }
    
    @classmethod
    def from_dict(cls, task_dict):
        """Create a task from a dictionary."""
        return cls(
            task_id=task_dict['id'],
            description=task_dict['description'],
            completed=task_dict['completed']
        )


class TaskManager:
    """Manages the list of tasks and provides operations to manipulate tasks."""
    
    def __init__(self, save_file="tasks.json"):
        """
        Initialize the task manager with an empty task list or load from a file.
        
        Args:
            save_file (str, optional): The file path to save tasks to. Defaults to "tasks.json".
        """
        self.tasks = []
        self.next_id = 1
        self.save_file = save_file
        self.load_tasks()
    
    def add_task(self, description):
        """
        Add a new task to the list.
        
        Args:
            description (str): The description of the task.
            
        Returns:
            Task: The newly created task.
        """
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def update_task(self, task_id, description=None, completed=None):
        """
        Update an existing task.
        
        Args:
            task_id (int): The ID of the task to update.
            description (str, optional): The new description. Defaults to None.
            completed (bool, optional): The new completion status. Defaults to None.
            
        Returns:
            Task: The updated task, or None if not found.
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        self.save_tasks()
        return task
    
    def delete_task(self, task_id):
        """
        Delete a task from the list.
        
        Args:
            task_id (int): The ID of the task to delete.
            
        Returns:
            bool: True if the task was deleted, False otherwise.
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def get_task(self, task_id):
        """
        Get a task by its ID.
        
        Args:
            task_id (int): The ID of the task to get.
            
        Returns:
            Task: The task, or None if not found.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            list: A list of all tasks.
        """
        return self.tasks
    
    def save_tasks(self):
        """Save tasks to a file."""
        with open(self.save_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)
    
    def load_tasks(self):
        """Load tasks from a file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    tasks_data = json.load(f)
                    
                self.tasks = [Task.from_dict(task_dict) for task_dict in tasks_data]
                
                # Update next_id to be one more than the maximum ID
                if self.tasks:
                    self.next_id = max(task.id for task in self.tasks) + 1
                else:
                    self.next_id = 1
            except (json.JSONDecodeError, KeyError):
                # If the file is invalid, start with an empty task list
                self.tasks = []
                self.next_id = 1


class VoiceRecognizer:
    """Handles voice recognition and command interpretation."""
    
    def __init__(self):
        """Initialize the voice recognizer."""
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise when the recognizer instance is initialized
        # This helps improve voice recognition accuracy
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
        except (sr.RequestError, sr.UnknownValueError):
            # Handle case where microphone is not available or ambient noise adjustment fails
            pass
    
    def listen(self):
        """
        Listen for voice input.
        
        Returns:
            str: The recognized speech, or None if recognition failed.
        """
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
                
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
    
    def interpret_command(self, text):
        """
        Interpret a voice command.
        
        Args:
            text (str): The text to interpret.
            
        Returns:
            tuple: A tuple containing the command and parameters.
        """
        if not text:
            return None, None
        
        text = text.lower()
        
        if "add" in text or "create" in text:
            # Extract the task description after "add" or "create"
            parts = text.split("add ", 1) if "add" in text else text.split("create ", 1)
            if len(parts) > 1:
                return "add", parts[1]
            return "add", ""
        
        elif "delete" in text or "remove" in text:
            # Try to extract a task number
            words = text.split()
            for i, word in enumerate(words):
                if word in ["delete", "remove"] and i+1 < len(words):
                    try:
                        task_id = int(words[i+1])
                        return "delete", task_id
                    except ValueError:
                        # If the next word is not a number, try to use the rest as a description
                        if i+1 < len(words):
                            return "delete_by_desc", " ".join(words[i+1:])
            return "delete", None
        
        elif "complete" in text or "mark done" in text:
            # Try to extract a task number
            words = text.split()
            for i, word in enumerate(words):
                if word in ["complete", "done"] and i+1 < len(words):
                    try:
                        task_id = int(words[i+1])
                        return "complete", task_id
                    except ValueError:
                        # If the next word is not a number, try to use the rest as a description
                        if i+1 < len(words):
                            return "complete_by_desc", " ".join(words[i+1:])
            return "complete", None
        
        elif "list" in text or "show" in text:
            return "list", None
        
        return None, None


class VoiceFeedback:
    """Provides voice feedback to the user."""
    
    def __init__(self):
        """Initialize the voice feedback system."""
        self.engine = pyttsx3.init()
        # Can set properties like rate, volume, etc.
        self.engine.setProperty('rate', 150)  # Speed of speech
    
    def speak(self, text):
        """
        Speak the given text.
        
        Args:
            text (str): The text to speak.
        """
        self.engine.say(text)
        self.engine.runAndWait()


class TaskTrackerApp:
    """Main application class for the voice-based task tracker."""
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Voice-based Task Tracker")
        self.root.geometry("600x400")
        
        self.task_manager = TaskManager()
        self.voice_recognizer = VoiceRecognizer()
        self.voice_feedback = VoiceFeedback()
        
        self.create_widgets()
        self.update_task_list()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Task input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Task entry
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        # Add task button
        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Voice command button
        voice_button = ttk.Button(input_frame, text="Voice Command", command=self.start_voice_command)
        voice_button.pack(side=tk.LEFT, padx=5)
        
        # Task list frame with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task list (Treeview)
        self.task_tree = ttk.Treeview(
            list_frame,
            columns=("ID", "Description", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Status", text="Status")
        
        self.task_tree.column("ID", width=50)
        self.task_tree.column("Description", width=400)
        self.task_tree.column("Status", width=100)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_tree.yview)
        
        # Bind double click on task to toggle completion
        self.task_tree.bind("<Double-1>", self.toggle_task_completion)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Complete button
        complete_button = ttk.Button(button_frame, text="Mark Complete", command=self.complete_task)
        complete_button.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        delete_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=5)
    
    def update_task_list(self):
        """Update the task list display."""
        # Clear the current list
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Add all tasks
        for task in self.task_manager.get_all_tasks():
            status = "Completed" if task.completed else "Pending"
            self.task_tree.insert("", "end", values=(task.id, task.description, status))
    
    def add_task(self):
        """Add a new task from the entry field."""
        description = self.task_entry.get().strip()
        if description:
            self.task_manager.add_task(description)
            self.task_entry.delete(0, tk.END)  # Clear the entry
            self.update_task_list()
            self.status_var.set(f"Added task: {description}")
    
    def complete_task(self):
        """Mark the selected task as complete."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a task to mark as complete.")
            return
        
        # Get the task ID from the selected item
        task_id = int(self.task_tree.item(selected_item[0], "values")[0])
        self.task_manager.update_task(task_id, completed=True)
        self.update_task_list()
        self.status_var.set(f"Marked task {task_id} as complete")
    
    def delete_task(self):
        """Delete the selected task."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a task to delete.")
            return
        
        # Get the task ID from the selected item
        task_id = int(self.task_tree.item(selected_item[0], "values")[0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task {task_id}?"):
            self.task_manager.delete_task(task_id)
            self.update_task_list()
            self.status_var.set(f"Deleted task {task_id}")
    
    def toggle_task_completion(self, event):
        """Toggle the completion status of the selected task."""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        # Get the task ID and current status from the selected item
        values = self.task_tree.item(selected_item[0], "values")
        task_id = int(values[0])
        current_status = values[2]
        
        # Toggle the completion status
        new_completed = current_status != "Completed"
        self.task_manager.update_task(task_id, completed=new_completed)
        self.update_task_list()
        
        new_status = "completed" if new_completed else "pending"
        self.status_var.set(f"Updated task {task_id} to {new_status}")
    
    def start_voice_command(self):
        """Start listening for a voice command."""
        self.status_var.set("Listening...")
        self.voice_feedback.speak("Listening for command")
        self.root.after(100, self.process_voice_command)
    
    def process_voice_command(self):
        """Process the voice command."""
        text = self.voice_recognizer.listen()
        if not text:
            self.status_var.set("Sorry, I didn't catch that.")
            self.voice_feedback.speak("Sorry, I didn't catch that")
            return
        
        command, param = self.voice_recognizer.interpret_command(text)
        
        if command == "add":
            if param:
                self.task_manager.add_task(param)
                self.update_task_list()
                feedback = f"Added task: {param}"
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
            else:
                self.status_var.set("Please specify a task to add.")
                self.voice_feedback.speak("Please specify a task to add")
        
        elif command == "delete" and param is not None:
            if isinstance(param, int):
                task = self.task_manager.get_task(param)
                if task:
                    self.task_manager.delete_task(param)
                    self.update_task_list()
                    feedback = f"Deleted task {param}"
                    self.status_var.set(feedback)
                    self.voice_feedback.speak(feedback)
                else:
                    feedback = f"Task {param} not found"
                    self.status_var.set(feedback)
                    self.voice_feedback.speak(feedback)
            else:
                self.status_var.set("Please specify a task number to delete.")
                self.voice_feedback.speak("Please specify a task number to delete")
        
        elif command == "delete_by_desc":
            # Try to find a task with a matching description
            matching_tasks = [task for task in self.task_manager.get_all_tasks() 
                             if param.lower() in task.description.lower()]
            if len(matching_tasks) == 1:
                task = matching_tasks[0]
                self.task_manager.delete_task(task.id)
                self.update_task_list()
                feedback = f"Deleted task: {task.description}"
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
            elif len(matching_tasks) > 1:
                feedback = "Multiple matching tasks found. Please be more specific."
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
            else:
                feedback = "No matching task found."
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
        
        elif command == "complete" and param is not None:
            if isinstance(param, int):
                task = self.task_manager.get_task(param)
                if task:
                    self.task_manager.update_task(param, completed=True)
                    self.update_task_list()
                    feedback = f"Marked task {param} as complete"
                    self.status_var.set(feedback)
                    self.voice_feedback.speak(feedback)
                else:
                    feedback = f"Task {param} not found"
                    self.status_var.set(feedback)
                    self.voice_feedback.speak(feedback)
            else:
                self.status_var.set("Please specify a task number to complete.")
                self.voice_feedback.speak("Please specify a task number to complete")
        
        elif command == "complete_by_desc":
            # Try to find a task with a matching description
            matching_tasks = [task for task in self.task_manager.get_all_tasks() 
                             if param.lower() in task.description.lower()]
            if len(matching_tasks) == 1:
                task = matching_tasks[0]
                self.task_manager.update_task(task.id, completed=True)
                self.update_task_list()
                feedback = f"Marked task as complete: {task.description}"
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
            elif len(matching_tasks) > 1:
                feedback = "Multiple matching tasks found. Please be more specific."
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
            else:
                feedback = "No matching task found."
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
        
        elif command == "list":
            tasks = self.task_manager.get_all_tasks()
            if not tasks:
                feedback = "Your task list is empty."
                self.status_var.set(feedback)
                self.voice_feedback.speak(feedback)
            else:
                feedback = "Here are your tasks: "
                for task in tasks:
                    status = "completed" if task.completed else "pending"
                    feedback += f"Task {task.id}, {task.description}, {status}. "
                
                self.status_var.set("Listed all tasks")
                self.voice_feedback.speak(feedback)
        
        else:
            self.status_var.set(f"Command not recognized: {text}")
            self.voice_feedback.speak("Command not recognized")
    
    def on_close(self):
        """Handle window close event."""
        # Make sure tasks are saved
        self.task_manager.save_tasks()
        self.root.destroy()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()