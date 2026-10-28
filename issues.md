
# Static Code Analysis — Issue Log

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Insecure temporary-file creation | Security | Actual line | `tempfile.mktemp()` can introduce a race condition when creating files. | Use a secure temporary-file creation method. |
| Shell command execution | Security | Actual line | A constructed shell command can create command-injection risk. | Avoid shell interpretation and validate the input path. |
| Broad exception handling | Code quality | Actual line | `except Exception` can hide unexpected errors. | Catch the specific exception expected. |
| Non-standard function naming | Style | Actual lines | Function names use camelCase instead of snake_case. | Rename functions and update their calls. |
