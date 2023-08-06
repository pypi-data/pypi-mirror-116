# opportini_html2pdf
Python microservice to generate PDF from HTML


## generate PDF from HTML directly
PYTHONPATH=. python html2pdf_converter/converter.py --from_html 1 --html_file templates/void-report.html -o test.pdf -e 0

## generate PDF from template
PYTHONPATH=. python html2pdf_converter/converter.py --from_html 0 -o test.pdf -e 0 --temp_html_base_dir /Users/phoenix/Documents/Projects/CI/HTMLs
PYTHONPATH=. python html2pdf_converter/converter.py --from_html 0 -o test.pdf -e 0 --temp_html_base_dir ./HTMLs