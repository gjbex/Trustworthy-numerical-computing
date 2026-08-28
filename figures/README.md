# Course Figures

`binary64-spacing.svg` is an intentional, reviewed course asset generated from
IEEE 754 binary64 values by the Python standard library.

Regenerate it from the repository root with:

```bash
python scripts/generate_binary64_spacing_figure.py
```

The generator uses `math.nextafter` for the highlighted values and the exact
binary64 spacing rule within each displayed exponent interval. The figure shows
finite positive values from approximately $10^{-6}$ through $10^{16}$ on
logarithmic axes. The local number-line insets are magnified independently and
must not be interpreted as sharing one linear scale.
