import datetime

class BaseResource:
    """Base Resource class for data/model logic."""
    def __init__(self, db_connection, table=None, fields=None):
        self.db = db_connection
        self.table = table
        self.fields = fields or []

    def all(self):
        """Return all records."""
        if not self.table:
            raise ValueError("Table name not set.")
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table}")
            results = cursor.fetchall()
        # Convert timedelta fields to strings
        for row in results:
            for key, value in row.items():
                if isinstance(value, datetime.timedelta):
                    row[key] = str(value)
        return results


    def find(self, id):
        """Find a record by ID."""
        if not self.table or not self.fields:
            raise ValueError("Table name or fields not set.")
        pk = self.fields[0]
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE {pk} = %s", (id,))
            result = cursor.fetchone()
        if result:
            for key, value in result.items():
                if isinstance(value, datetime.timedelta):
                    result[key] = str(value)
        return result

    def create(self, data):
        """Create a new record."""
        if not self.table:
            raise ValueError("Table name not set.")
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            new_id = cursor.lastrowid
        return self.find(new_id)

    def update(self, id, data):
        """Update a record by ID."""
        if not self.table or not self.fields:
            raise ValueError("Table name or fields not set.")
        pk = self.fields[0]
        set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
        sql = f"UPDATE {self.table} SET {set_clause} WHERE {pk} = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()) + (id,))
            self.db.commit()
        return self.find(id)

    def delete(self, id):
        """Delete a record by ID."""
        if not self.table or not self.fields:
            raise ValueError("Table name or fields not set.")
        pk = self.fields[0]
        sql = f"DELETE FROM {self.table} WHERE {pk} = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            self.db.commit()
        return True
