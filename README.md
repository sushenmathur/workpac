# workpac

## MarkItDown

This repository uses [MarkItDown](https://github.com/microsoft/markitdown), a
lightweight Python utility for converting a wide range of file formats (PDF,
Word, Excel, PowerPoint, HTML, images, audio and more) into Markdown for use
with language models and text-analysis pipelines.

### Requirements

- Python 3.10 or higher

### Installation

Create and activate a virtual environment, then install from `requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

This installs `markitdown[all]`, which includes every optional format handler.
To install only the handlers you need, install the package directly with the
relevant extras, for example:

```bash
pip install 'markitdown[pdf,docx,pptx,xlsx]'
```

> **Note:** Audio transcription also requires `ffmpeg` to be installed and
> available on your `PATH`. Document conversion does not need it.

### Usage

Command line:

```bash
markitdown path/to/document.pdf > document.md
```

Python:

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("path/to/document.docx")
print(result.text_content)
```

## Web app (browse-file converter)

`app.py` is a small Flask web app that wraps MarkItDown with a browse-file
window: pick a document, and it returns clean Markdown to preview, copy or
download.

### Run it

```bash
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000> in your browser. Set a different port with
`PORT=5001 python app.py`.

### How it works

- `GET /` serves the browse-file page (`templates/index.html`).
- `POST /convert` stages the upload in a temporary file, runs MarkItDown, and
  renders the Markdown result (`templates/result.html`) with download and copy
  actions. The temporary file is deleted immediately after conversion.
- Supported inputs: PDF, Word, Excel, PowerPoint, HTML, CSV, images and more.
  Uploads are capped at 32&nbsp;MB.

> **Privacy:** candidate resumes and client documents contain personal
> information. Handle them in line with the Australian Privacy Principles and
> only upload what a task requires. This app runs locally and does not store
> files after conversion.

## Browser-only version (GitHub Pages)

`docs/` contains a **static, browser-only** converter that needs no server —
suitable for hosting on GitHub Pages. You browse for a file, it is converted to
Markdown **entirely in your browser**, and you can preview, copy or download the
result. Because nothing is uploaded, the file never leaves your device.

Conversion libraries are **vendored** in `docs/vendor/` (pdf.js, mammoth,
SheetJS, Turndown) so the app has no external CDN dependency.

### Differences from the Python app

- Runs client-side in JavaScript — it does **not** use the Python `markitdown`
  library, so output is not identical.
- Supports the common formats: PDF, Word (.docx), Excel (.xlsx/.xls), CSV, HTML
  and text. (No audio, images-with-OCR, or the full markitdown format list.)
- PDF text extraction is best-effort and may include minor spacing artefacts on
  complex layouts.

### Enable GitHub Pages

1. In the repository on GitHub, go to **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Select the branch, set the folder to **`/docs`**, and **Save**.
4. After a minute the site publishes at `https://<owner>.github.io/workpac/`.

> GitHub Pages on a **private** repository requires a paid GitHub plan. On a
> public repository it is free. Since this tool handles personal data, review
> hosting with your IT/security team before publishing it publicly.

---

*WorkPac Brand Style Guide is available on SharePoint: Marketing Toolbox >
Style Guide.*
