I am building a python tkinter application that generates its user interface from a YAML file.
Each YAML file serves as a configuration file for dynamically generating a form entry GUI for a database table.

# Requirements:
 - There are buttons below the form entry fields to save the data to the database, and to clear the form.
 - The GUI part of the application is encapsulated in a class.
 - The python program has a if __main__ block that creates an instance of the class and runs the mainloop.
 - Argparse is used to specify the yaml file to use and to specify a local or remote database.
 - Sqlite and Mysql are supported.
 - The form entry allows different datatypes for each column in the table, varchar(255), integer, decimal, and datetime.
 - Each column has a database identifier (e.g. battery_voltage), a label (e.g. Battery Voltage), and a type (e.g. DECIMAL).
 - The GUI shows the entry label with a field alongside for the user to fill in.
 - For the datetime type, the field is filled in with the current datetime.
 - Use python logging to log errors and debug messages.
 - Use git to manage the project.

# YAML File Structure:
- **form**: The top-level element containing all form-related configurations.
  - **title**: A string that specifies the title of the form. This title is displayed at the top of the GUI form.
  - **columns**: A list of dictionaries, each representing an input field in the form.

## Field Definitions within `columns`:
Each dictionary in the `columns` list corresponds to a form field and contains the following keys:

- **id** (string): A unique identifier for the corresponding database column. This identifier is used as the key in database operations.
- **label** (string): The human-readable label displayed next to the input field in the GUI.
- **type** (string): The data type of the input field. Valid types are:
  - **VARCHAR**: For text strings.
  - **INTEGER**: For integer numbers.
  - **DECIMAL**: For decimal numbers.
  - **DATETIME**: For date and time entries.
  - **BOOLEAN**: For true/false values.
- **max_length** (integer, optional): Applicable to `VARCHAR`, specifies the maximum number of characters.
- **placeholder** (string, optional): Text that appears in the input field to guide the user on what to enter.
- **default** (varies, optional): Default value for the field. Specific behaviors include:
  - For `DATETIME`, setting `"now"` will fill the field with the current date and time.
  - For `BOOLEAN`, `"true"` or `"false"` sets the default state of a checkbox.
- **precision** (integer, optional): Applicable to `DECIMAL`. `precision` defines the total number of digits allowed.

# Project Directory Structure:
/form-app/
│
├── src/                    # Source files
│   ├── main.py             # Entry point of the application
│   ├── app.py              # Application class handling GUI
│   └── ...                 # More files as needed.
│
├── config/                 # Configuration files
│   ├── eqinspect.yml       # Example database table worksheet.
│   └── eqcheckin.yml       # Example database table worksheet.
│
├── tests/                  # Unit and integration tests
│   ├── test_app.py
│   └── ...
│
├── docs/                   # Documentation files
│   └── README.md
│
├── .gitignore              # Specifies intentionally untracked files to ignore
├── create.sh               # Creates this directory structure and files
├── LICENSE                 # Empty license file, for future use
├── requirements.txt        # Required Python packages
├── setup.py                # Setup script for the application
└── MANIFEST.in             # Include non-code files

# Classes

## Tkinter Application Window Class

**Class Name**: `FormApp`
**Source File**: `app.py`

**Purpose**: The `FormApp` class, by subclassing `tk.Tk`, serves as the main application window for a Tkinter-based form entry GUI. It simplifies the integration of GUI components and functionality by directly inheriting from `tk.Tk`. The form GUI is dynamically generated based on a configuration dictionary derived from a YAML file, with command-line arguments specifying database connectivity options. This class is responsible for rendering GUI elements, handling user input, and executing database operations, supporting both local SQLite and remote MySQL databases.

**Attributes**:
- `args`: The results from Argparse.
- `config`: A dictionary containing the form configuration, pre-loaded from the YAML file.
- `fields`: A dictionary that maps field identifiers to their corresponding Tkinter widgets, facilitating easy data manipulation and retrieval.

**Methods**:
- `__init__(self, args, config)`: Constructor that initializes the Tkinter window, sets up the database type based on `args`, saves the `config` attribute, and calls methods to build the form fields and buttons.
- `create_form_fields(self)`: Dynamically generates form fields according to the `columns` specified in the `config` dictionary. Each widget is configured based on properties such as type, default values, and placeholders.
- `save_to_database(self)`: Collects data from the form widgets, formats it according to the database schema, and executes the necessary database commands to insert or update records.
- `clear_form(self)`: Resets all form fields to their default states or clears them, as defined by their configuration in the `config`.

**Behavior**:
- Upon instantiation, the class initializes itself as a Tkinter main window, setting up its properties and layout based on the provided `config` and `args`.
- It then generates the GUI components for each form field as specified in the `columns` of the `config`. This includes handling various data types such as date pickers for `DATETIME` fields and checkboxes for `BOOLEAN`.
- The application features buttons for database operations and form management, linking GUI actions directly to database interactions.
- As a subclass of `tk.Tk`, all window-related methods are directly accessible, simplifying event handling, window configuration, and lifecycle management.

# Command Line Arguments (argparse)

**YAML Configuration File (`--config`, `-c`)**
- Type: String (file path)
- Description: Path to the YAML file for form configuration.
- Default: './config/eqinspect.yml'
- Required: No.

**Database Type (`--dbtype`, `-t`)**
- Choices: `sqlite`, `mysql`
- Description: Type of the database (local SQLite or remote MySQL).
- Required: Yes.

**Database Connection String (`--connection`, `-cn`)**
- Type: String
- Description: Connection string or file path for the database.
- Required: Yes.

# Tasks:
- [x] Write a description of the project directory structure.
- [x] Write a description of the yaml file
- [x] Write a description of the classes and interfaces.
- [x] Create a bash script that generates the folder structure for the project, .gitignore, and empty python files.
- [x] Create the git repository and connect the project to git.
- [ ] Fill in the python code for the classes and interfaces.
- [ ] Write a requirements.txt file for all of the modules we will be requiring.
- [ ] Write a readme.md that includes usage instructions.

The next task is to write app.py.  Give me the python for app.py.  Using logging to log errors and debug messages to the console.






