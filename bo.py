import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chương Trình Xử Lý Ảnh - OpenCV")
        
        self.root.geometry("1000x950")
        self.root.minsize(950, 750)

        self.img_raw = None          
        self.img_bgr = None          
        self.img_rgb = None
        self.img_gray = None
        self.img_hsv = None

        self.active_tool_img = None  
        self.initial_tool_img = None 
        self.active_color_name = "RGB"
        self.selected_point = None   

        self.setup_scrollable_window()
        self.setup_header()
        self.setup_step1_select()
        self.setup_step2_convert()
        self.setup_step3_display_and_tools()

    def setup_scrollable_window(self):
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scroll_content = tk.Frame(self.main_canvas)

        self.scroll_content.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        self.main_canvas.create_window((0, 0), window=self.scroll_content, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def setup_header(self):
        header_frame = tk.Frame(self.scroll_content, bg="#1565C0", pady=15)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="XỬ LÝ ẢNH", font=("Arial", 18, "bold"), fg="white", bg="#1565C0").pack()
        tk.Label(
            header_frame, 
            text="Họ và tên: Dung Thanh Hiền  |  MSSV: 124001518  |  Lớp: 24TD111", 
            font=("Arial", 10, "italic"), 
            fg="#E3F2FD", 
            bg="#1565C0"
        ).pack(pady=(4, 0))

    def setup_step1_select(self):
        frame_s1 = tk.LabelFrame(self.scroll_content, text=" BƯỚC 1: CHỌN HÌNH ÁNH ", font=("Arial", 11, "bold"), padx=15, pady=10)
        frame_s1.pack(fill="x", padx=15, pady=10)

        self.btn_select = tk.Button(
            frame_s1, 
            text="📂 Chọn Hình Ảnh Trên Máy Tính", 
            font=("Arial", 11, "bold"),
            bg="#2E7D32", 
            fg="white", 
            padx=15, 
            pady=6,
            cursor="hand2",
            command=self.choose_image
        )
        self.btn_select.pack()

        self.lbl_status = tk.Label(frame_s1, text="Trạng thái: Chưa chọn ảnh", font=("Arial", 10), fg="#757575")
        self.lbl_status.pack(pady=4)

        self.frame_preview_step1 = tk.Frame(frame_s1)
        self.frame_preview_step1.pack(pady=4)

    def setup_step2_convert(self):
        self.frame_s2 = tk.LabelFrame(self.scroll_content, text=" BƯỚC 2: PHÂN TÍCH MÀU ", font=("Arial", 11, "bold"), padx=15, pady=10)
        self.frame_s2.pack(fill="x", padx=15, pady=5)

        self.btn_convert_3color = tk.Button(
            self.frame_s2, 
            text="🎨 1. Chuyển Đổi & Hiển Thị 3 Không Gian Màu", 
            font=("Arial", 11, "bold"),
            bg="#1976D2", 
            fg="white", 
            pady=8,
            cursor="hand2",
            state="disabled",
            command=self.render_3_color_spaces
        )
        self.btn_convert_3color.pack(fill="x")

    def setup_step3_display_and_tools(self):
        self.frame_s3 = tk.Frame(self.scroll_content, padx=15, pady=5)
        self.frame_s3.pack(fill="x")

        self.frame_3_images = tk.Frame(self.frame_s3)
        self.frame_3_images.pack(fill="x")

        self.frame_bottom_action = tk.Frame(self.frame_s3, pady=15)
        
        self.btn_tools = tk.Button(
            self.frame_bottom_action, 
            text="🛠️ 2. Công Cụ Biến Đổi (Tools)", 
            font=("Arial", 11, "bold"),
            bg="#7B1FA2", 
            fg="white", 
            pady=8,
            padx=25,
            cursor="hand2",
            command=self.open_tools_selector
        )
        self.btn_tools.pack()

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn hình ảnh",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp *.tiff"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.img_raw = cv2.imread(file_path)
        if self.img_raw is None:
            messagebox.showerror("Lỗi", "Không thể đọc file hình ảnh đã chọn!")
            return

        self.img_bgr = self.img_raw.copy()
        self.update_color_spaces()

        file_name = file_path.split("/")[-1]
        self.lbl_status.config(text=f"Đã chọn: {file_name}", fg="#2E7D32")

        for widget in self.frame_preview_step1.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(4.0, 2.5))
        ax.imshow(cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2RGB))
        ax.axis("off")
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_preview_step1)
        canvas.draw()
        canvas.get_tk_widget().pack()

        self.btn_convert_3color.config(state="normal")
        self.frame_bottom_action.pack_forget()
        for widget in self.frame_3_images.winfo_children():
            widget.destroy()

    def update_color_spaces(self):
        self.img_rgb = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2RGB)
        self.img_gray = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)
        self.img_hsv = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2HSV)

    def render_3_color_spaces(self):
        for widget in self.frame_3_images.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(11.5, 3.5))
        
        plt.subplot(1, 3, 1)
        plt.imshow(self.img_rgb)
        plt.title("1. Ảnh Gốc (RGB)", fontsize=11, fontweight='bold')
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.imshow(self.img_gray, cmap='gray')
        plt.title("2. Ảnh Xám (Grayscale)", fontsize=11, fontweight='bold')
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.imshow(self.img_hsv)
        plt.title("3. Ảnh Màu HSV", fontsize=11, fontweight='bold')
        plt.axis("off")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_3_images)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x")

        self.frame_bottom_action.pack()

    # =========================================================================
    # BẢNG TOOLS
    # =========================================================================
    def open_tools_selector(self):
        select_win = tk.Toplevel(self.root)
        select_win.title("Chọn loại ảnh chỉnh sửa")
        select_win.geometry("360x220")
        select_win.grab_set()

        tk.Label(select_win, text="CHỌN 1 LOẠI MÀU ÁNH CẦN CHỈNH SỬA:", font=("Arial", 10, "bold"), pady=15).pack()

        def start_tool(color_type):
            select_win.destroy()
            if color_type == "RGB":
                self.active_tool_img = self.img_bgr.copy()
                self.active_color_name = "Ảnh Gốc (RGB)"
            elif color_type == "GRAY":
                self.active_tool_img = cv2.cvtColor(self.img_gray, cv2.COLOR_GRAY2BGR)
                self.active_color_name = "Ảnh Xám (Grayscale)"
            else:
                self.active_tool_img = self.img_hsv.copy()
                self.active_color_name = "Ảnh Màu HSV"

            # Lưu bản sao ban đầu chuẩn
            self.initial_tool_img = self.active_tool_img.copy()
            self.selected_point = None
            self.show_tools_window()

        tk.Button(select_win, text="1. Ảnh Gốc (RGB)", font=("Arial", 10), bg="#1976D2", fg="white", width=25, command=lambda: start_tool("RGB")).pack(pady=4)
        tk.Button(select_win, text="2. Ảnh Xám (Grayscale)", font=("Arial", 10), bg="#616161", fg="white", width=25, command=lambda: start_tool("GRAY")).pack(pady=4)
        tk.Button(select_win, text="3. Ảnh Màu HSV", font=("Arial", 10), bg="#E65100", fg="white", width=25, command=lambda: start_tool("HSV")).pack(pady=4)

    def show_tools_window(self):
        self.tools_win = tk.Toplevel(self.root)
        self.tools_win.title(f"Bảng Công Cụ Tools - [{self.active_color_name}]")
        self.tools_win.geometry("600x820")
        self.tools_win.resizable(False, False)

        tk.Label(self.tools_win, text=f"CÔNG CỤ BIẾN ĐỔI - {self.active_color_name.upper()}", font=("Arial", 12, "bold"), fg="#7B1FA2", pady=6).pack()

        self.frame_tool_canvas = tk.Frame(self.tools_win, bd=1, relief="solid")
        self.frame_tool_canvas.pack(pady=4)

        self.lbl_coord = tk.Label(self.tools_win, text="💡 Mẹo: Click chuột trực tiếp lên hình để chọn vị trí tâm Zoom", font=("Arial", 9, "italic"), fg="#2E7D32")
        self.lbl_coord.pack()

        # Độ sáng
        frame_bright = tk.LabelFrame(self.tools_win, text=" ☀️ Độ Sáng ", font=("Arial", 9, "bold"), padx=10, pady=2)
        frame_bright.pack(fill="x", padx=15, pady=3)

        self.brightness_slider = tk.Scale(frame_bright, from_=-100, to=100, orient="horizontal", length=520)
        self.brightness_slider.set(0)
        self.brightness_slider.pack()
        tk.Button(frame_bright, text="Áp Dụng Độ Sáng", bg="#00897B", fg="white", font=("Arial", 8, "bold"), command=self.apply_brightness).pack(pady=2)

        # Zoom
        frame_zoom = tk.LabelFrame(self.tools_win, text=" 🔍 Phóng To / Thu Nhỏ (Theo vị trí Click chuột) ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_zoom.pack(fill="x", padx=15, pady=3)

        btn_zoom_grid = tk.Frame(frame_zoom)
        btn_zoom_grid.pack()

        tk.Button(btn_zoom_grid, text="🔍 Phóng To 1.5x", width=18, bg="#00897B", fg="white", font=("Arial", 9, "bold"), command=lambda: self.tool_scale(1.5)).pack(side="left", padx=10)
        tk.Button(btn_zoom_grid, text="🔍 Thu Nhỏ 1.5x", width=18, bg="#00897B", fg="white", font=("Arial", 9, "bold"), command=lambda: self.tool_scale(1/1.5)).pack(side="left", padx=10)

        # Xoay ảnh (-360 đến 360 độ)
        frame_rotate = tk.LabelFrame(self.tools_win, text=" 🔄 Xoay Ảnh Theo Góc ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_rotate.pack(fill="x", padx=15, pady=3)

        frame_rot_controls = tk.Frame(frame_rotate)
        frame_rot_controls.pack()

        tk.Label(frame_rot_controls, text="Nhập hoặc chọn góc xoay (-360° đến 360°):", font=("Arial", 9)).pack(side="left", padx=5)
        
        self.spin_angle = tk.Spinbox(frame_rot_controls, from_=-360, to=360, increment=15, width=10, font=("Arial", 10))
        self.spin_angle.delete(0, "end")
        self.spin_angle.insert(0, "90")
        self.spin_angle.pack(side="left", padx=5)

        tk.Button(frame_rot_controls, text="🔄 Thực Hiện Xoay", bg="#5C6BC0", fg="white", font=("Arial", 9, "bold"), command=self.tool_rotate_custom).pack(side="left", padx=10)

        # Dịch chuyển
        frame_move = tk.LabelFrame(self.tools_win, text=" ↕️↔️ Dịch Chuyển Ảnh (4 Hướng) ", font=("Arial", 9, "bold"), padx=10, pady=5)
        frame_move.pack(fill="x", padx=15, pady=3)

        btn_grid = tk.Frame(frame_move)
        btn_grid.pack()

        tk.Button(btn_grid, text="⬆️ Lên 40px", width=13, bg="#7E57C2", fg="white", font=("Arial", 9, "bold"), command=lambda: self.tool_move(0, -40)).grid(row=0, column=1, padx=4, pady=2)
        tk.Button(btn_grid, text="⬅️ Trái 40px", width=13, bg="#7E57C2", fg="white", font=("Arial", 9, "bold"), command=lambda: self.tool_move(-40, 0)).grid(row=1, column=0, padx=4, pady=2)
        tk.Button(btn_grid, text="➡️ Phải 40px", width=13, bg="#7E57C2", fg="white", font=("Arial", 9, "bold"), command=lambda: self.tool_move(40, 0)).grid(row=1, column=2, padx=4, pady=2)
        tk.Button(btn_grid, text="⬇️ Xuống 40px", width=13, bg="#7E57C2", fg="white", font=("Arial", 9, "bold"), command=lambda: self.tool_move(0, 40)).grid(row=2, column=1, padx=4, pady=2)

        # NÚT RESET
        frame_reset = tk.Frame(self.tools_win, pady=4)
        frame_reset.pack()
        tk.Button(frame_reset, text="🔄 RESET ÁNH ĐANG CHỈNH", font=("Arial", 9, "bold"), bg="#C62828", fg="white", padx=15, pady=4, command=self.tool_reset).pack()

        # Hoàn tất
        tk.Button(
            self.tools_win, 
            text="✅ HOÀN THÀNH & LƯU ÁNH", 
            font=("Arial", 11, "bold"), 
            bg="#2E7D32", 
            fg="white", 
            pady=8, 
            padx=20, 
            command=self.finish_tools_and_save
        ).pack(pady=8)

        self.render_tool_preview()

    def on_image_click(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.selected_point = (int(event.xdata), int(event.ydata))
            self.lbl_coord.config(
                text=f"📍 Đã chọn tâm Zoom tại tọa độ: X={self.selected_point[0]}, Y={self.selected_point[1]}", 
                fg="#1565C0"
            )
            self.render_tool_preview()

    def render_tool_preview(self):
        for widget in self.frame_tool_canvas.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(4.8, 2.7))

        if len(self.active_tool_img.shape) == 3:
            img_disp = cv2.cvtColor(self.active_tool_img, cv2.COLOR_BGR2RGB)
            ax.imshow(img_disp)
        else:
            ax.imshow(self.active_tool_img, cmap='gray')

        if self.selected_point is not None:
            ax.plot(self.selected_point[0], self.selected_point[1], 'ro', markersize=7)

        ax.axis("off")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_tool_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack()

        fig.canvas.mpl_connect('button_press_event', self.on_image_click)

    def apply_brightness(self):
        val = self.brightness_slider.get()
        if val != 0:
            self.active_tool_img = cv2.addWeighted(self.active_tool_img, 1.0, np.zeros(self.active_tool_img.shape, self.active_tool_img.dtype), 0, val)
            self.brightness_slider.set(0)
            self.render_tool_preview()

    def tool_rotate_custom(self):
        """Xoay ảnh giữ nguyên tỉ lệ & kích thước (Không làm ảnh bị thu nhỏ)"""
        try:
            angle = float(self.spin_angle.get())
            if angle < -360 or angle > 360:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập góc từ -360° đến 360°!")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            return

        h, w = self.active_tool_img.shape[:2]
        center = (w / 2, h / 2)

        # Xoay chuẩn quanh tâm giữ nguyên kích thước không bị xén dồn
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.active_tool_img = cv2.warpAffine(self.active_tool_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        self.selected_point = None
        self.render_tool_preview()

    def tool_scale(self, factor):
        h, w = self.active_tool_img.shape[:2]

        if self.selected_point is not None:
            cx, cy = self.selected_point
        else:
            cx, cy = w // 2, h // 2

        interp = cv2.INTER_LANCZOS4 if factor > 1.0 else cv2.INTER_AREA

        if factor > 1.0:
            scaled = cv2.resize(self.active_tool_img, (int(w * factor), int(h * factor)), interpolation=interp)
            sh, sw = scaled.shape[:2]

            new_cx, new_cy = int(cx * factor), int(cy * factor)
            x1 = max(0, min(sw - w, new_cx - w // 2))
            y1 = max(0, min(sh - h, new_cy - h // 2))

            self.active_tool_img = scaled[y1:y1+h, x1:x1+w]
        else:
            scaled = cv2.resize(self.active_tool_img, (max(1, int(w * factor)), max(1, int(h * factor))), interpolation=interp)
            sh, sw = scaled.shape[:2]

            canvas = np.zeros_like(self.active_tool_img)
            x1 = (w - sw) // 2
            y1 = (h - sh) // 2

            canvas[y1:y1+sh, x1:x1+sw] = scaled
            self.active_tool_img = canvas

        self.selected_point = None
        self.lbl_coord.config(text="💡 Mẹo: Click chuột trực tiếp lên hình để chọn vị trí tâm Zoom", fg="#2E7D32")
        self.render_tool_preview()

    def tool_move(self, dx, dy):
        h, w = self.active_tool_img.shape[:2]
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        self.active_tool_img = cv2.warpAffine(self.active_tool_img, M, (w, h), flags=cv2.INTER_CUBIC)
        self.render_tool_preview()

    def tool_reset(self):
        """Reset chuẩn an toàn, giữ nguyên cửa sổ Tools"""
        if self.initial_tool_img is not None:
            self.active_tool_img = self.initial_tool_img.copy()
            self.selected_point = None
            self.brightness_slider.set(0)
            self.spin_angle.delete(0, "end")
            self.spin_angle.insert(0, "90")
            self.lbl_coord.config(text="💡 Mẹo: Click chuột trực tiếp lên hình để chọn vị trí tâm Zoom", fg="#2E7D32")
            
            # Vẽ lại giao diện mượt mà
            self.render_tool_preview()

    def finish_tools_and_save(self):
        self.img_bgr = self.active_tool_img.copy()
        self.update_color_spaces()
        self.render_3_color_spaces()
        self.tools_win.destroy()
        self.open_save_window()

    def open_save_window(self):
        save_win = tk.Toplevel(self.root)
        save_win.title("Lưu File Ảnh")
        save_win.geometry("380x180")
        save_win.grab_set()

        tk.Label(save_win, text="💾 LƯU FILE ÁNH CHẤT LƯỢNG CAO", font=("Arial", 11, "bold"), fg="#1565C0", pady=12).pack()

        frame_form = tk.Frame(save_win, padx=20)
        frame_form.pack(fill="x")

        tk.Label(frame_form, text="Chọn định dạng file:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=10)
        ext_combo = ttk.Combobox(frame_form, values=[".png", ".jpg", ".bmp", ".webp"], state="readonly", width=15)
        ext_combo.current(0)
        ext_combo.grid(row=0, column=1, padx=10, pady=10)

        def execute_save():
            selected_ext = ext_combo.get()
            def_name = f"anh_chinh_sua{selected_ext}"

            save_path = filedialog.asksaveasfilename(
                title="Chọn vị trí lưu file",
                initialfile=def_name,
                defaultextension=selected_ext,
                filetypes=[(f"File {selected_ext.upper()}", f"*{selected_ext}"), ("All files", "*.*")]
            )

            if save_path:
                params = []
                if selected_ext.lower() in ['.jpg', '.jpeg']:
                    params = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
                elif selected_ext.lower() == '.png':
                    params = [int(cv2.IMWRITE_PNG_COMPRESSION), 0]

                success = cv2.imwrite(save_path, self.img_bgr, params)
                if success:
                    messagebox.showinfo("Thành công", f"Đã lưu ảnh thành công tại:\n{save_path}")
                    save_win.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể lưu được ảnh!")

        tk.Button(save_win, text="💾 LƯU FILE ÁNH", font=("Arial", 11, "bold"), bg="#2E7D32", fg="white", pady=6, padx=20, command=execute_save).pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()