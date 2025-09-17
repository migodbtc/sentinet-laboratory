---
applyTo: '**'
---
# Copilot Guidelines — Repository Context Awareness

This repository has **three distinct scopes**, and GitHub Copilot should generate code or documentation with this context in mind. Each scope has different expectations:

---

## 1. defense/ — Business System (Employee Attendance & Payroll)

* Focus on **secure software development**.
* Languages: JavaScript/TypeScript (Node.js + React) or Python (FastAPI/Flask).
* Always enforce **defensive coding practices**:

  * Input validation and sanitization.
  * Parameterized queries (no string concatenation in SQL).
  * Authentication and authorization (JWT, session management).
  * Proper error handling and logging.
* Encourage **unit tests** and **CI/CD best practices** (linting, testing, code quality checks).

---

## 2. offense/ — Educational Attack Simulations

* All content here is **lab-only and simulated**.
* Never generate code that targets **external systems** or performs real unauthorized actions.
* Attack examples should:

  * Be **safe payloads** (e.g., `' OR 1=1--` for SQLi).
  * Run only against **mock databases** or **lab containers** inside this repo.
  * Always include a **defense mapping** explaining how to mitigate the attack.
* Add a `/* SECURITY-RISK: SIMULATED ONLY */` header in files when producing potentially sensitive examples.

---

## 3. .notes/ — Knowledge & Personal Journey

* Generate **structured markdown** for:

  * Defensive notes
  * Offensive logs
  * Architecture/design reflections
* Support diagrams in Markdown (e.g., Mermaid) when illustrating architecture, workflows, or attack/defense flows.

---

## Cross-Cutting Instructions

* Always clarify whether content belongs to **defense**, **offense**, or **notes**.
* Pair every **offensive example** with a **defensive countermeasure**.
* If unsure whether a request is safe, **default to pseudocode and explanation** instead of runnable exploit code.

---

