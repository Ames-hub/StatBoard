from datetime import datetime
from errors import errors
import os.path
import sqlite3

class db:
    @staticmethod
    def get_conn(check_on_deletion:bool=True, modernize_always=False) -> sqlite3.Connection:
        """
        This function is used to get a connection to the database. It will check if the database exists and if it doesn't,
        it will create it and bring it up to date.

        :param check_on_deletion:
        :param modernize_always:
        :return:
        """
        if not modernize_always:
            if check_on_deletion:
                if not os.path.exists('statbot.db'):
                    db.modernize()
        else:
            db.modernize()

        return sqlite3.connect('statbot.db')

    @staticmethod
    def track_new_stat(stat_name, stat_desc):
        with db.get_conn() as conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO stats (name, description)
                    VALUES (?, ?);
                ''', (stat_name, stat_desc))
                conn.commit()
            finally:
                cur.close()

    @staticmethod
    def delete_tracked_stat(stat_name):
        with db.get_conn() as conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    DELETE FROM stats
                    WHERE name = ?;
                ''', (stat_name,))
                conn.commit()  # Commit should be here and only called if everything succeeded
            finally:
                cur.close()

    @staticmethod
    def enter_stat_data(stat_name, value, date:datetime.date=None):
        """
        This function is used to enter data for a statistic. If the date is not provided, it will default to the current
        date.

        Note: I don't know how/why, but if you insert to the same date multiple times, it will add the values together
        :param stat_name: The name of the statistic
        :param value: The value to enter for the statistic
        :param date: The date to enter the data for. If not provided, it will default to the current date.
        :return:
        """
        with db.get_conn() as conn:
            try:
                if date is None:
                    date = datetime.now()
                    date = date.strftime('%Y-%m-%d')

                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO tracked_data (name, value, timestamp)
                    VALUES (?, ?, ?);
                ''', (stat_name, value, date))
            finally:
                print("Ran finally")
                conn.commit()
                cur.close()

    @staticmethod
    def delete_stat_data(stat_name, date:datetime.date):
        if date is None:
            return False

        with db.get_conn() as conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    DELETE FROM tracked_data
                    WHERE name = ? AND DATE(timestamp) = ?;
                ''', (stat_name, date))
            finally:
                conn.commit()
                cur.close()

    @staticmethod
    def check_stat_exists(stat_name) -> bool:
        """
        This function is used to check if a statistic exists in the database.

        :param stat_name:
        :return: True if the statistic exists, False if it doesn't
        """
        with db.get_conn() as conn:
            try:
                cur = conn.cursor()
                cur.execute('''
                    SELECT name
                    FROM stats
                    WHERE name = ?;
                ''', (stat_name,))

                return cur.fetchone() is not None
            finally:
                cur.close()

    @staticmethod
    def get_statistics(stat_name, searchback=7):
        with db.get_conn() as conn:
            cur = conn.cursor()
            # This query will get the entries by date and group by name
            query = '''
                SELECT name, SUM(value) AS total_value, DATE(timestamp) AS date
                FROM tracked_data
                WHERE timestamp >= datetime('now', ?)
                GROUP BY name, DATE(timestamp)
            '''
            params = (f'-{searchback} days',)
            if stat_name != '*':
                query += ' AND name = ?'
                params += (stat_name,)

            cur.execute(query, params)
            data = cur.fetchall()

            # Gets the 'name' column from stats table to determine if the statistic is still tracked and not deleted
            cur.execute('''
                SELECT name
                FROM stats
            ''')
            tracked_stats = cur.fetchall()

            # If the stat_name is not '*', check if the stat_name is in the tracked_stats list
            if stat_name != '*':
                # If the stat_name is not in the tracked_stats list, return an error
                if (stat_name,) not in tracked_stats:
                    raise errors.StatNonExistentError()
            else:
                # If the stat_name is '*', just filter out the stats that are not in the tracked_stats list
                data = [item for item in data if (item[0],) in tracked_stats]

                # If a tracked stat is not in the data, add it with a value of 0
                for stat in tracked_stats:
                    if stat[0] not in [item[0] for item in data]:
                        data.append((stat[0], 0, datetime.now().strftime('%Y-%m-%d')))

        # For every name and date combination, we need to organize the data
        evaluated_data = {}
        for item in data:
            name, total_value, date = item
            if name not in evaluated_data:
                evaluated_data[name] = {}
            evaluated_data[name][date] = total_value

        # Preview of eval'd data: {'statistic_name': {'2024-11-01': 392, ...}, ...}

        return evaluated_data

    @staticmethod
    def modernize():
        """
        This function is used to modernize the database to the current version. It will check if the tables exist and
        if they don't, it will create them. If the tables do exist, it will check if the columns are up to date and if
        they aren't, it will update them.

        :return:
        """
        # Function I pulled from another project.
        # Using this dict, it formats the SQL query to create the tables if they don't exist
        table_dict = {
            'stats': {
                'name': 'TEXT PRIMARY KEY',
                'description': 'TEXT DEFAULT NULL',
                'created_at': 'INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP',
            },
            'tracked_data': {
                'id': 'SERIAL',
                'name': 'TEXT REFERENCES stats(name)',
                'value': 'INTEGER NOT NULL',
                'timestamp': 'TEXT NOT NULL DEFAULT (DATE(\'now\'))',
            },
        }

        for table_name, columns in table_dict.items():
            with db.get_conn(check_on_deletion=False) as conn:
                cur = conn.cursor()
                cur.execute(f'''
                    SELECT name
                    FROM sqlite_master
                    WHERE type='table' AND name='{table_name}';
                ''')
                table_exist = cur.fetchone() is not None

            # If the table exists, check and update columns
            if table_exist:
                for column_name, column_properties in columns.items():
                    # Check if the column exists
                    cur.execute(f'''
                        PRAGMA table_info({table_name});
                    ''')
                    columns_info = cur.fetchall()
                    column_exist = any(column_info[1] == column_name for column_info in columns_info)

                    # If the column doesn't exist, add it
                    if not column_exist:
                        cur.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_properties};')

            # If the table doesn't exist, create it with columns
            else:
                columns_str = ', '.join(
                    [f'{column_name} {column_properties}' for column_name, column_properties in columns.items()]
                )
                try:
                    cur.execute(f'CREATE TABLE {table_name} ({columns_str});')
                except sqlite3.OperationalError:
                    exit(1)