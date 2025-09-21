---
applyTo: 'defense/server/**'
---
# Copilot Guidelines — Resource and Controller Directories

This instruction file is specifically tailored for the `resource/` and `controller/` directories within the `server/` directory of the `defense/` scope. The purpose of this file is to provide guidance on how to work with these directories, ensuring consistency, maintainability, and adherence to best practices.

---

## Purpose of the `controller/` Directory

- **Role**: The `controller/` directory contains the logic for handling incoming API requests and orchestrating the application's business logic.
- **Responsibilities**:
  - Validate and sanitize incoming requests.
  - Delegate data access to the `resource/` layer.
  - Handle errors gracefully and return appropriate HTTP responses.
- **Best Practices**:
  - Keep controllers lightweight and focused on request handling.
  - Avoid embedding business logic directly in controllers.
  - Use consistent naming conventions for methods and classes.
- **Key Files**:
  - `_base_controller.py`: Base class for shared functionality across controllers.
  - `attendance_logs_controller.py`: Manages attendance log-related operations.
  - `employees_controller.py`: Handles employee-related operations.
  - `payroll_controller.py`: Manages payroll-related functionality.
  - `shifts_controller.py`: Handles shift-related operations.
  - `users_controller.py`: Manages user-related actions, such as authentication.

---

## Purpose of the `resource/` Directory

- **Role**: The `resource/` directory encapsulates data access logic, interacting with the database or external APIs.
- **Responsibilities**:
  - Provide a clean interface for data retrieval and manipulation.
  - Abstract database queries and external API calls.
  - Ensure proper error handling for data operations.
- **Best Practices**:
  - Focus solely on data access and manipulation.
  - Avoid embedding business logic in resources.
  - Use parameterized queries to prevent SQL injection.
- **Key Files**:
  - `_base_resource.py`: Base class for shared functionality across resources.
  - `attendance_logs_resource.py`: Handles data access for attendance logs.
  - `employees_resource.py`: Manages data access for employee-related information.
  - `payroll_resource.py`: Provides data access for payroll-related data.
  - `shifts_resource.py`: Manages data access for shift-related data.
  - `users_resource.py`: Handles data access for user-related information.

---

## General Guidelines

1. **Secure Development**:
   - Validate and sanitize all inputs in controllers.
   - Use parameterized queries in resources to prevent SQL injection.
   - Implement proper authentication and authorization mechanisms.

2. **Error Handling**:
   - Use consistent error-handling patterns across controllers and resources.
   - Log errors for debugging while avoiding sensitive data exposure.

3. **Testing**:
   - Write unit tests for all controllers and resources.
   - Use mock data to simulate database interactions.
   - Ensure tests are isolated and repeatable.

4. **Documentation**:
   - Document all public methods and classes.
   - Use meaningful commit messages and PR descriptions.

---

By following these guidelines, the `resource/` and `controller/` directories will remain maintainable, secure, and aligned with the overall goals of the repository.