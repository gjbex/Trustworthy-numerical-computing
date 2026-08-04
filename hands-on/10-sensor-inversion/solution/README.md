# Reference Solution

Use this directory after attempting or discussing the capstone starter.

- [`capstone.py`](capstone.py) contains the completed implementation.
- [`test_capstone.py`](test_capstone.py) contains the same checks supplied with
  the starter.
- [`evidence-record.md`](evidence-record.md) records the independently checked
  results and qualified conclusion.

From this directory, run:

```bash
python3 capstone.py
python3 capstone.py --report
python3 -m unittest -v
```

The implementation uses only Python's standard library. The `Decimal`
calculation is a reference for the declared nominal decimal inputs, while the
four-corner envelope addresses deterministic input sensitivity. Neither check
validates the physical sensor model.
