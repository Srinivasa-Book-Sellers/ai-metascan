# ai-metascan

Turn photos of stationery inventory into a Vyapaar item import Excel file.

Each photo shows one item with a handwritten label (prices, quantity, stock). Copilot reads the photos, you confirm the extracted rows, and a small script fills the Vyapaar template.

## Folders

Images and generated files stay outside this repository, in `C:\Users\DELL\Documents\scanning`:

```text
scanning\
  input\          # Put new images here
  output\         # Generated inventory-<timestamp>.xlsx files
  processed\      # Images already written to Excel
  needs_review\   # Images Copilot could not read with confidence, with a reason .txt
  records\        # Batch JSON files used to fill the template
```

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Usage

1. Copy images into `scanning\input`.
2. In the Copilot app, ask: **"Process the scanning folder."**
3. Copilot reads each image, shows the extracted rows, and waits for you to confirm or correct them.
4. Copilot runs `scripts\fill_template.py`, which saves the Excel file in `output` and moves the images to `processed`.
5. Import the Excel file into Vyapaar.

The extraction rules and steps Copilot follows are in [`.github/skills/process-scanning/SKILL.md`](.github/skills/process-scanning/SKILL.md).

## Template

`resources\Import Items Template.xlsx` is the Vyapaar import template; its headers must not change. The script fills these `Item Details` columns when available: `Item name*`, `Item code`, `Category`, `HSN`, `Default MRP`, `Sale price`, `Purchase price`, `Wholesale price`, `Minimum wholesale quantity`, `Discount Type`, `Sale Discount`, and `Opening stock quantity`. Tax, unit, and MRP discount percentage columns are left blank.

Items without a barcode get an internal EAN-13 code starting with `200`, numbered after the highest such code in existing output files. These codes are for this shop only and are not registered GS1 barcodes.

## Test case

`tests\sample` holds 4 sample images (compressed to 1600px), the confirmed rows (`batch.json`), and the expected Excel output (`expected-output.xlsx`). The test runs the script on a temporary copy and checks the output matches:

```powershell
python -m unittest discover -s tests
```

To check extraction, ask Copilot to process the sample images and compare its rows with `batch.json`.
