import streamlit as st
import datetime
import os

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & DỮ LIỆU MENU
# ---------------------------------------------------------
st.set_page_config(page_title="Tính Hóa Đơn Trà Sữa", page_icon="🧋", layout="centered")

# Hiển thị ảnh nếu file tồn tại trong thư mục
if os.path.exists("trasua.jpg"):
    st.image("trasua.jpg")

# Bảng giá Trà sữa (VNĐ)
MENU_TRA_SUA = {
    "Trà sữa Truyền thống": 30000,
    "Trà sữa Trân châu Đường đen": 35000,
    "Trà sữa Oolong": 38000,
    "Trà sữa Thái Xanh": 32000,
    "Trà Matcha Đậu đỏ": 40000,
    "Trà Đào Cam Sả": 35000
}

# Bảng giá Topping (VNĐ)
MENU_TOPPING = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

# Khởi tạo giỏ hàng trong session_state
if "gio_hang" not in st.session_state:
    st.session_state.gio_hang = []

# ---------------------------------------------------------
# 2. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 Quản Lý Hóa Đơn Quán Trà Sữa")
st.write("Nhập thông tin đơn hàng bên dưới để tính tiền và xuất hóa đơn.")

st.markdown("---")

# Thông tin khách hàng
st.subheader("1. Thông tin khách hàng")
ten_khach_hang = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách hàng...")

# Thông tin chọn đồ uống
st.subheader("2. Chọn món vào đơn hàng")

col1, col2 = st.columns(2)

with col1:
    loai_tra_sua = st.selectbox("Chọn loại trà sữa:", list(MENU_TRA_SUA.keys()))
    muc_duong = st.radio("Mức độ đường:", ["100%", "70%", "0%"], horizontal=True)

with col2:
    so_luong = st.number_input("Số lượng:", min_value=1, max_value=50, value=1, step=1)
    toppings = st.multiselect("Thêm Topping:", list(MENU_TOPPING.keys()))

# Tính toán giá món hiện tại đang chọn
don_gia_tra_sua = MENU_TRA_SUA[loai_tra_sua]
tong_tien_topping_1_ly = sum(MENU_TOPPING[top] for top in toppings)
don_gia_1_ly = don_gia_tra_sua + tong_tien_topping_1_ly
thanh_tien_mon = don_gia_1_ly * so_luong

# Nút Thêm vào đơn hàng
if st.button("➕ Thêm món này vào đơn", type="primary"):
    mon_moi = {
        "ten_mon": loai_tra_sua,
        "don_gia_mon": don_gia_tra_sua,
        "muc_duong": muc_duong,
        "toppings": toppings,
        "so_luong": so_luong,
        "thanh_tien": thanh_tien_mon
    }
    st.session_state.gio_hang.append(mon_moi)
    st.success(f"Đã thêm {so_luong} ly {loai_tra_sua} vào danh sách!")

st.markdown("---")

# ---------------------------------------------------------
# 3. HIỂN THỊ DANH SÁCH MÓN ĐÃ CHỌN & TỔNG TIỀN
# ---------------------------------------------------------
st.subheader("📋 Danh sách món đã chọn")

if not st.session_state.gio_hang:
    st.info("Chưa có món nào trong đơn hàng. Vui lòng chọn món và bấm 'Thêm món này vào đơn'.")
else:
    # Hiển thị từng món trong giỏ hàng
    tong_cong_hoa_don = 0
    
    for i, item in enumerate(st.session_state.gio_hang):
        tong_cong_hoa_don += item["thanh_tien"]
        topping_str = ", ".join(item["toppings"]) if item["toppings"] else "Không"
        
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(
                f"**{i+1}. {item['ten_mon']}** x **{item['so_luong']} ly** "
                f"({item['thanh_tien']:,} VNĐ)\n"
                f"- *Đường:* {item['muc_duong']} | *Topping:* {topping_str}"
            )
        with c2:
            if st.button("❌ Xóa", key=f"xoa_{i}"):
                st.session_state.gio_hang.pop(i)
                st.rerun()

    st.markdown("---")
    st.markdown(f"### **💰 TỔNG CỘNG THANH TOÁN: {tong_cong_hoa_don:,} VNĐ**")

    # ---------------------------------------------------------
    # 4. XUẤT HÓA ĐƠN RA FILE (.TXT)
    # ---------------------------------------------------------
    if not ten_khach_hang.strip():
        st.warning("⚠️ Vui lòng nhập tên khách hàng bên trên để tiến hành xuất hóa đơn.")
    else:
        thoi_gian_hien_tai = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Tạo chuỗi chi tiết từng món cho hóa đơn
        chi_tiet_mon_txt = ""
        for idx, item in enumerate(st.session_state.gio_hang, 1):
            top_txt = ", ".join(item["toppings"]) if item["toppings"] else "Không"
            chi_tiet_mon_txt += f"""
{idx}. {item['ten_mon']}
   - Số lượng: {item['so_luong']} ly
   - Đường: {item['muc_duong']}
   - Topping: {top_txt}
   - Thành tiền: {item['thanh_tien']:,} VNĐ
-----------------------------------"""

        # Nội dung file hóa đơn
        noi_dung_hoa_don = f"""===================================
        HÓA ĐƠN BÁN HÀNG
           QUÁN TRÀ SỮA
===================================
Thời gian: {thoi_gian_hien_tai}
Khách hàng: {ten_khach_hang}

-----------------------------------
CHI TIẾT ĐƠN HÀNG:{chi_tiet_mon_txt}
===================================
TỔNG CỘNG: {tong_cong_hoa_don:,} VNĐ
===================================
Cảm ơn quý khách và hẹn gặp lại!
"""

        col_pay1, col_pay2 = st.columns(2)
        
        with col_pay1:
            # Nút tải hóa đơn
            ten_file = f"HoaDon_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            st.download_button(
                label="💳 Thanh toán & Xuất hóa đơn (.txt)",
                data=noi_dung_hoa_don,
                file_name=ten_file,
                mime="text/plain",
                type="primary"
            )

        with col_pay2:
            # Nút hủy/làm mới đơn
            if st.button("🗑️ Xóa toàn bộ đơn hàng"):
                st.session_state.gio_hang = []
                st.rerun()
