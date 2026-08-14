| Metric                | Value |
|-----------------------|-------|
| Submitted instances   | 40    |
| Completed instances   | 37    |
| Empty_Patch instances | 2     |
| Error instances       | 1     |
| Resolved instances    | 21    |
| Unresolved instances  | 16    |

| #  | Instance ID                      | Status      | Steps | Patch Size | Tool Calls | Tools Breakdown                                                                                                                      |
|----|----------------------------------|-------------|-------|------------|------------|--------------------------------------------------------------------------------------------------------------------------------------|
| 1  | django__django-10880             | Resolved    | 32    | 22         | 19         | insert_lines(3), outline_file(1), read_file(4), run_tests(6), str_replace(5)                                                         |
| 2  | django__django-11095             | Unresolved  | 16    | 8          | 13         | find_definition(5), insert_lines(2), outline_file(1), read_file(3), search_in_file(1), str_replace(1)                                |
| 3  | django__django-11333             | Resolved    | 23    | 16         | 11         | find_definition(1), insert_lines(1), read_file(2), run_tests(1), search_in_file(3), str_replace(3)                                   |
| 4  | django__django-11532             | Resolved    | 18    | 9          | 7          | insert_lines(1), read_file(2), run_tests(2), search_in_file(1), str_replace(1)                                                       |
| 5  | django__django-11880             | Resolved    | 57    | 29         | 26         | insert_lines(9), outline_file(1), read_file(12), run_tests(4)                                                                        |
| 6  | django__django-13089             | Resolved    | 28    | 10         | 17         | insert_lines(1), outline_file(1), read_file(9), run_tests(2), str_replace(4)                                                         |
| 7  | django__django-13363             | Resolved    | 26    | 6          | 6          | read_file(2), run_tests(2), search_in_file(1), str_replace(1)                                                                        |
| 8  | django__django-13417             | Unresolved  | 98    | 24         | 33         | find_definition(3), insert_lines(9), read_file(15), search_in_file(4), str_replace(2)                                                |
| 9  | django__django-14007             | Unresolved  | 28    | 30         | 22         | insert_lines(1), outline_file(3), read_file(11), str_replace(7)                                                                      |
| 10 | django__django-14017             | Resolved    | 35    | 48         | 21         | find_definition(1), insert_lines(5), outline_file(2), read_file(7), str_replace(4), write_file(2)                                    |
| 11 | django__django-14725             | Unresolved  | 78    | 1429       | 52         | insert_lines(9), outline_file(1), read_file(31), run_tests(7), str_replace(4)                                                        |
| 12 | django__django-14855             | Resolved    | 9     | 8          | 6          | find_definition(1), read_file(1), search_in_file(3), str_replace(1)                                                                  |
| 13 | django__django-15103             | Resolved    | 29    | 25         | 20         | find_definition(1), insert_lines(1), read_file(3), run_tests(7), search_in_file(2), str_replace(6)                                   |
| 14 | django__django-15315             | Resolved    | 22    | 48         | 6          | find_definition(3), read_file(1), search_in_file(1), str_replace(1)                                                                  |
| 15 | django__django-15368             | Unresolved  | 23    | 4          | 12         | find_definition(1), insert_lines(1), outline_file(1), read_file(3), run_tests(3), search_in_file(1), str_replace(2)                  |
| 16 | django__django-15554             | Unresolved  | 30    | 59         | 14         | find_definition(2), outline_file(2), read_file(9), str_replace(1)                                                                    |
| 17 | django__django-15863             | Resolved    | 14    | 35         | 8          | insert_lines(1), outline_file(1), read_file(4), search_in_file(2)                                                                    |
| 18 | django__django-15987             | Resolved    | 5     | 4          | 2          | read_file(1), str_replace(1)                                                                                                         |
| 19 | django__django-16136             | Unresolved  | 86    | 54         | 51         | find_definition(1), insert_lines(6), outline_file(2), read_file(20), run_tests(15), search_in_file(3), str_replace(3), write_file(1) |
| 20 | django__django-16560             | Unresolved  | 31    | 32         | 20         | find_definition(2), insert_lines(4), outline_file(1), read_file(10), str_replace(3)                                                  |
| 21 | django__django-16642             | Resolved    | 12    | 37         | 5          | find_definition(2), insert_lines(1), outline_file(1), read_file(1)                                                                   |
| 22 | django__django-16661             | Unresolved  | 55    | 44         | 20         | find_definition(2), insert_lines(1), read_file(5), run_tests(5), search_in_file(4), str_replace(3)                                   |
| 23 | psf__requests-2317               | Unresolved  | 13    | 41         | 8          | read_file(3), run_tests(2), search_in_file(2), str_replace(1)                                                                        |
| 24 | pydata__xarray-6461              | Resolved    | 83    | 39         | 54         | find_definition(2), insert_lines(5), outline_file(1), read_file(26), search_in_file(7), str_replace(13)                              |
| 25 | pydata__xarray-6992              | Unresolved  | 14    | 11         | 7          | insert_lines(1), read_file(5), str_replace(1)                                                                                        |
| 26 | pylint-dev__pylint-4661          | Unresolved  | 9     | 6          | 6          | find_definition(2), read_file(2), str_replace(2)                                                                                     |
| 27 | pytest-dev__pytest-5809          | Resolved    | 5     | 4          | 3          | read_file(1), search_in_file(1), str_replace(1)                                                                                      |
| 28 | pytest-dev__pytest-7982          | Resolved    | 6     | 4          | 4          | read_file(1), search_in_file(2), str_replace(1)                                                                                      |
| 29 | scikit-learn__scikit-learn-13135 | Resolved    | 29    | 3          | 6          | read_file(6)                                                                                                                         |
| 30 | scikit-learn__scikit-learn-13142 | Resolved    | 17    | 24         | 8          | find_definition(2), insert_lines(1), outline_file(2), read_file(3)                                                                   |
| 31 | sphinx-doc__sphinx-8595          | Error       | 20    | 22802      | 3          | read_file(1), search_in_file(1), str_replace(1)                                                                                      |
| 32 | sphinx-doc__sphinx-8721          | Resolved    | 37    | 4          | 22         | insert_lines(7), read_file(14), search_in_file(1)                                                                                    |
| 33 | sphinx-doc__sphinx-9229          | Unresolved  | 20    | 18         | 16         | find_definition(6), insert_lines(2), read_file(3), search_in_file(5)                                                                 |
| 34 | sympy__sympy-13615               | Empty_Patch | 250   | -          | 130        | find_definition(6), insert_lines(108), read_file(8), search_in_file(8)                                                               |
| 35 | sympy__sympy-13852               | Unresolved  | 11    | 39         | 6          | find_definition(2), outline_file(1), read_file(2), str_replace(1)                                                                    |
| 36 | sympy__sympy-14248               | Empty_Patch | 250   | -          | 80         | find_definition(3), insert_lines(52), outline_file(1), read_file(17), str_replace(7)                                                 |
| 37 | sympy__sympy-15017               | Resolved    | 21    | 11         | 11         | outline_file(2), read_file(6), search_in_file(2), str_replace(1)                                                                     |
| 38 | sympy__sympy-16792               | Resolved    | 113   | 44         | 50         | find_definition(6), insert_lines(8), read_file(22), str_replace(14)                                                                  |
| 39 | sympy__sympy-17139               | Unresolved  | 8     | 6          | 3          | read_file(1), str_replace(2)                                                                                                         |
| 40 | sympy__sympy-19346               | Unresolved  | 49    | 13         | 15         | find_definition(1), insert_lines(2), outline_file(1), read_file(10), search_in_file(1)                                               |
