import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime
import sqlite3
import mysql.connector

class FormApp(tk.Tk):
    def __init__(self, args, config):
        super().__init__()
        self.args = args
        self.config = config
        self.fields = {}

        # Setup logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        # Log the configuration
        logging.info("Configuration loaded: %s", self.config['form'])

        self.title(self.config.get("title", "Form Application"))
        self.create_form_fields()
        self.create_buttons()


    def create_form_fields(self):
        for index, field_config in enumerate(self.config['form']["columns"]):
            row = tk.Frame(self)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            label = tk.Label(row, text=field_config["label"], width=22, anchor='w')
            label.pack(side=tk.LEFT)

            entry = None
            if field_config["type"] == "VARCHAR":
                entry = tk.Entry(row)
                if "max_length" in field_config:
                    entry.config(validate="key", validatecommand=(self.register(self.on_validate), '%P', field_config["max_length"]))
                if "placeholder" in field_config:
                    entry.insert(0, field_config["placeholder"])
                if "default" in field_config:
                    entry.delete(0, tk.END)
                    entry.insert(0, field_config["default"])

            elif field_config["type"] == "INTEGER":
                entry = tk.Entry(row, validate="key", validatecommand=(self.register(self.validate_int), '%P'))

            elif field_config["type"] == "DECIMAL":
                entry = tk.Entry(row, validate="key", validatecommand=(self.register(self.validate_decimal), '%P', field_config.get("precision", 2)))

            elif field_config["type"] == "DATETIME":
                entry = tk.Entry(row)
                default_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entry.insert(0, default_datetime)

            elif field_config["type"] == "BOOLEAN":
                entry = tk.Checkbutton(row, text="Yes", onvalue=True, offvalue=False)
                entry.var = tk.BooleanVar(value=field_config.get("default", False))
                entry.config(variable=entry.var)

            if entry:
                entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                self.fields[field_config["id"]] = entry

    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        tk.Button(button_frame, text="Save", command=self.save_to_database).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5, pady=5)

    def save_to_database(self):
        data = {field_id: self.get_field_value(field_id) for field_id in self.fields}

        # reconstruct the data as a list in the same order as the columns
        data = [str(data[field["id"]]) for field in self.config['form']["columns"]]
        logging.debug("Data to save: %s", data)

        # Make a list of columns names to be used in the SQL query
        columns = [field['id'] for field in self.config['form']["columns"]]
        logging.debug("Columns: %s", columns)
        # log data to debug
        logging.debug("Data to save: %s", data)
        try:
            if self.args.dbtype == "sqlite":
                conn = sqlite3.connect(self.args.connection)
            elif self.args.dbtype == "mysql":
                conn = mysql.connector.connect(host=self.args.host, user=self.args.user,
                                            password=self.args.password, database=self.args.database)
            else:
                logging.error("Unsupported database type")
                messagebox.showerror("Error", "Unsupported database type")
                return
            
            cursor = conn.cursor()

            self.ensure_table_exists(cursor)

            # Constructing SQL query for insertion
            columns_str = ', '.join(columns)
            # Add ' single quotes around each item in data
            for i in range(len(data)):
                data[i] = f"'{data[i]}'"

            data_str = ', '.join(data)
            sql = f"INSERT INTO tablename ({columns_str}) VALUES ({data_str})"
            # log the sql to debug
            logging.debug("SQL Query: %s", sql)

            # Executing the SQL command
            cursor.execute(sql, tuple(data))
            conn.commit()
            logging.info("Data saved to database successfully")

        except Exception as e:
            logging.error("Failed to save data: %s", e)
            messagebox.showerror("Error", "Failed to save data to database.")
        finally:
            if conn:
                conn.close()

    def clear_form(self):
        for field_id, widget in self.fields.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Checkbutton):
                widget.var.set(False)

    def get_field_value(self, field_id):
        widget = self.fields[field_id]
        if isinstance(widget, tk.Entry):
            return widget.get()
        elif isinstance(widget, tk.Checkbutton):
            return widget.var.get()
        return None

    def on_validate(self, value, max_length):
        if len(value) <= int(max_length):
            return True
        else:
            return False

    def validate_int(self, value):
        if value.isdigit() or value == "":
            return True
        else:
            return False

    def validate_decimal(self, value, precision):
        try:
            if value:
                float(value)
                return len(value.split('.')[-1]) <= int(precision)
            return True
        except ValueError:
            return False

    def ensure_table_exists(self, cursor):
        create_statement = """
        CREATE TABLE IF NOT EXISTS tablename (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {}
        );
        """
        columns = []
        for field in self.config['form']["columns"]:
            column_type = {
                "VARCHAR": f"{field['id']} VARCHAR({field.get('max_length', 255)})",
                "INTEGER": f"{field['id']} INTEGER",
                "DECIMAL": f"{field['id']} DECIMAL",
                "DATETIME": f"{field['id']} DATETIME",
                "BOOLEAN": f"{field['id']} BOOLEAN"
            }.get(field["type"], "VARCHAR(255)")
            columns.append(column_type)
        
        create_statement = create_statement.format(", ".join(columns))
        cursor.execute(create_statement)
        logging.info("Checked for table existence and created if not present")
