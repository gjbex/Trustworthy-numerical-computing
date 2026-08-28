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

`floating-point-layouts-little-endian.svg` compares the logical field widths of
binary16, bfloat16, binary32, and binary64, then shows the same fields grouped
into bytes from low to high memory addresses on a little-endian system.

Regenerate it from the repository root with:

```bash
python scripts/generate_floating_point_layout_figure.py
```

The field allocations are encoded and checked in the generator. The logical
panel is endian-independent. In the memory panel, bytes are in increasing
address order and bits within each byte are shown in the conventional bit 7 to
bit 0 direction. The figure therefore does not imply that little endian reverses
all bits.
