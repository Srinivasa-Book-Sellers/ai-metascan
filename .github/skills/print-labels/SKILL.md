---
name: print-labels
description: Generate printable blank item labels (2-across 38x25 mm roll) for writing item details and prices by hand. Use when the user asks to make, print, or generate labels or stickers.
---

# Print item labels

Run from the repository root:

```powershell
python scripts\make_labels.py
```

- The PDF is one page: one row of the roll with 2 labels of 38×25 mm side by side and a 2 mm gap (change with `--gap`).
- Output goes to `C:\Users\DELL\Documents\scanning\labels\labels-<timestamp>.pdf` unless `--out` is given.
- Report the output file to the user.
- A sample and preview are in `resources\labels\`.

## Printing

- In the label printer driver, set the paper size to the page size (78×25 mm with the default gap) and print at **100% / actual size**, with no fit-to-page scaling.
- For more labels, set the number of copies in the print dialog.
- If the labels are shifted sideways, regenerate with a different `--gap`.

## Label fields

```
Details ______________________
MRP   ________   Sale  ________
Whsl  ________   Qty   ________
Pur   ________   Stock ________
```

`process-scanning` maps these fields to template columns.

## Writing on the labels

- Write in dark ink above each line, one value per field, without crossing into the next field.
- Write paise with a dot or dash (`40.50` or `40-50`); both mean 40 rupees 50 paise.
- Leave a field blank rather than writing a dash or "NA".
- Photograph the item with the label flat, in good light, and fully in frame.
