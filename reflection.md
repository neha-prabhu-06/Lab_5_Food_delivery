# Reflection

The handout says to provide answers to reflection questions, but the uploaded `Lab_5_Static_Code_Analysis_Student_handout.docx` does not list the four exact questions. It only states that students should reflect on the static analysis experience. The write-up below is therefore based on the reflection requirement and learning outcomes in the handout, without inventing missing instructor question wording.

## Static Analysis Experience

Using Pylint, Bandit, and Flake8 helped identify different categories of problems in `delivery_system.py`. Pylint was useful for code quality issues such as missing documentation, naming problems, dangerous default arguments, and broad exception handling. Flake8 focused on formatting and PEP 8 style issues, such as long lines and spacing. Bandit focused on security and identified the unsafe use of `pickle` for backup and restore.

The most important issue was the use of `pickle` for restoring saved orders. This was a security risk because loading pickle data from an untrusted file can execute unsafe code. Replacing it with JSON made the backup format safer and easier to inspect. After switching to JSON, restore validation was also added so corrupted or invalid backup data would not be accepted silently.

The tools also helped reveal reliability and maintainability problems. The original code accepted unknown menu items by assigning a fake price, allowed empty customer names and empty orders, accepted invalid statuses, and ignored missing order IDs. These issues were fixed with explicit input validation and clear `ValueError` messages. This made the program behavior easier to understand and safer to test.

After fixing the issues, the static analysis tools were run again to verify the results. The final Pylint score was `10.00/10`, Bandit reported no issues, and Flake8 reported no findings. This showed that the corrected code improved in style, security, and reliability while still preserving the expected food delivery order workflow.

Overall, this lab showed that static analysis is helpful because it catches problems that may not appear during a normal program run. However, the tools do not replace manual testing. Some important logic problems, such as incorrect order totals, invalid statuses, and `next_id` handling after restore, still needed to be checked by reading and testing the program behavior.
