# Botdesk

**Botdesk** is a powerful desktop automation tool designed to simplify repetitive tasks on your computer. It provides a user-friendly
dashboard for automating common tasks like organizing files, finding duplicate files and analyzing folder structures. Built with Python
and PyQt5, BotDesk is ideal for professionals and everyday users seeking efficiency and time savings.

---

## Features

- **File Organizer**: Automatically organizes files into subfolders based on their extensions.
- **Duplicate Finder**: Detects and lists duplicate files in a selected folder.
- **Folder Analyzer**: Provides insights into folder sizes, file counts, and storage usage.
- **Batch File Renamer**: Rename multiple files in a folder with customizable patterns or by appending timestamps for better organization.
- **File Search and Filter**: Quickly search for specific files based on extensions sizes or modification dates includes advanced filtering options to locate files faster.
- **Scheduled Automation**: Set up automation tasks to run at specific times, such as organizing files or clearing duplicates daily, weekly, or monthly.
- **Drag-and-Drop Support**: Simplifies file selection by allowing users to drag folders or files directly into the app interface.
- **Custom Rules for File Organization**: Set up custom rules to sort files not just by extensions but also by file size, date, or even keywords in filenames.
- **Multi-Folder Support**: Automate actions across multiple folder simultaneously, saving you time for large-scale file operations.
- **Backup & Restore**: Automatically create backups of files before applying any changes, with a one-click restore option for added safety.

---

## Upcoming Features

- **Cloud Integration**: Automate file organization and synchronization with popular cloud storage services like Google Drive, Dropbox, and OneDrive.
- **Advanced File Filters**: Filter files by metadata such as creation date, size range, and custom tags for precise automation.
- **Email Automation**: Automatically download, sort, and organize email attachments into specified folders.
- **File Conversion Tools**: Convert files between popular formats (e.g., PDF to Word, image formats) directly within the app.
- **Text Extraction and OCR**: Extract text from images or scanned documents using Optical Character Recognition (OCR) for document processing tasks.
- **Task Schedular Enhancements**: Introduce an intuitive task calendar to manage recurring
- **Duplicate Detection Improvements**: Add visual previews and advanced duplicate comparison options, such as by resolution for images or embedded metadata.
- **System Cleanup Tools**: Automate cleaning temporary files, caches, and unused programs to optimize computer performance.
- **Zip and Archive Management**: Automate compression and extraction of files, with options to organize extracted content into subfolders.
- **Integration with External APIs**: Enable automations that interact with external APIs for custom workflows, such as downloading reports or scraping web content.
- **Customizable Themes**: Personalize your BotDesk experience with light, dark, and high-contrast themes.
- **Multi-Language Support**: Expand accessibility with support for multiple languages, starting with French, Spanish and German.
- **Ai-Powered Suggestions**: Leverage AI to analyze usage patterns and recommend automation tasks tailored to your workflow.

---

## Installation
### Prerequisites

1. Install 3.8 or higher
2. Install pip (Python's package manager)
3. Install the required dependencies using the command
``
pip install -r requirements.txt
``

### Steps to Run
1. Clone this repository:
```
git clone https://github.com/C4bbage64/BotDesk
```
2. Navigate to the project directory:
```
cd BotDesk
```
3. Run the application:
```
python main.py
```

---

## Usage
### Dashboard Overview

When you launch BotDesk, you'll be greeted with a dashboard featuring multiple automation options. Each option provides a dedicated
interface to execute the desired automation.

1. File Organizer:
   - Enter a folder path.
   - Specify file extensions(comma-seperated).
   - Click "Organize Files" to sort files into subfolders by extension.
2. Duplicate Finder:
    - Enter a folder path
    - Click "Find Duplicates" to detect duplicate files in the selected folder.
    - View duplicate results in the log area.
3. Folder Analyzer:
    - Enter a folder path.
    - Click "Analyzer" to get detailed statistics about the folder and its contents

---

## Project Structure

```
BotDesk/
├── automations/
│   ├── file_organizer.py       # Core logic for file organization
│   ├── duplicate_finder.py     # Core logic for finding duplicate files
│   ├── folder_analyzer.py      # Core logic for analyzing folders
├── ui/
│   ├── dashboard.py            # Main dashboard UI
│   ├── file_organizer.py       # File Organizer UI
│   ├── duplicate_finder.py     # Duplicate Finder UI
│   ├── folder_analyzer.py      # Folder Analyzer UI
├── main.py                     # Entry point of the application
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Dependencies

The following Python libraries are required:
- PyQt5
- os
- shutil
- hashlib

Install all dependencies with:
```
pip install -r requirements.txt
```

---

# Future Enhancements

Planned features for upcoming versions
- Add more automation tools, like scheduled tasks or batch renaming.
- Introduce drag-and-drop functionality for file selection.
- Save user preferences for faster operations
- Support for advanced file (e.g., by size or date)

---

# Contributing
Contributions are welcome! If you'd like to improve this project:
1. Fork the repository.
2. Create a feature branch:
```
git checkout -b feature-name
```
3. Commit your changesand push the branch:
```
git push origin feature-name
```
4. Create a pull request

---

## License

This project is licensed under the MIT License

---

## Acknowledgements

Special thanks to the open-source community for their tools and inspirations