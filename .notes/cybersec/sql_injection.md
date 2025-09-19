# SQL Injection

- Title: SQL Injection — Injection Flaw & Prevention
- Date: 2025-09-19
- Topic / Term: SQL Injection
- Category: Injection / Defensive (lab-safe)
- Severity / Impact: High

## Summary 📝
SQL Injection (SQLi) is a class of injection vulnerabilities where untrusted input is embedded into SQL queries in an unsafe way, allowing attackers to alter the intended query semantics. Successful exploitation can lead to data leakage, data modification, authentication bypass, or full system compromise.

This note is a defensive write-up intended for lab use. All examples are safe and do not target external systems. When demonstrating vulnerable patterns we use pseudocode or mock examples that run only against controlled test databases.

## Technical Details 🔧
- Protocols / services involved: SQL databases (MySQL, PostgreSQL, SQLite, etc.) accessed via application backends (Python DB-API, MySQL Connector, psycopg2, ORM layers).
- Typical targets / assets: Web application input fields, query parameters, HTTP headers, APIs, batch import routines.
- Example payloads / commands:
  - Classic bypass: `' OR '1'='1` (used in a string context)
  - Termination + comment: `'; DROP TABLE users; -- ` (destructive payload; simulated only)
  - Blind boolean payload: `' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT((SELECT DATABASE()), FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) -- ` (complex; simulated only)

## Walkthrough / Steps 🧭
Reproduction / detection workflow (lab-only):
1. Identify user-controlled inputs that reach SQL execution paths (form fields, URL params, JSON body).
2. Probe with safe, low-impact payloads such as `' OR '1'='1` or `' AND 1=0 -- ` to observe differences in query results or application behavior.
3. Use parameterized queries / prepared statements or ORM abstractions to verify that the payloads no longer alter query structure.

## Detection 🔍
- Logs to check:
  - Application query logs (if available) for unexpected concatenated input.
  - Database error logs showing syntax errors or type mismatches originating from user values.
  - Web server access logs with suspiciously crafted parameters.
- IDS/IPS signatures: Look for common SQLi patterns such as `UNION SELECT`, `' OR 1=1`, `--`, `; DROP` in payloads.
- Suggested SIEM queries (ELK / Splunk / Sigma):
  - Search for parameter values containing `UNION` or multiple SQL keywords.
  - Rate-limit and alert on requests that cause repeated database errors from the same source.

## Mitigations / Best Practices 🛡️
- Short-term:
  - Use parameterized queries or prepared statements. Never build SQL by concatenating untrusted strings.
  - Perform input validation and strictly enforce expected data types and formats (whitelisting).
  - Apply least privilege for DB accounts — only grant the minimal privileges needed.
  - Enable detailed logging in non-production environments to capture query construction for review.
- Long-term:
  - Adopt an ORM or query builder that enforces parameterization by default.
  - Add a global DB access layer with centralized sanitization and parameterization.
  - Use static analysis and security testing (SAST/DAST) in CI to detect unsafe SQL patterns.
  - Run regular security reviews and threat modeling for new query paths.

## Example: Reviewing `_base_resource.py` (defensive and vulnerable patterns)
File referenced: `defense/server/resource/_base_resource.py`

Overview: `_base_resource.py` implements common CRUD methods that execute SQL against a database connection. The real-world risk surface depends on how SQL strings and parameters are built and passed to the DB driver.

Viable (safe) patterns used in `_base_resource.py`:
- Parameterized queries when inserting/updating/deleting values. For example, `create()` builds placeholders (`%s`) and passes `tuple(vals)` to `cursor.execute(sql, tuple(vals))`. This avoids injecting untrusted values into the structural SQL.
- Column name validation: Before interpolating column names into SQL, `create()` and `update()` verify column names with `k.replace('_', '').isalnum()` and wrap them in backticks. This prevents injection via column names (a common advanced vector).

Nonviable (unsafe) patterns observed or possible in similar code:
- Using string formatting to substitute table or column identifiers directly from untrusted input (e.g., `"SELECT * FROM %s" % table_name` without validation). The `_base_resource.py` version shows a potential issue in `all()` and `find()` where the SQL is written as `cursor.execute("SELECT * FROM %s", (self.table,))` — many DB APIs do not allow parameterizing identifiers (table names) this way; instead they treat them as strings which may produce invalid SQL. If the code string-interpolates identifiers without strict validation, it can become vulnerable.
- Concatenating user input into the WHERE clause or building raw SQL fragments from unvalidated strings.

Safe rewrite suggestions and checks:
1. Never pass table/column names as query parameters. Validate against a fixed allowlist, or set them in code and never accept from user input. For example:

   - Validate `self.table` against a module-level mapping of allowed tables:
     - `ALLOWED_TABLES = {'employees': 'employees', 'shifts': 'shifts'}`
     - `if self.table not in ALLOWED_TABLES: raise ValueError()`

2. Use parameterized queries only for data values, not identifiers. Compose SQL identifiers with explicit, validated strings and use parameters for values:

   - Safe SELECT by id example:

     sql = f"SELECT * FROM `{self.table}` WHERE `{pk}` = %s"
     cursor.execute(sql, (id,))

3. Centralize DB access and enforce the patterns in a base resource or use an ORM.

## Detection examples using `_base_resource.py` patterns
- If `all()` uses `cursor.execute("SELECT * FROM %s", (self.table,))`, test it in a dev environment: set `self.table` to an unexpected value (simulate attacker-controlled string) and observe the resulting SQL or error. Proper DB drivers will treat that parameter as a string literal and the query will likely fail; but if an application incorrectly formats identifiers, it's a red flag.

## Defensive countermeasures mapping (for lab/from `offense/` mapping)
- If offensive lab code demonstrates concatenation-based SQL execution, mirror it only against a mock DB within `offense/` with the header `/* SECURITY-RISK: SIMULATED ONLY */` and include a clear mitigation section (as above).

## References 🔗
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- OWASP Cheat Sheet — SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- MySQL parameterized queries docs (connector): https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
- PEP 249 — Python Database API Specification v2.0: https://www.python.org/dev/peps/pep-0249/

## Notes / Observations 🗒️
- Some DB drivers do not support parameterizing SQL identifiers like table names; treat any attempt to parameterize identifiers as suspicious and instead use strict validation and whitelisting.
- Where column names are built dynamically, prefer an internal mapping of logical fields to physical columns to avoid direct user input in identifiers.
- When in doubt, prefer explicit errors over attempting to accept unknown identifiers.

---

*Classification: defensive note (for `defense/` scope). Includes lab-safe examples and defensive mappings.*
