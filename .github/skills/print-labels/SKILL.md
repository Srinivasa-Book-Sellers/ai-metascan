---
name: print-labels
description: Generate printable blank item labels (2-across 38x25 mm roll) for writing item details and prices by hand. Use when the user asks to make, print, or generate labels or stickers.
---

# Print item labels

Run from the repository root:

```powershell
python scripts\make_labels.py --labels <N>
```

- Each PDF page is one row of the roll: 2 labels of 38×25 mm side by side, with a 2 mm gap (change with `--gap`).
- `--labels 10` makes a 5-page PDF (10 labels). Odd numbers round up to fill the row. Output goes to `C:\Users\DELL\Documents\scanning\labels\labels-<timestamp>.pdf` unless `--out` is given.
- Report the output file to the user.
- A 10-label sample and preview are in `resources\labels\`.

## Printing

- A label printer treats each PDF page as one row of labels and feeds the roll to the next row after each page. Printing a 5-page PDF once prints 10 labels.
- In the label printer driver, set the paper size to the page size (78×25 mm with the default gap) and print at **100% / actual size**, with no fit-to-page scaling.
- Use the driver's media/gap sensing (calibrate once) so each page starts at the top of a label row.
- Print a 2-label PDF first to check alignment. If the labels are shifted sideways, regenerate with a different `--gap`.

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
