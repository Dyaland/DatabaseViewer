import sqlite3


class SupportFunctions:
    """SQL functions for dB reader lite"""

    def __init__(self):
        """Pre-made tables data"""
        self.initial_people = (
            ('Airi', 'Satou', 'Accountant', 'Tokyo', 162700),
            ('Angelica', 'Ramos', 'Chief Executive Officer (CEO)', 'London', 1200000),
            ('Ashton', 'Cox', 'Junior Technical Author', 'San Francisco', 86000),
            ('Bradley', 'Greer', 'Software Engineer', 'London', 132000),
            ('Brenden', 'Wagner', 'Software Engineer', 'San Francisco', 206850),
            ('Brielle', 'Williamson-Hurlington', 'Senior Integration Specialist', 'New York', 372000),
            ('Bruno', 'Nash', 'Software Engineer', 'London', 163500),
            ('Caesar', 'Vance', 'Pre-Sales Support', 'New York', 106450),
            ('Cara', 'Stevens', 'Sales Assistant', 'New York', 145600),
            ('Cedric', 'Kelly', 'Senior Javascript Developer', 'Edinburgh', 433060),
            ('Charde', 'Marshall', 'Regional Director', 'San Francisco', 470600),
            ('Colleen', 'Hurst', 'Javascript Developer', 'San Francisco', 205500),
            ('Dai', 'Rios', 'Personnel Lead', 'Edinburgh', 217500),
            ('Donna', 'Snider', 'Customer Support', 'New York', 112000),
            ('Doris', 'Wilder', 'Sales Assistant', 'Sydney', 85600),
            ('Finn', 'Camacho', 'Support Engineer', 'San Francisco', 87500),
            ('Fiona', 'Green', 'Chief Operating Officer (COO)', 'San Francisco', 850000),
            ('Garrett', 'Winters', 'Accountant', 'Tokyo', 170750),
            ('Gavin', 'Cortez', 'Team Leader', 'San Francisco', 235500),
            ('Gavin', 'Joyce', 'Developer', 'Edinburgh', 92575),
            ('Gloria', 'Little', 'Systems Administrator', 'New York', 237500),
            ('Haley', 'Kennedy', 'Senior Marketing Designer', 'London', 313500),
            ('Hermione', 'Butler', 'Regional Director', 'London', 356250),
            ('Herrod', 'Chandler', 'Sales Assistant', 'San Francisco', 137500),
            ('Hope', 'Fuentes', 'Secretary', 'San Francisco', 109850),
            ('Howard', 'Hatfield', 'Office Manager', 'San Francisco', 164500),
            ('Jackson', 'Bradshaw', 'Director', 'New York', 645750),
            ('Jena', 'Gaines', 'Office Manager', 'London', 90560),
            ('Jenette', 'Caldwell', 'Development Lead', 'New York', 345000),
            ('Jennifer', 'Acosta', 'Junior Javascript Developer', 'Edinburgh', 75650),
            ('Jennifer', 'Chang', 'Regional Director', 'Singapore', 357650),
            ('Jonas', 'Alexander', 'Developer', 'San Francisco', 86500),
            ('Lael', 'Greer', 'Systems Administrator', 'London', 103500),
            ('Martena', 'Mccray', 'Post-Sales support', 'Edinburgh', 324050),
            ('Michael', 'Bruce', 'Javascript Developer', 'Singapore', 183000),
            ('Michael', 'Silva', 'Marketing Designer', 'London', 198500),
            ('Michelle', 'House', 'Integration Specialist', 'Sydney', 95400),
            ('Olivia', 'Liang', 'Support Engineer', 'Singapore', 234500),
            ('Paul', 'Byrd', 'Chief Financial Officer (CFO)', 'New York', 725000),
            ('Prescott', 'Bartlett', 'Technical Author', 'London', 145000),
            ('Quinn', 'Flynn', 'Support Lead', 'Edinburgh', 342000),
            ('Rhona', 'Davidson', 'Integration Specialist', 'Tokyo', 327900),
            ('Sakura', 'Yamamoto', 'Support Engineer', 'Tokyo', 139575),
            ('Serge', 'Baldwin', 'Data Coordinator', 'Singapore', 138575),
            ('Shad', 'Decker', 'Regional Director', 'Edinburgh', 183000),
            ('Shou', 'Itou', 'Regional Marketing', 'Tokyo', 163000),
            ('Sonya', 'Frost', 'Software Engineer', 'Edinburgh', 103600),
            ('Suki', 'Burks', 'Developer', 'London', 114500),
            ('Tatyana', 'Fitzpatrick', 'Regional Director', 'London', 385750),
            ('Thor', 'Walton', 'Developer', 'New York', 98540),
            ('Tiger', 'Nixon', 'System Architect', 'Edinburgh', 320800),
            ('Timothy', 'Mooney', 'Office Manager', 'London', 136200),
            ('Unity', 'Butler', 'Marketing Designer', 'San Francisco', 85675),
            ('Vivian', 'Harrell', 'Financial Controller', 'San Francisco', 452500),
            ('Yuri', 'Berry', 'Chief Marketing Officer (CMO)', 'New York', 675000),
            ('Zenaida', 'Frank', 'Software Engineer', 'New York', 125250),
            ('Zorita', 'Serrano', 'Software Engineer', 'San Francisco', 115000),
        )
        self.office_supplies = (
            ('1/6/2020', 'East', 'Jones', 'Pencil', '95', '1.99', '189.05'),
            ('1/23/2020', 'Central', 'Kivell', 'Binder', '50', '19.99', '999.5'),
            ('2/9/2020', 'Central', 'Jardine', 'Pencil', '36', '4.99', '179.64'),
            ('2/26/2020', 'Central', 'Gill', 'Pen', '27', '19.99', '539.73'),
            ('3/15/2020', 'West', 'Sorvino', 'Pencil', '56', '2.99', '167.44'),
            ('4/1/2020', 'East', 'Jones', 'Binder', '60', '4.99', '299.4'),
            ('4/18/2020', 'Central', 'Andrews', 'Pencil', '75', '1.99', '149.25'),
            ('5/5/2020', 'Central', 'Jardine', 'Pencil', '90', '4.99', '449.1'),
            ('5/22/2020', 'West', 'Thompson', 'Pencil', '32', '1.99', '63.68'),
            ('6/8/2020', 'East', 'Jones', 'Binder', '60', '8.99', '539.4'),
            ('6/25/2020', 'Central', 'Morgan', 'Pencil', '90', '4.99', '449.1'),
            ('7/12/2020', 'East', 'Howard', 'Binder', '29', '1.99', '57.71'),
            ('7/29/2020', 'East', 'Parent', 'Binder', '81', '19.99', '1,619.19'),
            ('8/15/2020', 'East', 'Jones', 'Pencil', '35', '4.99', '174.65'),
            ('9/1/2020', 'Central', 'Smith', 'Desk', '2', '125', '250'),
            ('9/18/2020', 'East', 'Jones', 'Pen Set', '16', '15.99', '255.84'),
            ('10/5/2020', 'Central', 'Morgan', 'Binder', '28', '8.99', '251.72'),
            ('10/22/2020', 'East', 'Jones', 'Pen', '64', '8.99', '575.36'),
            ('11/8/2020', 'East', 'Parent', 'Pen', '15', '19.99', '299.85'),
            ('11/25/2020', 'Central', 'Kivell', 'Pen Set', '96', '4.99', '479.04'),
            ('12/12/2020', 'Central', 'Smith', 'Pencil', '67', '1.29', '86.43'),
            ('12/29/2020', 'East', 'Parent', 'Pen Set', '74', '15.99', '1,183.26'),
            ('1/15/2021', 'Central', 'Gill', 'Binder', '46', '8.99', '413.54'),
            ('2/1/2021', 'Central', 'Smith', 'Binder', '87', '15', '1,305.00'),
            ('2/18/2021', 'East', 'Jones', 'Binder', '4', '4.99', '19.96'),
            ('3/7/2021', 'West', 'Sorvino', 'Binder', '7', '19.99', '139.93'),
            ('3/24/2021', 'Central', 'Jardine', 'Pen Set', '50', '4.99', '249.5'),
            ('4/10/2021', 'Central', 'Andrews', 'Pencil', '66', '1.99', '131.34'),
            ('4/27/2021', 'East', 'Howard', 'Pen', '96', '4.99', '479.04'),
            ('5/14/2021', 'Central', 'Gill', 'Pencil', '53', '1.29', '68.37'),
            ('5/31/2021', 'Central', 'Gill', 'Binder', '80', '8.99', '719.2'),
            ('6/17/2021', 'Central', 'Kivell', 'Desk', '5', '125', '625'),
            ('7/4/2021', 'East', 'Jones', 'Pen Set', '62', '4.99', '309.38'),
            ('7/21/2021', 'Central', 'Morgan', 'Pen Set', '55', '12.49', '686.95'),
            ('8/7/2021', 'Central', 'Kivell', 'Pen Set', '42', '23.95', '1,005.90'),
            ('8/24/2021', 'West', 'Sorvino', 'Desk', '3', '275', '825'),
            ('9/10/2021', 'Central', 'Gill', 'Pencil', '7', '1.29', '9.03'),
            ('9/27/2021', 'West', 'Sorvino', 'Pen', '76', '1.99', '151.24'),
            ('10/14/2021', 'West', 'Thompson', 'Binder', '57', '19.99', '1,139.43'),
            ('10/31/2021', 'Central', 'Andrews', 'Pencil', '14', '1.29', '18.06'),
            ('11/17/2021', 'Central', 'Jardine', 'Binder', '11', '4.99', '54.89'),
            ('12/4/2021', 'Central', 'Jardine', 'Binder', '94', '19.99', '1,879.06'),
            ('12/21/2021', 'Central', 'Andrews', 'Binder', '28', '4.99', '139.72'),
        )
        self.initial_students = (
            ('Elina', 42, 'ENA', 'Lyckselevägen 137'),
            ('Sigurd', 28, 'ENI, FRI', 'Smidesvägen 12A'),
            ('Elis', 23, 'PYI, SPA, BII', 'Trädmästargatan 60'),
            ('Johannes', 37, 'PYI', 'Fruktvägen 76'),
            ('Sahba', 31, 'PYI, FRI', 'Färjevägen 38'),
            ('Sami', 43, 'PYI, RUI', 'Bredgatan 2'),
            ('Amal', 24, 'SPI, FRI, BII', 'Kävlingevägen 7'),
            ('Curt', 29, 'RUI', 'Ugglestigen 1'),
            ('Karin', 39, 'SPI, FRI', 'Huvudgatan 42'),
            ('Loke', 22, 'ENA, SPI, BII', 'Odengatan 9'),
            ('Agnes', 54, 'FRI', 'Härförarvägen 68'),
            ('Unni', 33, 'SPA, RUI', 'Torget 7'),
            ('Harald', 24, 'SPI, FRI', 'Storgatan 7'),
        )
        self.initial_courses = (
            ('English Introductory', 'ENI', 'FRP'),
            ('English Advanced', 'ENA', 'FRP'),
            ('Spanish Introductory', 'SPI', 'LUM'),
            ('Python Introductory', 'PYI', 'BOA'),
            ('French Introductory', 'FRI', 'LUM'),
            ('Spanish Advanced', 'SPA', 'LUM'),
            ('Ruby Introductory', 'RUI', 'BOA'),
            ('Biology Introductory', 'BII', 'MOA')

        )
        self.initial_teachers = (
            ('Frank Pew', 56, 'Gångvägen 15', "ENI, ENA", 'FRP'),
            ('Lucia Madrid', 48, 'Promenadgränd 7', "SPI, FRI, SPA", 'LUM'),
            ('Boa Anaconda', 67, 'Slingervägen 3', "PYI, RUI", 'BOA'),
            ('Mohammad Awar', 39, 'Åkergränd 29', "BII", 'MOA')
        )

    def create_sample_db(self):
        """Create a sample db file"""
        try:
            with sqlite3.connect("SQL_sample.db") as connection:
                cursor = connection.cursor()

                cursor.execute('CREATE TABLE Members("First Name" TEXT, "Last name" TEXT, Title, Address TEXT,'
                               'Salary INT)')
                cursor.executemany('INSERT INTO Members VALUES(?, ?, ?, ?, ?);', self.initial_people)

                cursor.execute('CREATE TABLE "Office Supplies"("Order Date" TEXT, Region TEXT, Rep TEXT, Item TEXT,'
                               'Units INT, "Unit Cost" FLOAT, Total FLOAT)')
                cursor.executemany('INSERT INTO "Office Supplies" VALUES(?, ?, ?, ?, ?, ?, ?);', self.office_supplies)
            print("""Created "SQL_sample.db" """)
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()


    def create_test_db(self):
        """Create a sample db file"""
        try:
            with sqlite3.connect("SQL_test.db") as connection:
                cursor = connection.cursor()

                cursor.execute('CREATE TABLE Students(Name TEXT, Age INT, Courses TEXT, Address TEXT)')
                cursor.executemany("INSERT INTO Students VALUES(?, ?, ?, ?);", self.initial_students)

                cursor.execute('CREATE TABLE Courses(Subject TEXT, Code TEXT, Teacher TEXT)')
                cursor.executemany("INSERT INTO Courses VALUES(?, ?, ?);", self.initial_courses)

                cursor.execute('CREATE TABLE Teachers(Name, Age INT, Address TEXT, Courses TEXT, Initials TEXT)')
                cursor.executemany("INSERT INTO Teachers VALUES(?, ?, ?, ?, ?);", self.initial_teachers)
            print("""Created "SQL_test.db" """)
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def fetch_tablenames(filepath):
        """Fetches a list of all table names from a file"""
        try:
            with sqlite3.connect(filepath) as connection:
                cursor = connection.execute("""SELECT NAME FROM sqlite_master WHERE type="table";""")

                return [table[0] for table in cursor.fetchall()]
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def open_table(filepath, table_name):
        """Unpack data and return list of headers and list of lists of data"""
        
        try:
            with sqlite3.connect(filepath) as connection:

                # Get header names
                connection.row_factory = sqlite3.Row
                cursor = connection.execute(f"""SELECT rowid, * FROM "{table_name}" """)
                headers = cursor.fetchone().keys()  # List of headers
                headers[0] = "ID"  # Rename "rowid" as "Id"

                # Get rows of data. (RE-SELECT so that first data-row isn't lost)
                cursor.execute(f"""SELECT rowid, * FROM "{table_name}" ORDER BY ROWID""")
                data_rows = [[i for i in row] for row in cursor.fetchall()]
            return headers, data_rows
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def output_formatted(headers, data_rows):
        """Outputs formatted data"""
        # Get format len for each column
        format_spacing = [len(str(headers[i])) + 3 for i in range(len(headers))]  # Start with header lengths
        for i in range(len(headers)):  # For each data column...
            for line in data_rows:  # Check data rows
                if len(str(line[i])) > format_spacing[i] - 3:  # If len is larger than saved int
                    format_spacing[i] = len(str(line[i])) + 3  # update saved int

        # Format string of headers
        head_str = ""
        for i in range(len(headers)):
            head_str += f"{headers[i]:<{format_spacing[i]}}"

        # All data lines in one formatted string
        data_str = ""
        for i in range(len(data_rows)):
            line_str = ""
            for j in range(len(headers)):
                line_str += f"{data_rows[i][j]:<{format_spacing[j]}}"
            data_str += line_str + "\n"

        # Return headers and data as strings
        return head_str.strip(), data_str.strip(), sum(format_spacing)

    @staticmethod
    def write_row(filepath, table_name, data_dict):
        """Writes input data to table"""
        try:
            with sqlite3.connect(filepath) as connection:
                cursor = connection.cursor()

                header_string = ", ".join([f'"{keys}"' for keys in data_dict])
                data_row = tuple([data_dict[values] for values in data_dict])

                cursor.execute(f"""INSERT INTO "{table_name}" ({header_string}) VALUES {data_row}""")
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_row(filepath, table_name, row_id):
        try:
            with sqlite3.connect(filepath) as connection:
                cursor = connection.cursor()

                cursor.execute(f"""DELETE FROM "{table_name}" WHERE rowid={row_id}""")
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def edit_row(filepath, table_name, row_id, data_dict):
        try:
            with sqlite3.connect(filepath) as connection:
                cursor = connection.cursor()

                cursor.execute(f"""DELETE FROM "{table_name}" WHERE rowid={row_id}""")

                header_string = ", ".join([f'"{keys}"' for keys in data_dict])
                data_row = tuple([data_dict[item] for item in data_dict])

                cursor.execute(f"""INSERT INTO "{table_name}" ({header_string}) VALUES {data_row}""")
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def rip_txt(filepath):
        """Fetches data, separated by tabs , from a text file.
        Scrubs whitespace and prints it as tuples of data."""
        with open(filepath, "r") as f:

            for row in f:
                lst = row.split("\t")
                line = "', '".join(lst).strip()
                print(f"('{line}'),")


if __name__ == '__main__':
    sf = SupportFunctions()
    sf.create_sample_db()
    sf.create_test_db()
    # SupportFunctions().rip_txt("data1.txt")
