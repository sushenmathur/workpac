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
