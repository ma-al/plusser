Description
===========
Reads in a CSV like so:
```bash
money.txt
Date | Time | Amount | Location | Notes
2015-01-02 | 14:44:25 +1100 | +100 | ATM | Cash Withdrawal
2015-01-05 | 23:15:56 +1100 | -25 | Fancy Restaurant | Lunch
2015-01-09 | 14:20:01 +1100 | -9 | Corner Food Store | Dinner
2015-01-09 | 14:20:01 +1100 | -1 | N/A | Lost
```

Then calculates a running total, and re-inserts back to the file like so:
```bash
...
2015-01-09 | 14:20:01 +1100 | -9 | Corner Food Store | Dinner
2015-01-09 | 14:20:01 +1100 | -1 | N/A | Lost
2015-01-09 | 19:21:01 +1100 | 00 | N/A | Running Total: 65
```
