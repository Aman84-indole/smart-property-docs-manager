from pdf2image import convert_from_path

try:
    pdf_path = r'"C:\Users\DELL\Desktop\SmartProperty Docs Manager\uploads\geeta davi\House\Registry\registry.pdf"'
    pages = convert_from_path(
        pdf_path,
        dpi=100,
        poppler_path=r"C:\Users\DELL\Desktop\Release-23.11.0-0\poppler-23.11.0\Library\bin"
    )
    print("✅ Poppler Working - Pages loaded:", len(pages))
except Exception as e:
    print("❌ Poppler Conversion Failed:", e)
