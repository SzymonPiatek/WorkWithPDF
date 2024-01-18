from pypdf import PdfMerger


pdfs = []

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("output.pdf")
merger.close()
