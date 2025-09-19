# Whitelisting — Defensive Input Validation

- Title: Whitelisting — Defensive Input Validation & Enforcement
- Date: 2025-09-19
- Topic / Term: Whitelisting
- Category: Defensive / Input Validation
- Severity / Impact: High

## Summary 📝
Whitelisting is a defensive technique where only explicitly allowed values, patterns, or identifiers are accepted for use in application logic, configuration, or data access. This approach blocks untrusted or unexpected input, reducing the risk of injection, privilege escalation, and logic flaws. In database access, whitelisting is critical for preventing attackers from manipulating table or column names, query logic, or other sensitive resources.

## Technical Details 🔧
- Protocols / services involved: Application backends, database drivers (MySQL, PostgreSQL, SQLite), web APIs, configuration parsers.
- Typical targets / assets: Table names, column names, user roles, file paths, configuration keys, API endpoints.
- Example payloads / commands:
  - Attempted bypass: `employees; DROP TABLE employees; --` (should be rejected)
  - Invalid field: `first_name; UPDATE users SET admin=1` (should be rejected)
  - Valid field: `employee_id` (accepted if in whitelist)

## Walkthrough / Steps 🧭
Step-by-step reproduction or detection workflow:
1. Identify all places where user input or external data is used to select resources (e.g., table/column names, file paths).
2. Attempt to supply values not present in the application's whitelist (e.g., a table name not defined in the resource).
3. Observe that the application rejects or errors on non-whitelisted values, preventing unsafe access or logic.

## Detection 🔍
- Logs to check:
  - Application error logs for rejected identifiers or values.
  - Audit logs showing failed access attempts to non-whitelisted resources.
- IDS/IPS signatures:
  - Look for repeated attempts to access unknown tables, columns, or endpoints.
- Suggested SIEM queries (ELK / Splunk / Sigma):
  - Alert on error messages containing "Unsafe table name" or "Unsafe field".
  - Track requests with parameters not matching known whitelisted values.

## Mitigations / Best Practices 🛡️
- Short-term:
  - Define explicit lists of allowed tables, columns, roles, or endpoints in code.
  - Validate all identifiers and resource selectors against these lists before use.
  - Reject or error on any value not present in the whitelist.
- Long-term:
  - Centralize whitelist definitions and validation logic in a base class or configuration module.
  - Use static analysis to detect places where whitelisting is missing or bypassed.
  - Regularly review and update whitelists as application logic evolves.

## References 🔗
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- NIST SP 800-53: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final (see AC-6, SC-7)

## Notes / Observations 🗒️
- Whitelisting is more secure than blacklisting, as it only allows known-safe values and blocks everything else by default.
- In `_base_resource.py`, whitelisting is enforced by validating `self.table` and `self.fields` against resource-defined lists before using them in SQL queries. This blocks attackers from injecting or accessing unintended tables/columns.
- Whitelisting is applicable beyond SQL: use it for file access, configuration keys, API endpoints, and any resource selection logic.

---

*Classification: defensive note (for `defense/` scope). Includes lab-safe examples and defensive mappings.*
