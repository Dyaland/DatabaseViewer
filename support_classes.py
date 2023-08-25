import tkinter as tk


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


class SharedStates:
    """Keeps track of preferences between instances."""
    
    def __init__(self):
        self.sort_i = 0  # Sorting selection by column index.
        self.search_all = False  # False for single table searhc, True for all tables search.

    def set_sort(self, sort_i):
        self.sort_i = sort_i

    def get_sort(self):
        return self.sort_i


class DataRow:
    """Class for storing a set of headers and data when inputing new data or editing an existing row."""

    def __init__(self, headers: list, data: list):
        self.data_dict = {headers[i]: data[i] for i in range(len(headers))}

    def compile_data(self):
        return self.data_dict
