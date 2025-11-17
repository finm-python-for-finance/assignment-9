Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
fix_parser.py                 19      2    89%   31-32
logger.py                     19      0   100%
main.py                       25      4    84%   30-38
order.py                      20      0   100%
risk_engine.py                16      1    94%   20
test\test_fix_parser.py       30      0   100%
test\test_logger.py           38      0   100%
test\test_order.py            38      0   100%
test\test_risk_engine.py      39      5    87%   29-37
test_main_flow.py             45      2    96%   92-93
--------------------------------------------------------
TOTAL                        289     14    95%
================= short test summary info =================
FAILED test/test_risk_engine.py::test_position_limit_exceeded - ValueError: Order size 1900 exceeds max 1000
FAILED test_main_flow.py::test_logger_save_writes_json - AssertionError: assert 4 == 2