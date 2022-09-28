"""
Programmering 2 redovisningsprojekt, uppdaterad

OBS! På äppeldatorer, ändra typsnittsstorlek (rad 148) från 11 till 14.

Kör filen sql_functions.py separat för att skapa två exempel-filer med tabeller.

/Johannes
"""


import sqlite3
import tkinter as tk
from tkinter import font  # For setting font globally
from tkinter.filedialog import askopenfilename as open_file
from os.path import basename  # Display filename without file-path

import sql_functions
import button_functions


class DataRow:
    """Class for storing a set of headers and data"""
    def __init__(self, headers, data):
        self.data_dict = {headers[i]: data[i] for i in range(len(headers))}

    def compile_data(self):
        return self.data_dict


class AutoScrollbar(tk.Scrollbar):
    """Scrollbar that appears only when its area is scrollable"""
    
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
            self.grid_forget()
        else:
            try:
                self.grid()
            except Exception as e:  # Defaults to grid if pack doesn't work
                self.pack(side="right", fill="y")

        tk.Scrollbar.set(self, lo, hi)


class DataFrame(tk.Frame):
    """Class containing data table display"""
    def __init__(self, master, table_name, headers, data, sort_i):
        super().__init__(master)

        # Imports
        self.sql = sql_functions.SupportFunctions  # Import my SQL functions
        self.obj = button_functions  # Import my buttons and general button functions
        self.bf = button_functions.ButtonFunctions()  # Import button functions

        # Variables
        self.table_name, self.headers, self.data, self.form_width = table_name, headers, data, [0]

        # Layout: Data Sorter Frame widgets; LABEL, SORTER DROPDOWN
        self.sorter_frame = tk.Frame(self, bd=1, relief="raised")
        self.sorter_head_var = tk.StringVar(self.sorter_frame)
        self.sorter_head_var.set(f"{self.table_name}, Sort by:")
        self.sorter_head = tk.Label(self.sorter_frame, textvariable=self.sorter_head_var)
        self.sort_drop_choice = tk.StringVar(self.sorter_frame, self.headers[sort_i])
        self.sort_drop_choice.trace("w", self.sorter_select)
        self.sort_dropdown = tk.OptionMenu(self.sorter_frame, self.sort_drop_choice, *self.headers)

        self.sorter_frame.grid(row=0, column=0, sticky="nwe")
        self.sorter_head.pack(side="left", padx=5, anchor="nw")
        self.sort_dropdown.pack(side="left", anchor="nw")

        # Layout: Data widgets; TABLE HEADERS, TABLE DATA ROWS, SCROLLBARS
        self.data_headers = tk.Text(self, height=1, wrap="none", bd=1, relief="raised")
        self.data_text = tk.Text(self, wrap="none", bd=1, relief="raised")
        self.data_headers.grid(row=1, column=0, sticky="nwe")
        self.data_text.grid(row=2, column=0, sticky="nwe")
        self.data_scroll_y = AutoScrollbar(self, width=6, command=self.data_text.yview, orient='vertical')
        self.data_scroll_x = AutoScrollbar(self, width=6, command=self.dual_scroll, orient='horizontal')
        self.data_scroll_y.grid(row=1, rowspan=2, column=1, sticky='nsew')
        self.data_scroll_x.grid(row=3, column=0, sticky='nsew')
        self.data_headers['xscrollcommand'] = self.data_scroll_x.set
        self.data_text['xscrollcommand'] = self.data_scroll_x.set
        self.data_text['yscrollcommand'] = self.data_scroll_y.set

        self.sort_and_display(sort_i)

    def dual_scroll(self, *_):
        """scrolls both text-boxes at once"""
        self.data_headers.xview(*_)
        self.data_text.xview(*_)

    def sorter_select(self, *_):
        sort_i = self.headers.index(self.sort_drop_choice.get())  # Get sorting index by text from dropdown
        Main.sort_i = sort_i  # Returns class sort_i to "Main" so that sorting is kept when clicking menu buttons
        self.sort_and_display(sort_i)

    def sort_and_display(self, sort_i, *_):
        """When selecting a header in the sorter dropdown menu, loading a file, or committing changes to a table"""

        # Get sorting index, return it to Main class so that sorting is kept when switching between operations
        if self.data:
            # Sort and format rows of data
            sorted_data = sorted(self.data, key=lambda x: x[sort_i])  # sort the data rows by the index
            formatted_headers, formatted_data, self.form_width = self.sql.output_formatted(self.headers, sorted_data)

            # Update texts for data headers and data table
            for widget in [self.data_headers, self.data_text]:
                widget.config(state="normal")
                widget.delete('1.0', "end")
            self.data_headers.insert('1.0', formatted_headers)
            self.data_text.insert('1.0', formatted_data)

            # Limit width/height of data_table and headers to enable scrolling
            height = len(self.data) + 1
            if screen.search_toggle:
                if height > 15:
                    height = 15
            else:
                if height > 20:
                    height = 20
            self.data_text.config(height=height)

            # Change bg-color for every other row of data
            last_line = self.data_text.index("end").split(".")[0]
            tag = "odd"
            for i in range(1, int(last_line)):
                self.data_text.tag_add(tag, "%s.0" % i, "%s.0" % (i + 1))
                tag = "even" if tag == "odd" else "odd"
            self.data_text.tag_configure("odd", background="white")
            for text_box in [self.data_headers, self.data_text]:
                text_box.config(state="disabled")

        self.pack(side="top", fill="both", expand=True, anchor="nw")  # Packs class object data frame


class Main(tk.Tk):
    """Class containing base gui elements and operational functions"""
    def __init__(self):
        super().__init__()
        self.geometry('900x600+250+100')
        self.title('SQL Database (Johannes Överland)')
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

        # Variables
        self.f_path = ""
        self.headers, self.data, self.form_width = ["placeholder"], [["placeholder"]], []
        self.tables_names = ["placeholder"]  # Used for generating table selection buttons
        self.table_i = 0  # Keeping track of which table is currently selected.
        self.sort_i = 0
        self.current_row = []  # Container for list to send for writing to sql table
        self.entry_i = 0  # Index used for user input selections and/or iterations.
        self.search_toggle = False  # For selecting search modes False or True, "single" or "all", respectively
        self.display_data = [self.tables_names[self.table_i], self.headers, self.data]
        self.data_frames = []  # Container for addressing data frames for  removal

        # Layout: Root level Frames
        self.screen = tk.Frame(self)
        self.screen.pack(fill="both", padx=5, pady=5, expand=True)

        # Layout: Screen Frame
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

        # Layout: Side Frame MENU BUTTONS
        self.open_button = self.obj.PressReleaseButton(self.side_frame, "Open file").create()
        self.open_button.pack(padx=5, pady=10)
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
        self.quit_button = self.obj.PressReleaseButton(self.side_frame, "Quit").create()
        self.quit_button.pack(pady=10)

        # Layout: Top Frame children
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
        self.open_button.bind("<ButtonRelease-1>", self.click_open, add="+")
        self.quit_button.bind("<Button-1>", self.bf.click_down)
        self.quit_button.bind("<ButtonRelease-1>", self.quit_click)

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
        self.sort_i = 0
        self.headers, self.data = self.sql.open_table(self.f_path, self.tables_names[self.table_i])  # Fetch data
        self.read_click(_)

    def _operation_reset(self):
        """When clicking write, delete, edit or search buttons, this runs"""
        for frame in self.data_frames:
            frame.destroy()
        # Search mode buttons
        self.search_toggle = False
        for button in [self.search_single, self.search_all]:
            button.pack_forget()
            button.config(**self.unselected)
        self.data_frames.append(DataFrame(self.data_main, self.tables_names[self.table_i], self.headers, self.data,
                                          self.sort_i))
        # Menu button states
        for button in [self.read_button, self.write_button, self.delete_button, self.edit_button,
                       self.search_button]:
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
            self.search_toggle = False
        else:
            self.search_toggle = True

        self.bf.enable(self.execute_button)
        self.execute_button.bind("<Button-1>", self.search_execute)

    def search_execute(self, _):
        for frame in self.data_frames:
            frame.destroy()

        if self.search_toggle is False:  # Searching selected table
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
        return DataFrame(self.data_main, self.tables_names[i], headers, search_result, self.sort_i)

    def _update_scrollregion(self, _):
        """Updates Data Main's scroll region after making multiple tables search"""
        self.data_canvas.configure(scrollregion=self.data_canvas.bbox("all"))

    @staticmethod
    def quit_click(_):
        screen.destroy()


if __name__ == '__main__':
    screen = Main()
    screen.mainloop()
