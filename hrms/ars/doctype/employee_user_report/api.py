import frappe
import io
import zipfile
#from frappe.utils.pdf import merge_pdfs
# from frappe.utils.file_manager import save_file
# from frappe.utils import get_url

from frappe.utils.file_manager import save_file_on_filesystem
from frappe.utils import get_url

#import io
from typing import Iterable, Union
from pypdf import PdfReader, PdfWriter

PDFInput = Union[bytes, bytearray, memoryview, io.BytesIO]

def merge_pdfs(pdfs: Iterable[PDFInput]) -> bytes:
    """
    Merge an iterable of in-memory PDF binaries into a single PDF (as bytes).
    Each item should be a bytes-like object (not file paths).
    """
    writer = PdfWriter()

    for pdf in pdfs:
        # Normalize to BytesIO
        if isinstance(pdf, (bytes, bytearray, memoryview)):
            stream = io.BytesIO(bytes(pdf))
        elif isinstance(pdf, io.BytesIO):
            stream = pdf
            stream.seek(0)
        else:
            raise TypeError("merge_pdfs expects bytes-like objects or BytesIO streams")

        reader = PdfReader(stream)

        # pypdf ≥3 has writer.append(reader); older versions used append_pages_from_reader
        try:
            writer.append(reader)  # preferred in newer pypdf
        except AttributeError:
            for page in reader.pages:
                writer.add_page(page)

    out = io.BytesIO()
    writer.write(out)
    out.seek(0)
    return out.read()



PREFERRED_PF = "Ars Report Format"   # change/omit if not needed

def _get_pdf_bytes(doctype: str, name: str, print_format: str | None = None) -> bytes:
    """
    Always return PDF bytes for a single document.
    Works across Frappe versions that may not support as_pdf kwarg.
    """
    # Try: if this Frappe has as_pdf support
    try:
        pdf_or_html = frappe.get_print(
            doctype, name,
            print_format=print_format,
            as_pdf=True,                # ✅ returns bytes on newer Frappe
        )
        if isinstance(pdf_or_html, (bytes, bytearray, memoryview)):
            return bytes(pdf_or_html)
        # Some environments still hand back HTML; fall through to convert.
    except TypeError:
        # Older Frappe: no as_pdf kwarg → will raise TypeError
        pass

    # Fallback path: get HTML then convert
    html = frappe.get_print(
        doctype, name,
        print_format=print_format
    )
    # html is str → convert to PDF bytes
    return get_pdf(html)



# # 1) Write the PDF bytes to /public/files and get (file_name, file_url)

# # data -> {"file_name": "...", "file_url": "/files/Preview_All_Employee_User_Reports.pdf"}

# # 2) Create a File doc with NO attached_to_* fields


@frappe.whitelist()
def generate_all_employee_reports(from_date=None, to_date=None):
    employees = frappe.get_all("Employee", pluck="name")   #['HR-EMP-00008','HR-EMP-00020','HR-EMP-00017']#
    pdfs, failures = [], []

    for emp in employees:
        try:
            doc = frappe.new_doc("Employee User Report")
            doc.employee = emp
            doc.select_from = from_date
            doc.select_to = to_date
            doc.insert(ignore_permissions=True)
            doc.submit()

            # ALWAYS get PDF bytes
            pdf_bytes = _get_pdf_bytes("Employee User Report", doc.name, PREFERRED_PF)
            pdfs.append(pdf_bytes)

        except Exception as e:
            failures.append({"employee": emp, "error": frappe.utils.cstr(e)})

    # Merge expects bytes-like objects → now it will work
    merged = merge_pdfs(pdfs) if pdfs else b""

    file_url = None
    # if merged:
    #     fd = frappe.utils.file_manager.save_file(
    #         "All_Employee_User_Reports.pdf",
    #         merged,
    #         "File",
    #         None,
    #         is_private=0,
    #     )
    #     file_url = frappe.utils.get_url(fd.file_url)
    data = save_file_on_filesystem(
        fname=f"{to_date}.pdf",
        content=merged,         
        is_private=0
    )
    file_doc = frappe.get_doc({
    "doctype": "File",
    "file_name": data["file_name"],
    "file_url": data["file_url"],
    "is_private": 0,
    "folder": "Home",            

    })
    file_doc.insert(ignore_permissions=True)

    file_url = get_url(file_doc.file_url)

    return {
        "file_url": file_url,
        "count": len(pdfs),
        "failed": failures,
        "total_employees": len(employees),
    }
    employees = frappe.get_all("Employee", pluck="name")
    pdfs = []

    for emp in employees:
        doc = frappe.new_doc("Employee User Report")
        doc.employee = emp
        doc.select_from = from_date
        doc.select_to = to_date
        doc.insert(ignore_permissions=True)
        doc.submit()

        pdf_data = frappe.get_print(
            "Employee User Report",
            doc.name,
            print_format="Ars Report Format"
        )
        pdfs.append(pdf_data)
    merged = merge_pdfs(pdfs)
    file_doc = save_file(
        fname="Preview_All_Employee_User_Reports.pdf",
        content=merged,          # bytes
        folder="Home",
        is_private=0
    )
    file_url = get_url(file_doc.file_url)


    return {
        "file_url": get_url(file_doc.file_url),
        "count": len(employees)
    }

