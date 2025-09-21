import datetime

class BaseResource:
    def __init__(self, db_connection, table=None, fields=None):
        self.db = db_connection
        self.table = table
        self.fields = fields or []

    def _validate_table(self):
        if not self.table or not isinstance(self.table, str):
            raise ValueError("Table name not set or invalid.")
        if not self.table.replace('_', '').isalnum():
            raise ValueError("Unsafe table name.")
        return self.table

    def _validate_fields(self, fields):
        if not self.fields or not isinstance(self.fields, list):
            raise ValueError("Fields not set or invalid.")
        for f in fields:
            if f not in self.fields:
                raise ValueError(f"Unsafe field: {f}. It is not included in the following fields: {self.fields}")
        return fields

    def all(self):
        """
        Returns all records from the resource table.
        Parameters:
            None

        Example:
            employees_resource.all()  
        """
        table = self._validate_table()
        with self.db.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM `{table}`"
            cursor.execute(sql)
            results = cursor.fetchall()
        for row in results:
            for key, value in row.items():
                if isinstance(value, datetime.timedelta):
                    row[key] = str(value)
        return results

    def find(self, id):
        """
        Finds a record by primary key.
        Parameters:
            id (any): The primary key value to search for.

        Example:
            employees_resource.find(1)  # Finds employee with employee_id=1
        """
        table = self._validate_table()
        pk = self.fields[0]
        self._validate_fields([pk])
        with self.db.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM `{table}` WHERE `{pk}` = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result:
            for key, value in result.items():
                if isinstance(value, datetime.timedelta):
                    result[key] = str(value)
        return result
    
    def find_by_field(self, field, value):
        """
        Finds a record by a specific field.
        Parameters:
            field (str): The field name to search by.
            value (any): The value to search for.

        Example:
            users_resource.find_by_field('username', 'alice.santos')
        """
        self._validate_fields([field])
        table = self._validate_table()
        with self.db.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM `{table}` WHERE `{field}` = %s"
            cursor.execute(sql, (value,))
            return cursor.fetchone()

    def create(self, data):
        """
        Creates a new record in the resource table.
        Parameters:
            data (dict): Dictionary of column-value pairs to insert.

        Example:
            employees_resource.create({
                'first_name': 'Eve',
                'last_name': 'Garcia',
                'position': 'DevOps Engineer',
                'base_salary': 60000.00,
                'hire_date': '2025-09-19'
            })
        """
        table = self._validate_table()
        cols = []
        vals = []
        for k, v in data.items():
            if not isinstance(k, str) or not k.replace('_', '').isalnum():
                raise ValueError("Invalid column name")
            self._validate_fields([k])
            cols.append(f"`{k}`")
            vals.append(v)
        placeholders = ', '.join(['%s'] * len(vals))
        sql = f"INSERT INTO `{table}` ({', '.join(cols)}) VALUES ({placeholders})"
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(vals))
            self.db.commit()
            new_id = cursor.lastrowid
        return self.find(new_id)

    def update(self, id, data):
        """
        Updates a record by primary key.
        Parameters:
            id (any): The primary key value to update.
            data (dict): Dictionary of column-value pairs to update.

        Example:
            employees_resource.update(2, {
                'base_salary': 42000.00,
                'position': 'HR Lead'
            })
        """
        table = self._validate_table()
        pk = self.fields[0]
        self._validate_fields([pk])
        set_parts = []
        vals = []
        for k, v in data.items():
            if not isinstance(k, str) or not k.replace('_', '').isalnum():
                raise ValueError("Invalid column name")
            self._validate_fields([k])
            set_parts.append(f"`{k}` = %s")
            vals.append(v)
        set_clause = ', '.join(set_parts)
        sql = f"UPDATE `{table}` SET {set_clause} WHERE `{pk}` = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(vals) + (id,))
            self.db.commit()
        return self.find(id)

    def delete(self, id):
        """
        Deletes a record by primary key.
        Parameters:
            id (any): The primary key value to delete.

        Example:
            employees_resource.delete(4) 
        """
        table = self._validate_table()
        pk = self.fields[0]
        self._validate_fields([pk])
        sql = f"DELETE FROM `{table}` WHERE `{pk}` = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            self.db.commit()
        return True
