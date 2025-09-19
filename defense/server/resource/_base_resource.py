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
            cursor.execute("SELECT * FROM %s", (self.table,))
            results = cursor.fetchall()
        # timedelta conversion
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
            cursor.execute("SELECT * FROM %s WHERE %s = %s", (self.table, pk, id))
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
        # validate and build columns safely
        cols = []
        vals = []
        for k, v in data.items():
            if not isinstance(k, str) or not k.replace('_', '').isalnum():
                raise ValueError("Invalid column name")
            cols.append(f"`{k}`")
            vals.append(v)
        placeholders = ', '.join(['%s'] * len(vals))
        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(self.table, ', '.join(cols), placeholders)
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(vals))
            self.db.commit()
            new_id = cursor.lastrowid
        return self.find(new_id)

    def update(self, id, data):
        """Update a record by ID."""
        if not self.table or not self.fields:
            raise ValueError("Table name or fields not set.")
        pk = self.fields[0]
        # build set clause safely
        set_parts = []
        vals = []
        for k, v in data.items():
            if not isinstance(k, str) or not k.replace('_', '').isalnum():
                raise ValueError("Invalid column name")
            set_parts.append(f"`{k}` = %s")
            vals.append(v)
        set_clause = ', '.join(set_parts)
        sql = "UPDATE `{}` SET {} WHERE `{}` = %s".format(self.table, set_clause, pk)
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(vals) + (id,))
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
