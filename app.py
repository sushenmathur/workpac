"""WorkPac Document-to-Markdown converter.

A small Flask web app that wraps microsoft/markitdown. Users browse for a
document (PDF, Word, Excel, PowerPoint, HTML, image), the file is converted to
Markdown server-side, and the result is shown for preview, copy and download.
"""

from __future__ import annotations

import os
import tempfile

from flask import Flask, render_template, request
from markitdown import MarkItDown
from werkzeug.utils import secure_filename

# Formats markitdown[all] can handle. Used to hint the user and filter the
# browse dialog; markitdown ultimately decides what it can parse.
ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml", ".txt", ".md",
    ".png", ".jpg", ".jpeg", ".zip", ".epub",
}

# 32 MB upload ceiling.
MAX_CONTENT_LENGTH = 32 * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

_converter = MarkItDown()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", allowed=sorted(ALLOWED_EXTENSIONS))


@app.route("/convert", methods=["POST"])
def convert():
    uploaded = request.files.get("document")
    if uploaded is None or uploaded.filename == "":
        return render_template(
            "index.html",
            allowed=sorted(ALLOWED_EXTENSIONS),
            error="Please choose a file before converting.",
        ), 400

    filename = secure_filename(uploaded.filename)
    _, ext = os.path.splitext(filename.lower())
    if ext and ext not in ALLOWED_EXTENSIONS:
        return render_template(
            "index.html",
            allowed=sorted(ALLOWED_EXTENSIONS),
            error=f"Unsupported file type '{ext}'. Try a document, spreadsheet, "
                  f"presentation, HTML or image file.",
        ), 400

    # markitdown works from a path, so stage the upload in a temp file.
    tmp_dir = tempfile.mkdtemp(prefix="markitdown_")
    tmp_path = os.path.join(tmp_dir, filename or "upload")
    uploaded.save(tmp_path)

    try:
        result = _converter.convert(tmp_path)
        markdown = result.text_content or ""
    except Exception as exc:  # markitdown raises on unparseable input
        return render_template(
            "index.html",
            allowed=sorted(ALLOWED_EXTENSIONS),
            error=f"Could not convert '{filename}': {exc}",
        ), 500
    finally:
        try:
            os.remove(tmp_path)
            os.rmdir(tmp_dir)
        except OSError:
            pass

    md_name = (os.path.splitext(filename)[0] or "document") + ".md"
    return render_template(
        "result.html",
        source_name=filename,
        md_name=md_name,
        markdown=markdown,
        line_count=markdown.count("\n") + 1 if markdown else 0,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
