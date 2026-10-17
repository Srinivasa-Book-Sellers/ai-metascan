"""Generate a printable PDF of blank item labels for a 2-across 38x25 mm label roll.

Each label has underlined fields to fill in by hand:

    Details ______________________
    MRP   ________   Sale  ________
    Whsl  ________   Qty   ________
    Pur   ________   Stock ________

Usage (from the repository root):
    python scripts\\make_labels.py [--gap MM] [--out FILE]

The PDF is a single page: one row of the roll (2 labels).
"""

import argparse
from datetime import datetime
from pathlib import Path

LABEL_W, LABEL_H = 38.0, 25.0
MARGIN = 1.5
ROWS = [["Details"], ["MRP", "Sale"], ["Whsl", "Qty"], ["Pur", "Stock"]]
FONT_SIZE = 6
LINE_WIDTH = 0.6  # points; about 2 dots on a 203 dpi printer
LABELS_DIR = Path(r"C:\Users\DELL\Documents\scanning\labels")

# Helvetica-Bold character widths (per 1000 units) for the field names.
WIDTHS = {
    "D": 722, "M": 833, "P": 667, "Q": 778, "R": 722, "S": 667, "W": 944,
    "a": 556, "c": 556, "e": 556, "h": 611, "i": 278, "k": 556, "l": 278,
    "o": 611, "r": 389, "s": 556, "t": 333, "u": 611, "y": 556,
}


def pt(mm):
    return mm * 72 / 25.4


def text_width_mm(text):
    return sum(WIDTHS[c] for c in text) * FONT_SIZE / 1000 * 25.4 / 72


def label_ops(x0):
    ops = []
    row_h = (LABEL_H - 2 * MARGIN) / len(ROWS)
    col_w = (LABEL_W - 2 * MARGIN - 1) / 2
    for i, names in enumerate(ROWS):
        line_y = LABEL_H - MARGIN - (i + 1) * row_h + 0.6
        for j, name in enumerate(names):
            if len(names) == 1:
                start, end = x0 + MARGIN, x0 + LABEL_W - MARGIN
            else:
                start = x0 + MARGIN + j * (col_w + 1)
                end = start + col_w
            ops.append(f"BT /F1 {FONT_SIZE} Tf {pt(start):.2f} {pt(line_y + 0.4):.2f} Td ({name}) Tj ET")
            line_start = start + text_width_mm(name) + 0.8
            ops.append(f"{pt(line_start):.2f} {pt(line_y):.2f} m {pt(end):.2f} {pt(line_y):.2f} l S")
    return ops


def build_pdf(gap):
    page_w = 2 * LABEL_W + gap
    content = "\n".join(
        [f"{LINE_WIDTH} w 0 G 0 g"] + label_ops(0) + label_ops(LABEL_W + gap)
    ).encode("ascii")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [5 0 R] /Count 1 >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(content), content),
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {pt(page_w):.2f} {pt(LABEL_H):.2f}] "
        f"/Resources << /Font << /F1 3 0 R >> >> /Contents 4 0 R >>".encode("ascii"),
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += b"%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(pdf)
    pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    pdf += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    pdf += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    return bytes(pdf)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gap", type=float, default=2.0, help="gap between the 2 labels in mm")
    parser.add_argument("--out", type=Path, help="output PDF (default: scanning\\labels\\labels-<timestamp>.pdf)")
    args = parser.parse_args()

    out = args.out or LABELS_DIR / f"labels-{datetime.now():%Y%m%d-%H%M%S}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(build_pdf(args.gap))
    print(f"Saved 2 labels to {out}")


if __name__ == "__main__":
    main()
