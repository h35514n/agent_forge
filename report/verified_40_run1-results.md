| Metric                | Value |
|-----------------------|-------|
| Submitted instances   | 40    |
| Completed instances   | 35    |
| Empty_Patch instances | 2     |
| Error instances       | 3     |
| Resolved instances    | 19    |
| Unresolved instances  | 16    |

| #  | Instance ID                      | Status      | Steps | Patch Size | Tool Calls | Tools Breakdown                                                                                |
|----|----------------------------------|-------------|-------|------------|------------|------------------------------------------------------------------------------------------------|
| 1  | django__django-10880             | Unresolved  | 56    | 1524       | 26         | read_file(8), run_tests(2), search_in_file(3), str_replace(1), write_file(12)                  |
| 2  | django__django-11095             | Resolved    | 15    | 8          | 7          | find_definition(1), outline_file(1), read_file(5)                                              |
| 3  | django__django-11333             | Resolved    | 31    | 2191       | 15         | outline_file(1), read_file(6), run_tests(2), search_in_file(1), str_replace(3), write_file(2)  |
| 4  | django__django-11532             | Resolved    | 32    | 34         | 12         | read_file(6), run_tests(2), write_file(4)                                                      |
| 5  | django__django-11880             | Resolved    | 40    | 1253       | 19         | read_file(12), run_tests(2), write_file(5)                                                     |
| 6  | django__django-13089             | Unresolved  | 20    | 301        | 15         | read_file(10), search_in_file(1), str_replace(1), write_file(3)                                |
| 7  | django__django-13363             | Resolved    | 33    | 166        | 12         | outline_file(1), read_file(8), run_tests(2), str_replace(1)                                    |
| 8  | django__django-13417             | Resolved    | 35    | 1988       | 9          | find_definition(4), read_file(2), search_in_file(2), write_file(1)                             |
| 9  | django__django-14007             | Resolved    | 70    | 2258       | 46         | read_file(20), search_in_file(22), str_replace(4)                                              |
| 10 | django__django-14017             | Unresolved  | 57    | 434        | 25         | outline_file(1), read_file(16), run_tests(1), search_in_file(2), str_replace(1), write_file(4) |
| 11 | django__django-14725             | Empty_Patch | 250   | -          | 114        | outline_file(2), read_file(88), run_tests(15), str_replace(4), write_file(5)                   |
| 12 | django__django-14855             | Resolved    | 6     | 451        | 4          | read_file(2), search_in_file(1), str_replace(1)                                                |
| 13 | django__django-15103             | Unresolved  | 23    | 1623       | 16         | read_file(6), run_tests(3), search_in_file(2), str_replace(3), write_file(2)                   |
| 14 | django__django-15315             | Resolved    | 25    | 2550       | 7          | find_definition(4), read_file(1), search_in_file(1), str_replace(1)                            |
| 15 | django__django-15368             | Resolved    | 24    | 3265       | 11         | read_file(4), run_tests(4), str_replace(1), write_file(2)                                      |
| 16 | django__django-15554             | Error       | 51    | 0          | 43         | read_file(19), run_tests(11), search_in_file(3), write_file(10)                                |
| 17 | django__django-15863             | Unresolved  | 24    | 1026       | 13         | read_file(6), search_in_file(3), str_replace(2), write_file(2)                                 |
| 18 | django__django-15987             | Resolved    | 8     | 4          | 4          | outline_file(1), read_file(3)                                                                  |
| 19 | django__django-16136             | Resolved    | 27    | 371        | 11         | find_definition(3), read_file(4), search_in_file(1), write_file(3)                             |
| 20 | django__django-16560             | Error       | 52    | 0          | 16         | outline_file(1), read_file(9), search_in_file(2), write_file(4)                                |
| 21 | django__django-16642             | Unresolved  | 23    | 789        | 6          | outline_file(1), read_file(2), str_replace(3)                                                  |
| 22 | django__django-16661             | Unresolved  | 14    | 2522       | 9          | read_file(5), run_tests(2), search_in_file(1), write_file(1)                                   |
| 23 | psf__requests-2317               | Unresolved  | 31    | 97         | 11         | outline_file(1), read_file(6), search_in_file(4)                                               |
| 24 | pydata__xarray-6461              | Resolved    | 12    | 2017       | 6          | read_file(3), search_in_file(2), write_file(1)                                                 |
| 25 | pydata__xarray-6992              | Unresolved  | 6     | 8949       | 2          | read_file(1), write_file(1)                                                                    |
| 26 | pylint-dev__pylint-4661          | Unresolved  | 33    | 130        | 19         | read_file(9), search_in_file(2), str_replace(7), write_file(1)                                 |
| 27 | pytest-dev__pytest-5809          | Resolved    | 7     | 120        | 5          | read_file(3), str_replace(2)                                                                   |
| 28 | pytest-dev__pytest-7982          | Resolved    | 7     | 4          | 3          | read_file(1), search_in_file(2)                                                                |
| 29 | scikit-learn__scikit-learn-13135 | Resolved    | 16    | 312        | 8          | outline_file(1), read_file(3), write_file(4)                                                   |
| 30 | scikit-learn__scikit-learn-13142 | Resolved    | 39    | 1170       | 16         | find_definition(1), outline_file(2), read_file(10), write_file(3)                              |
| 31 | sphinx-doc__sphinx-8595          | Error       | 65    | 0          | 28         | outline_file(2), read_file(16), search_in_file(1), str_replace(1), write_file(8)               |
| 32 | sphinx-doc__sphinx-8721          | Unresolved  | 5     | 302        | 2          | read_file(1), write_file(1)                                                                    |
| 33 | sphinx-doc__sphinx-9229          | Unresolved  | 73    | 601        | 36         | outline_file(4), read_file(22), search_in_file(1), str_replace(2), write_file(7)               |
| 34 | sympy__sympy-13615               | Unresolved  | 49    | 2287       | 29         | find_definition(2), read_file(13), search_in_file(6), str_replace(8)                           |
| 35 | sympy__sympy-13852               | Unresolved  | 12    | 584        | 4          | outline_file(1), read_file(2), str_replace(1)                                                  |
| 36 | sympy__sympy-14248               | Empty_Patch | 250   | -          | 104        | find_definition(1), read_file(36), search_in_file(9), str_replace(36), write_file(22)          |
| 37 | sympy__sympy-15017               | Unresolved  | 68    | 4          | 21         | find_definition(3), outline_file(2), read_file(10), search_in_file(5), str_replace(1)          |
| 38 | sympy__sympy-16792               | Resolved    | 37    | 2281       | 24         | outline_file(2), read_file(13), search_in_file(7), str_replace(1), write_file(1)               |
| 39 | sympy__sympy-17139               | Resolved    | 35    | 4451       | 22         | read_file(10), run_tests(6), str_replace(2), write_file(4)                                     |
| 40 | sympy__sympy-19346               | Unresolved  | 23    | 18         | 3          | read_file(3)                                                                                   |
