import pandas as pd
from fpdf import FPDF
import re
import os
from datetime import datetime

class PDFReport(FPDF):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self._add_title()

    def _add_title(self):
        """Adding the report title with professional formatting"""
        self.set_font("Arial", 'B', 18)
        self.set_text_color(0, 51, 102)  # Dark blue color
        self.multi_cell(0, 12, self._clean_text(self.title), align='C')
        self.ln(10)
        self.set_text_color(0, 0, 0)  # Reset to black

    def _clean_text(self, text):
        """Cleaning text to remove or replace problematic Unicode characters"""
        if not text:
            return ""
        # Replace Unicode bullet points with hyphen
        text = text.replace('\u2022', '-')
        # Encode to UTF-8 and decode back to remove any other problematic characters
        return text.encode('utf-8', errors='ignore').decode('utf-8')

    def _parse_markdown(self, content):
        """Parsing markdown content into structured elements"""
        if not content or str(content).strip().lower() == "none":
            return []

        # Ensure content starts with a clean slate
        content = content.strip()
        lines = content.split("\n")
        elements = []
        current_text = []

        for line in lines:
            line = self._clean_text(line.strip())
            if not line:
                if current_text:
                    elements.append(("text", "\n".join(current_text)))
                    current_text = []
                elements.append(("space", None))  # Add spacing for blank lines
                continue

            # Detect headers (e.g., # Heading, ## Subheading)
            header_match = re.match(r'^(#+)\s+(.+)$', line)
            if header_match:
                if current_text:
                    elements.append(("text", "\n".join(current_text)))
                    current_text = []
                level = len(header_match.group(1))
                elements.append(("header", header_match.group(2), level))
                continue

            # Detect bullet points with optional bold subheadings
            bullet_match = re.match(r'^\s*[-•]\s+\*\*(.+?):\*\*\s*(.+)?$', line)
            if bullet_match:
                if current_text:
                    elements.append(("text", "\n".join(current_text)))
                    current_text = []
                bold_text = bullet_match.group(1)
                rest_text = bullet_match.group(2) or ""
                elements.append(("bullet_bold", f"{bold_text}: {rest_text}"))
                continue

            # Detect regular bullet points
            bullet_match = re.match(r'^\s*[-•]\s+(.+)$', line)
            if bullet_match:
                if current_text:
                    elements.append(("text", "\n".join(current_text)))
                    current_text = []
                elements.append(("bullet", bullet_match.group(1)))
                continue

            # Detect subheadings ending with colon
            if line.endswith(":") and not line.startswith("-"):
                if current_text:
                    elements.append(("text", "\n".join(current_text)))
                    current_text = []
                elements.append(("subheader", line[:-1]))
                continue

            current_text.append(line)

        if current_text:
            elements.append(("text", "\n".join(current_text)))

        return elements

    def add_section(self, heading, content):
        """Adding a section with proper markdown rendering and consistent spacing"""
        if not content or str(content).strip().lower() == "none":
            return

        # Ensure extra spacing before section heading
        self.ln(12)  # Increased spacing to separate from previous section

        # Render section heading
        self.set_font("Arial", 'B', 14)
        self.set_text_color(0, 51, 102)
        self.multi_cell(0, 10, self._clean_text(heading))
        self.ln(8)  # Increased spacing after heading
        self.set_text_color(0, 0, 0)

        # Preprocess content to ensure newline at start
        content = "\n" + content.strip()

        # Parse and render content
        elements = self._parse_markdown(content)
        for element in elements:
            if element[0] == "header":
                text, level = element[1], element[2]
                font_size = 13 if level == 1 else 12
                self.set_font("Arial", 'B', font_size)
                self.multi_cell(0, 8, self._clean_text(text))
                self.ln(2)
            elif element[0] == "subheader":
                self.set_font("Arial", 'B', 11)
                self.multi_cell(0, 8, self._clean_text(element[1]))
                self.ln(1)
            elif element[0] == "bullet":
                self.set_font("Arial", '', 11)
                self.set_x(20)  # Indent bullet points
                self.multi_cell(0, 8, f"- {self._clean_text(element[1])}")
                self.ln(1)  # Add spacing after bullet
            elif element[0] == "bullet_bold":
                self.set_font("Arial", 'B', 11)
                self.set_x(20)  # Indent bullet points
                self.multi_cell(0, 8, f"- {self._clean_text(element[1])}")
                self.set_font("Arial", '', 11)
                self.ln(1)  # Add spacing after bullet
            elif element[0] == "text":
                self.set_font("Arial", '', 11)
                self.multi_cell(0, 8, self._clean_text(element[1]))
                self.ln(1)
            elif element[0] == "space":
                self.ln(4)  # Add spacing for blank lines

        self.ln(8)  # Increased spacing after section content

def export_to_pdf(result, filename):
    """Exporting report data to a formatted PDF"""
    pdf = PDFReport(f"Research Report: {result.keyword}")
    pdf.add_section("1. Scope", result.scope)
    pdf.add_section("2. Research Design", result.design)
    pdf.add_section("3. Literature Review", result.literature)
    pdf.add_section("4. Analysis", result.analysis)
    pdf.add_section("5. Discussion and Conclusion", result.discussion)
    pdf.add_section("6. Ethical Considerations", result.ethics)
    pdf.add_section("7. References", result.references or "No references provided.")
    pdf.output(filename)
    return filename

def export_to_csv(results, filename):
    """Exporting report data to CSV with proper encoding and formatting"""
    data = []
    for r in results:
        data.append({
            "Keyword": r.keyword,
            "Scope": r.scope or "",
            "Design": r.design or "",
            "Literature": r.literature or "",
            "Analysis": r.analysis or "",
            "Discussion": r.discussion or "",
            "Ethics": r.ethics or "",
            "References": r.references or "",
            "Created At": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if isinstance(r.created_at, datetime) else r.created_at
        })
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')  # UTF-8 with BOM for better compatibility
    return filename