# Python Treeview Image Viewer

This project is a simple GUI application that allows users to browse the directory structure of their machine and view image files within selected directories. It utilizes the `tkinter` library for the graphical interface.

## Project Structure

```
python-treeview-imageviewer
├── src
│   ├── main.py          # Entry point of the application
│   ├── gui
│   │   ├── treeview.py  # Contains DirectoryTreeView class for directory navigation
│   │   └── listbox.py   # Contains ImageListBox class for displaying image files
│   └── utils
│       └── file_utils.py # Utility functions for file operations
├── requirements.txt      # Lists the dependencies required for the project
└── README.md             # Documentation for the project
```

## Setup Instructions

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application by executing the following command:
   ```
   python src/main.py
   ```
2. The main window will open, displaying a Treeview on the left side for directory navigation and a Listbox on the right side for viewing image files.
3. Click on a directory in the Treeview to load and display the image files in the Listbox.

## Dependencies

- `tkinter`: For creating the GUI.
- Additional libraries may be included in `requirements.txt` for image handling.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.