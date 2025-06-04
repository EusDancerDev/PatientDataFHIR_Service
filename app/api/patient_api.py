"""
NOTE
----

According to our documentation in `cursor_main_questions_answers.md`,
we decided to keep certain files (or even abstract classes)
empty as a "back door" for future implementations.

This is a common and sensible approach in software projects, as it:

- **Reserves a place in the codebase** for future features or refactoring.
- **Signals intent** to other developers (or your future self) that this area is planned for expansion.
- **Helps maintain a clean and modular structure** as the project grows.

So, your empty `patient_api.py` is perfectly in line with your documented strategy.
We can leave it as is, perhaps with a comment at the top (which you already have),
and fill it in when we’re ready to implement new patient-related API features.

If we ever want to add an abstract class or interface as a placeholder,
we could do something like:

```python
# patient_api.py

class AbstractPatientAPI:
    \"\"\"Abstract base for future patient API implementations\"\"\"
    pass
```

But for now, our approach is absolutely fine!
"""