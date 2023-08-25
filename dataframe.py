import tkinter as tk

from support_classes import AutoScrollbar
import sql_functions
import button_functions


class DataFrame(tk.Frame):
    """Class containing data table display"""
    def __init__(self, master, table_name, headers, data, shared_states):
        super().__init__(master)

        # Imports
        self.sql = sql_functions.SupportFunctions  # Import my SQL functions
        self.obj = button_functions  # Import my buttons and general button functions
        self.bf = button_functions.ButtonFunctions()  # Import button functions
        self.shared_states = shared_states

        # Variables
        self.table_name, self.headers, self.data, self.form_width, self.shared_states = table_name, headers, data, [0], shared_states

        # Layout: Data Sorter Frame widgets; LABEL, SORTER DROPDOWN
        sorter_frame = tk.Frame(self, bd=1, relief="raised")
        sorter_head_var = tk.StringVar(sorter_frame)
        sorter_head_var.set(f"{self.table_name}, Sort by:")
        sorter_head = tk.Label(sorter_frame, textvariable=sorter_head_var)

        try:
            self.sort_drop_choice = tk.StringVar(sorter_frame, self.headers[self.shared_states.get_sort()])
        except IndexError:
            self.shared_states.set_sort(0)
            self.sort_drop_choice = tk.StringVar(sorter_frame, self.headers[0])
        self.sort_drop_choice.trace("w", self.sorter_select)
        sort_dropdown = tk.OptionMenu(sorter_frame, self.sort_drop_choice, *self.headers)

        sorter_frame.grid(row=0, column=0, sticky="nwe")
        sorter_head.pack(side="left", padx=5, anchor="nw")
        sort_dropdown.pack(side="left", anchor="nw")

        # Layout: Data widgets; TABLE HEADERS, TABLE DATA ROWS, SCROLLBARS
        self.data_headers = tk.Text(self, height=1, wrap="none", bd=1, relief="raised")
        self.data_text = tk.Text(self, wrap="none", bd=1, relief="raised")
        self.data_headers.grid(row=1, column=0, sticky="nwe")
        self.data_text.grid(row=2, column=0, sticky="nwe")
        data_scroll_y = AutoScrollbar(self, width=6, command=self.data_text.yview, orient='vertical')
        data_scroll_x = AutoScrollbar(self, width=6, command=self.dual_scroll, orient='horizontal')
        data_scroll_y.grid(row=1, rowspan=2, column=1, sticky='nsew')
        data_scroll_x.grid(row=3, column=0, sticky='nsew')
        self.data_headers['xscrollcommand'] = data_scroll_x.set
        self.data_text['xscrollcommand'] = data_scroll_x.set
        self.data_text['yscrollcommand'] = data_scroll_y.set

        self.sort_and_display(self.shared_states.get_sort())

    def dual_scroll(self, *_):
        """scrolls both text-boxes at once"""
        self.data_headers.xview(*_)
        self.data_text.xview(*_)

    def sorter_select(self, *_):
        sort_i = self.headers.index(self.sort_drop_choice.get())  # Get sorting index by text from dropdown
        self.shared_states.set_sort(sort_i)  # Stores the sorting selection in the main shared_state object.
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
            if self.shared_states.search_all:
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