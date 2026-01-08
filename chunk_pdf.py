#!/usr/bin/env python3
"""
Chunk a large PDF into smaller text files for incremental processing.
"""

import fitz  # PyMuPDF
import os
import sys
from pathlib import Path


def extract_pdf_metadata(pdf_path: str) -> dict:
    """Get PDF metadata and page count."""
    doc = fitz.open(pdf_path)
    info = {
        "page_count": len(doc),
        "metadata": doc.metadata,
    }
    doc.close()
    return info


def extract_page_text(pdf_path: str, page_num: int) -> str:
    """Extract text from a single page (0-indexed)."""
    doc = fitz.open(pdf_path)
    if page_num >= len(doc):
        doc.close()
        return ""
    page = doc[page_num]
    text = page.get_text()
    doc.close()
    return text


def chunk_pdf_to_files(pdf_path: str, output_dir: str, pages_per_chunk: int = 10):
    """
    Split PDF into text chunks and save to files.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save chunk files
        pages_per_chunk: Number of pages per chunk file
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    os.makedirs(output_dir, exist_ok=True)

    # Create a table of contents file
    toc_lines = [f"# PDF Chunks: {Path(pdf_path).name}",
                 f"Total pages: {total_pages}",
                 f"Pages per chunk: {pages_per_chunk}",
                 "",
                 "## Chunks:"]

    chunk_num = 0
    for start_page in range(0, total_pages, pages_per_chunk):
        end_page = min(start_page + pages_per_chunk, total_pages)
        chunk_num += 1

        # Extract text for this chunk
        chunk_text = []
        for page_num in range(start_page, end_page):
            page = doc[page_num]
            text = page.get_text()
            chunk_text.append(f"\n--- Page {page_num + 1} ---\n")
            chunk_text.append(text)

        # Save chunk to file
        chunk_filename = f"chunk_{chunk_num:02d}_pages_{start_page+1}-{end_page}.txt"
        chunk_path = os.path.join(output_dir, chunk_filename)

        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(''.join(chunk_text))

        # Get first line preview for TOC
        first_lines = chunk_text[1][:100].replace('\n', ' ').strip() if len(chunk_text) > 1 else ""
        toc_lines.append(f"- `{chunk_filename}`: Pages {start_page+1}-{end_page} - {first_lines}...")

        print(f"Created: {chunk_filename} ({end_page - start_page} pages)")

    doc.close()

    # Save TOC
    toc_path = os.path.join(output_dir, "00_index.md")
    with open(toc_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(toc_lines))

    print(f"\nCreated {chunk_num} chunks in {output_dir}/")
    print(f"Index file: {toc_path}")


def print_page_preview(pdf_path: str, page_num: int, chars: int = 500):
    """Print a preview of a specific page."""
    text = extract_page_text(pdf_path, page_num)
    print(f"--- Page {page_num + 1} Preview ({chars} chars) ---")
    print(text[:chars])
    if len(text) > chars:
        print(f"\n... ({len(text) - chars} more characters)")


if __name__ == "__main__":
    pdf_path = "DCSD_FY25-26_May_Final_Budget.pdf"

    if len(sys.argv) > 1:
        if sys.argv[1] == "info":
            info = extract_pdf_metadata(pdf_path)
            print(f"Pages: {info['page_count']}")
            print(f"Metadata: {info['metadata']}")
        elif sys.argv[1] == "preview" and len(sys.argv) > 2:
            page_num = int(sys.argv[2]) - 1  # Convert to 0-indexed
            print_page_preview(pdf_path, page_num)
        elif sys.argv[1] == "chunk":
            pages_per_chunk = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            chunk_pdf_to_files(pdf_path, "budget_chunks", pages_per_chunk)
        else:
            print("Usage:")
            print("  python chunk_pdf.py info          - Show PDF info")
            print("  python chunk_pdf.py preview N     - Preview page N")
            print("  python chunk_pdf.py chunk [N]     - Chunk into N pages per file (default 10)")
    else:
        # Default: show info and chunk
        info = extract_pdf_metadata(pdf_path)
        print(f"PDF has {info['page_count']} pages")
        print("\nChunking PDF...")
        chunk_pdf_to_files(pdf_path, "budget_chunks", 10)
