import fitz  # PyMuPDF
import os
import sys

def xu_ly_pdf_A4_A3():
    # Giữ nguyên cách lấy thư mục của bạn nhưng thêm xử lý cho file EXE
    if getattr(sys, 'frozen', False):
        input_folder = os.path.dirname(sys.executable)
    else:
        input_folder = os.getcwd()

    output_folder = os.path.join(input_folder, "KET_QUA_GOM_FILE")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Giữ nguyên cách lọc file của bạn
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    
    # Tìm file A4 và A3 theo cách của bạn
    file_a4 = next((f for f in files if "(A4)" in f), None)
    file_a3 = next((f for f in files if "(A3)" in f), None)
    
    page_counter = 1
    blue = (0, 0, 1)

    # =========================
    # 1. XỬ LÝ FILE A4
    # =========================
    if file_a4:
        doc = fitz.open(os.path.join(input_folder, file_a4))
        new_doc = fitz.open() # Tạo file mới để thực hiện Shrink
        
        for page in doc:
            # Bước 1: Xoay ngược chiều kim đồng hồ nếu trang ngang (Giống ý bạn)
            if page.rect.width > page.rect.height:
                page.set_rotation((page.rotation + 90) % 360)
            
            rect = page.rect
            w, h = rect.width, rect.height

            # Bước 2: THU NHỎ NỘI DUNG (Để tạo lề đánh số đẹp như PDF-XChange)
            new_page = new_doc.new_page(width=w, height=h)
            # Thu nhỏ 95% diện tích, chừa lề dưới
            shrink_rect = fitz.Rect(w*0.02, h*0.01, w*0.98, h*0.95)
            new_page.show_pdf_page(shrink_rect, doc, page.number)

            # Bước 3: Đánh số tại Vị trí A (A4 Dọc)
            pos = fitz.Point(w - 60, h - 30)
            new_page.insert_text(pos, f"Page {page_counter}", fontsize=11, fontname="helv", color=blue)
            page_counter += 1
            
        new_doc.save(os.path.join(output_folder, f"Checked_{file_a4}"))
        new_doc.close()
        doc.close()

    # =========================
    # 2. XỬ LÝ FILE A3
    # =========================
    if file_a3:
        doc = fitz.open(os.path.join(input_folder, file_a3))
        new_doc = fitz.open() # Tạo file mới để thực hiện Shrink
        
        for page in doc:
            rect = page.rect
            w, h = rect.width, rect.height

            # Thu nhỏ nội dung bản vẽ A3 để không đè vào khung tên
            new_page = new_doc.new_page(width=w, height=h)
            shrink_rect = fitz.Rect(w*0.02, h*0.01, w*0.98, h*0.95)
            new_page.show_pdf_page(shrink_rect, doc, page.number)

            # Phân loại vị trí B (A3 Dọc) hoặc C (A3 Ngang)
            if w < h: # A3 Dọc (Vị trí B)
                pos = fitz.Point(w - 80, h - 40)
                f_size = 13
            else: # A3 Ngang (Vị trí C)
                pos = fitz.Point(w - 120, h - 50)
                f_size = 14

            new_page.insert_text(pos, f"Page {page_counter}", fontsize=f_size, fontname="helv", color=blue)
            page_counter += 1
            
        new_doc.save(os.path.join(output_folder, f"Checked_{file_a3}"))
        new_doc.close()
        doc.close()

    print("Hoàn thành! Kiểm tra thư mục KET_QUA_GOM_FILE")

if __name__ == "__main__":
    xu_ly_pdf_A4_A3()
