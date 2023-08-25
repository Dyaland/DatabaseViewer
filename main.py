import sqlite3
import tkinter as tk
from tkinter import font  # For setting font globally
from tkinter.filedialog import askopenfilename as open_file
from os.path import basename  # Display filename without file-path

import sql_functions
import button_functions
from support_classes import AutoScrollbar, SharedStates, DataRow
from dataframe import DataFrame


class Main(tk.Tk):
    """Class containing base gui elements and operational functions"""
    def __init__(self):
        super().__init__()
        self.geometry('900x600+250+100')
        self.title('SQL Database Manager')
        self.config(bg="light gray")
        self.resizable(False, False)

        # Default styles
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Courier New", size=11)
        self.option_add("*Font", default_font)
        self.option_add("*Background", "light gray")
        self.option_add("*Foreground", "black")
        self.option_add("*Entry*Background", "white")
        self.option_add("*Text*Background", "light gray")
        self.option_add("*HighlightThickness", 0)

        # Widget kwargs shortcuts
        self.selected = {"bg": "light green", "relief": "sunken"}
        self.unselected = {"bg": "light gray", "relief": "raised"}
        self.ridge, self.raised, self.sunken = {"relief": "ridge"}, {"relief": "raised"}, {"relief": "sunken"}

        # Imports
        self.sql = sql_functions.SupportFunctions  # Import my SQL functions
        self.obj = button_functions  # Import my buttons and general button functions
        self.bf = button_functions.ButtonFunctions()  # Import button functions
        self.shared_states = SharedStates()

        # Variables
        self.f_path = ""
        self.headers, self.data, self.form_width = ["placeholder"], [["placeholder"]], []
        self.tables_names = ["placeholder"]  # Used for generating table selection buttons
        self.table_i = 0  # Keeping track of which table is currently selected.
        self.current_row = []  # Container for list to send for writing to sql table
        self.entry_i = 0  # Index used for user input selections and/or iterations.
        self.display_data = [self.tables_names[self.table_i], self.headers, self.data]
        self.data_frames = []  # Container for addressing data frames for  removal

        # Layout: Root level Frames
        self.screen = tk.Frame(self)
        self.screen.pack(fill="both", padx=5, pady=5, expand=True)

        # Layout: Screen Frame widgets
        self.side_frame = tk.Frame(self.screen, bd=4, relief="ridge")
        self.side_frame.pack(side="left", fill="y", anchor="nw")
        self.top_frame = tk.Frame(self.screen, bd=4, relief="ridge")
        self.top_frame.pack(side="top", fill="both", anchor="nw")
        self.canvas_frame = tk.Frame(self.screen, bd=4, relief="ridge")
        self.canvas_frame.pack(fill="both", expand=True)
        self.data_canvas = tk.Canvas(self.canvas_frame)
        self.data_canvas.pack(side="left", fill="both", anchor="nw", expand=True)
        self.main_scroll = AutoScrollbar(self.canvas_frame, command=self.data_canvas.yview, orient="vertical")
        self.main_scroll.pack(side="right", fill="y")
        self.data_canvas.config(yscrollcommand=self.main_scroll.set)

        self.data_main = tk.Frame(self.data_canvas)
        self.data_main.bind("<Configure>", self._update_scrollregion)
        self.data_canvas.create_window((0, 0), window=self.data_main, anchor="nw")
        
        #  Bind an update of the scroll area of the container for the DataFrame(s). Makes scrolling work
        self.data_canvas.bind("<Configure>",
                              lambda e: self.data_canvas.configure(scrollregion=self.data_canvas.bbox("all")))

        # Layout: Left side Frame MENU BUTTONS
        open_button = self.obj.PressReleaseButton(self.side_frame, "Open file").create()
        open_button.pack(padx=5, pady=10)
        self.read_button = self.obj.DisabledButton(self.side_frame, "Read only").create()
        self.read_button.pack(pady=5, ipady=5)
        self.write_button = self.obj.DisabledButton(self.side_frame, "Write").create()
        self.write_button.pack(pady=5, ipady=5)
        self.delete_button = self.obj.DisabledButton(self.side_frame, "Delete").create()
        self.delete_button.pack(pady=5, ipady=5)
        self.edit_button = self.obj.DisabledButton(self.side_frame, "Edit").create()
        self.edit_button.pack(pady=5, ipady=5)
        self.search_button = self.obj.DisabledButton(self.side_frame, "Search").create()
        self.search_button.pack(pady=5, ipady=5)
        quit_button = self.obj.PressReleaseButton(self.side_frame, "Quit").create()
        quit_button.pack(pady=10)

        # Layout: top_frame children
        # Ops Frame 1
        self.ops_frame1 = tk.Frame(self.top_frame)
        self.ops_frame1.pack(fill="x")

        self.file_str = tk.StringVar(self.ops_frame1, "No file loaded")  # Display filename
        self.filename_rep = tk.Label(self.ops_frame1, textvariable=self.file_str)
        self.filename_rep.grid(row=0, column=0, ipady=10, sticky="w")
        self.tables_drop_var = tk.StringVar(self.ops_frame1, "Select table")
        self.tables_drop_var.trace_add("write", self.table_select)  # Tracer for updating and sorting tables
        self.tables_dropdown = tk.OptionMenu(self.ops_frame1, self.tables_drop_var, *self.tables_names)
        self.tables_dropdown["state"] = "disabled"
        self.tables_dropdown.grid(row=0, column=1, padx=5, sticky="w")

        # Ops Frame 2
        self.ops_frame2 = tk.Frame(self.top_frame)
        self.ops_frame2.pack(fill="x")

        self.entry_label_str = tk.StringVar(self.ops_frame2, "N/A")
        self.entry_label = tk.Label(self.ops_frame2, width=20, textvariable=self.entry_label_str, anchor="e",
                                    state="disabled", padx=15, pady=5)
        self.entry_label.grid(row=0, column=0)
        self.edit_drop_var = tk.StringVar(self.ops_frame2, '')
        self.edit_drop_var.trace("w", self.edit_drop_trace)
        self.edit_dropdown = tk.OptionMenu(self.ops_frame2, self.edit_drop_var, *self.headers)
        self.entry_field = tk.Entry(self.ops_frame2, width=31, state="disabled")
        self.entry_field.grid(row=0, column=1, pady=5)
        self.ok_button = self.obj.OkButton(self.ops_frame2, "OK").create()
        self.ok_button.grid(row=0, column=2, padx=15, sticky="ew")

        # Ops Frame 3
        self.ops_frame3 = tk.Frame(self.top_frame)
        self.ops_frame3.pack(fill="x")

        self.preview_string = tk.StringVar(self.ops_frame3, " \n ")
        self.preview = tk.Label(self.ops_frame3, anchor=tk.CENTER, textvariable=self.preview_string)
        self.preview.pack()

        # Ops Frame 4
        self.ops_frame4 = tk.Frame(self.top_frame)
        self.ops_frame4.pack(anchor="center")

        self.search_single = self.obj.MyButton(self.ops_frame4, "Single table").create()
        self.search_all = self.obj.MyButton(self.ops_frame4, "All tables").create()
        self.execute_button = self.obj.ExecuteButton(self.ops_frame4, "Commit").create()
        self.execute_button.pack()

        # Initial click-bindings
        open_button.bind("<ButtonRelease-1>", self.click_open, add="+")
        quit_button.bind("<Button-1>", self.bf.click_down)
        quit_button.bind("<ButtonRelease-1>", self.quit_click)

    # Program operations
    def click_open(self, _):
        """Loading a db file and create dropdown menu. Open the first table and activate menu"""
        for button in [self.read_button, self.write_button, self.delete_button, self.edit_button, self.search_button]:
            button.config(**self.unselected)
            self.bf.disable(button)
        self.file_str.set("No file loaded")
        for widget in self.data_frames:
            widget.destroy()
        try:
            self.f_path = open_file(title='Open database', filetypes=(('database files', '*.db'), ('All files', '*.*')))
            self.tables_names = self.sql.fetch_tablenames(self.f_path)  # Fetches list of table names from the database
            try:
                self.tables_dropdown.destroy()
                self.tables_dropdown = tk.OptionMenu(self.ops_frame1, self.tables_drop_var, *self.tables_names)
                self.tables_dropdown.grid(row=0, column=1, padx=5, sticky="w")
                self.file_str.set(f'{basename(self.f_path)} /')

                # Set Show/hide widgets to default states
                for button in [self.read_button, self.write_button, self.delete_button, self.edit_button,
                               self.search_button]:
                    button.config(**self.unselected)
                    self.bf.enable(button)

                self.read_button.bind("<Button-1>", self.read_click)
                self.write_button.bind("<Button-1>", self.write_click)
                self.delete_button.bind("<Button-1>", self.delete_click)
                self.edit_button.bind("<Button-1>", self.edit_click)
                self.search_button.bind("<Button-1>", self.search_click)
                self.search_single.bind("<Button-1>", self.search_mode)
                self.search_all.bind("<Button-1>", self.search_mode)

                self.tables_drop_var.set(f"{self.tables_names[0]}")  # TRACE triggers "table_select()"

            except IndexError or TypeError:
                pass
        except ValueError or FileNotFoundError:
            pass

    def table_select(self, *_):
        self.table_i = self.tables_names.index(self.tables_drop_var.get())  # Get table's index in tables_names list
        self.shared_states.set_sort(0)  # Set sorting to default.
        self.headers, self.data = self.sql.open_table(self.f_path, self.tables_names[self.table_i])  # Fetch data
        self.read_click(_)

    def _operation_reset(self):
        """When clicking write, delete, edit or search buttons, this runs"""
        for frame in self.data_frames:
            frame.destroy()
        # Search mode buttons
        self.shared_states.search_all = False
        for button in [self.search_single, self.search_all]:
            button.pack_forget()
            button.config(**self.unselected)
        self.data_frames.append(DataFrame(self.data_main, self.tables_names[self.table_i], self.headers, self.data, self.shared_states))
        # Menu button states
        for button in [self.read_button, self.write_button, self.delete_button, self.edit_button, self.search_button]:
            button.config(**self.unselected)

        for widget in [self.edit_dropdown]:
            widget.grid_forget()
        self.entry_label.grid(row=0, column=0)

        self.ok_button.grid(row=0, column=2, padx=15, sticky="ew")
        self.bf.enable(self.ok_button)
        self.bf.disable(self.execute_button)

        # Reset variables
        self.current_row = [] * len(self.headers)
        self.preview_string.set(" \n ")
        self.entry_i = 0

        for widget in [self.entry_label, self.entry_field]:
            widget["state"] = "normal"
        self.entry_field.delete(0, "end")
        self.entry_field.insert(0, "")

    def read_click(self, _):
        self._operation_reset()
        self.read_button.config(**self.selected)
        self.entry_label_str.set("N/A")
        self.execute_button["text"] = "Commit"
        for widget in [self.entry_label, self.entry_field, self.ok_button, self.execute_button]:
            self.bf.disable(widget)

    def write_click(self, _):
        """When selecting 'Write Row'"""
        self._operation_reset()
        self.write_button.config(**self.selected)

        # Write operations
        self.current_row = []  # Prepare current_row for preview display in write_ok method
        self.entry_i = 1  # Skip index 0 since RowId is generated by sqlite when writing to file.
        self.entry_label_str.set(f"Input {self.headers[self.entry_i]}:")
        self.ok_button.bind("<Button-1>", self.write_ok)
        self.execute_button.config(text="Commit row")

    def write_ok(self, _):
        """Add points of data to new row before committing it to file"""
        try:  # Try to add as int...
            user_input = int(self.entry_field.get())
            self.current_row.append(user_input)
        except ValueError:  # ... or defer to string
            user_input = str(self.entry_field.get())
            self.current_row.append(user_input.strip())

        # Format lengths of headers/data to be displayed in the preview Message
        formatted_headers, formatted_data, self.form_width = self.sql.output_formatted(
            self.headers[1:len(self.current_row) + 1], [self.current_row])
        self.preview_string.set(f"{formatted_headers}\n{formatted_data}")
        # Empty entry field
        self.entry_field.delete(0, "end")
        self.entry_field.insert(0, "")

        try:  # Go to next index of self.headers
            self.entry_i += 1
            self.entry_label_str.set(f"Input {self.headers[self.entry_i]}:")
        except IndexError:  # Done: Change widget states and enable execute_button for writing
            self.entry_label_str.set("N/A")
            self.entry_field.delete(0, "end")
            for widget in [self.ok_button, self.entry_label, self.entry_field]:
                self.bf.disable(widget)
            self.bf.enable(self.execute_button)
            self.execute_button.bind("<Button-1>", self.write_exe)

    def write_exe(self, _):
        """Commit new row of data to table."""
        # Compile data in a dict and write to file
        # self.current_row.pop(0)  # Remove first object in list, reserved for RowId, which is not used when writing.
        new_data = DataRow(self.headers[1:], self.current_row).compile_data()
        self.sql.write_row(self.f_path, self.tables_names[self.table_i], new_data)
        self.headers, self.data = self.sql.open_table(self.f_path, self.tables_names[self.table_i])
        self.write_click(_)

    def delete_click(self, _):
        """When selecting 'Delete Row'"""
        self._operation_reset()
        self.delete_button.config(**self.selected)

        self.entry_label_str.set(f"Select Id:")
        self.ok_button.bind("<Button-1>", self.delete_ok)
        self.execute_button.config(text="Confirm delete")

    def delete_ok(self, _):
        """Fetches a row based on first column ("ID") and asks for confirmation to delete it"""
        self.bf.disable(self.execute_button)
        try:
            self.entry_i = int(self.entry_field.get())
            for i in range(len(self.data)):
                if self.entry_i == self.data[i][0]:
                    self.current_row = self.data[i]
                    formatted_headers, formatted_data, self.form_width = self.sql.output_formatted(
                        self.headers, [self.current_row])
                    self.preview_string.set(f"{formatted_headers}\n{formatted_data}")
                    self.bf.enable(self.execute_button)
                    self.execute_button.bind("<Button-1>", self.delete_exe)
                    break
                else:
                    self.preview_string.set(f"Id not found: {self.entry_i}\n ")

            self.entry_field.delete(0, "end")
            self.entry_field.insert(0, "")
        except ValueError or sqlite3.OperationalError:
            self.preview_string.set(f"Invalid Id: {self.entry_field.get()}\n ")

    def delete_exe(self, _):
        """Deletes the selected row from the table"""
        self.sql.delete_row(self.f_path, self.tables_names[self.table_i], self.current_row[0])

        self.headers, self.data = self.sql.open_table(self.f_path, self.tables_names[self.table_i])
        self.delete_click(_)

    def edit_click(self, _):
        """When selecting 'Edit Row'"""
        self._operation_reset()
        self.edit_button.config(**self.selected)

        self.entry_label_str.set(f"Select Id:")
        self.execute_button.config(text="Confirm edit")
        self.ok_button.bind("<Button-1>", self.edit_ok)

    def edit_ok(self, _):
        """Selects ID and creates dropdown chooser, then accepts new data to replace selected data"""
        if len(self.entry_label_str.get()) > 0:
            try:  # Try for integer
                self.entry_i = int(self.entry_field.get())
                if self.entry_i in [row[0] for row in self.data]:  # Check if entry is among existing rows' "ID"
                    for row in self.data:
                        if self.entry_i == row[0]:
                            self.current_row = row
                            formatted_headers, formatted_data, self.form_width = self.sql.output_formatted(
                                self.headers, [self.current_row])
                            self.preview_string.set(f"{formatted_headers}\n{formatted_data}")
                            # Create dropdown menu and hide entry field
                            self.entry_label_str.set("")
                            self.entry_label.grid_forget()
                            self.edit_drop_var.set(self.headers[1])
                            self.edit_dropdown = tk.OptionMenu(self.ops_frame2, self.edit_drop_var, *self.headers[1:])
                            self.edit_dropdown.config(width=16)
                            self.edit_dropdown.grid(row=0, column=0, padx=19, sticky="e")
                            # Update widget states
                            self.entry_field.delete(0, "end")
                            self.entry_field.insert(0,
                                                    f"{self.current_row[self.headers.index(self.edit_drop_var.get())]}")
                else:
                    self.preview_string.set(f"""Id not found: "{self.entry_i}"\n """)
            except ValueError or sqlite3.OperationalError:
                self.preview_string.set(f"""Invalid input: "{self.entry_field.get()}"\n """)
        else:
            # Save any and all changes made to variables and to display string.
            self.current_row[self.headers.index(self.edit_drop_var.get())] = self.entry_field.get()
            formatted_headers, formatted_data, self.form_width = self.sql.output_formatted(self.headers,
                                                                                           [self.current_row])
            self.preview_string.set(f"{formatted_headers}\n{formatted_data}")
            # Update widgets
            self.entry_field.delete(0, "end")
            self.entry_field.insert(0, "")
            self.bf.enable(self.execute_button)
            self.execute_button.bind("<Button-1>", self.edit_execute)

    def edit_drop_trace(self, *_):
        # Inserts the data you want to edit into the entry field.
        self.entry_field.delete(0, "end")
        self.entry_field.insert(0, f"{self.current_row[self.headers.index(self.edit_drop_var.get())]}")

    def edit_execute(self, _):
        # Compile data in a dict and use to replace the same ID/RowId in the file.
        self.headers[0] = 'rowid'  # re-named for writing to file.
        new_data = DataRow(self.headers, self.current_row).compile_data()
        self.sql.edit_row(self.f_path, self.tables_names[self.table_i], self.entry_i, new_data)

        self.headers, self.data = self.sql.open_table(self.f_path, self.tables_names[self.table_i])
        self.edit_click(_)

    def search_click(self, _):
        """When selecting 'Search'"""
        self._operation_reset()
        _.widget.config(**self.selected)

        # Widget settings
        self.entry_label["state"] = "normal"
        self.entry_field["state"] = "normal"
        self.entry_label_str.set(f"Enter search phrase: ")
        self.execute_button.config(text="Search")

        # Remove Ok button, display search options
        self.ok_button.grid_forget()
        self.execute_button.pack_forget()
        self.search_single.pack(side="left")
        self.execute_button.pack(side="left", padx=5)
        self.search_all.pack(side="left")

    def search_mode(self, _):
        for button in [self.search_single, self.search_all]:
            button.config(**self.unselected)
        _.widget.config(**self.selected)

        if _.widget.cget("text") == 'Single table':
            self.shared_states.search_all = False
        else:
            self.shared_states.search_all = True

        self.bf.enable(self.execute_button)
        self.execute_button.bind("<Button-1>", self.search_execute)

    def search_execute(self, _):
        for frame in self.data_frames:
            frame.destroy()

        if self.shared_states.search_all is False:  # Searching selected table
            self.data_frames.append(self.search_function(self.table_i))
        else:
            for i in range(len(self.tables_names)):  # Searching ALL tables
                self.data_frames.append(self.search_function(i))

    def search_function(self, i):
        # Function for searching a table
        search_phrase = self.entry_field.get()
        search_result = []

        headers, data_rows = self.sql.open_table(self.f_path, self.tables_names[i])
        for row in data_rows:
            for data in row:  # Check item by item in list
                if search_phrase.lower() in str(data).lower():  # Check for search phrase
                    search_result.append(row)  # Add to search result data
                    break  # Move on to next row, to not add the same row because if hit on multiple items
        self.preview_string.set(" \n ")
        # Finally, create a table with the search results.
        return DataFrame(self.data_main, self.tables_names[i], headers, search_result, self.shared_states)

    def _update_scrollregion(self, _):
        """Updates Data Main's scroll region after making multiple tables search"""
        self.data_canvas.configure(scrollregion=self.data_canvas.bbox("all"))

    def quit_click(self, _):
        self.destroy()


if __name__ == '__main__':
    screen = Main()
    screen.mainloop()
