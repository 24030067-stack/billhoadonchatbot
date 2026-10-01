import streamlit as st
import datetime
import io

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & DỮ LIỆU MENU
# ---------------------------------------------------------
st.set_page_config(page_title="Tính Hóa Đơn Trà Sữa", page_icon="🧋", layout="centered")

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

# ---------------------------------------------------------
# 2. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 Quản Lý Hóa Đơn Quán Trà Sữa")
st.write("Nhập thông tin đơn hàng bên dưới để tính tiền và xuất hóa đơn.")

st.markdown("---")

# Thông tin khách hàng
st.subheader("1. Thông tin khách hàng")
ten_khach_hang = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách hàng...")

# Thông tin đồ uống
st.subheader("2. Chi tiết món ăn")

col1, col2 = st.columns(2)

with col1:
    loai_tra_sua = st.selectbox("Chọn loại trà sữa:", list(MENU_TRA_SUA.keys()))
    muc_duong = st.radio("Mức độ đường:", ["100%", "70%", "0%"], horizontal=True)

with col2:
    so_luong = st.number_input("Số lượng:", min_value=1, max_value=50, value=1, step=1)
    toppings = st.multiselect("Thêm Topping:", list(MENU_TOPPING.keys()))

# ---------------------------------------------------------
# 3. TÍNH TOÁN CHI PHÍ
# ---------------------------------------------------------
don_gia_tra_sua = MENU_TRA_SUA[loai_tra_sua]
tong_tien_topping_1_ly = sum(MENU_TOPPING[top] for top in toppings)

don_gia_1_ly = don_gia_tra_sua + tong_tien_topping_1_ly
tong_tien = don_gia_1_ly * so_luong

st.markdown("---")

# ---------------------------------------------------------
# 4. HIỂN THỊ TỔNG QUAN HÓA ĐƠN
# ---------------------------------------------------------
st.subheader("📋 Tóm tắt đơn hàng")

if ten_khach_hang.strip() == "":
    st.warning("⚠️ Vui lòng nhập tên khách hàng để hoàn tất.")
else:
    # Hiển thị thông tin tóm tắt trên giao diện
    st.markdown(f"**Khách hàng:** {ten_khach_hang}")
    st.markdown(f"**Loại trà sữa:** {loai_tra_sua} ({don_gia_tra_sua:,} VNĐ)")
    st.markdown(f"**Mức đường:** {muc_duong}")
    
    if toppings:
        list_topping_str = ", ".join([f"{t} (+{MENU_TOPPING[t]:,} VNĐ)" for t in toppings])
        st.markdown(f"**Topping đi kèm:** {list_topping_str}")
    else:
        st.markdown("**Topping đi kèm:** Không chọn")
        
    st.markdown(f"**Số lượng:** {so_luong} ly")
    st.markdown(f"### **💰 Tổng tiền thanh toán: {tong_tien:,} VNĐ**")

    st.markdown("---")

    # ---------------------------------------------------------
    # 5. XUẤT HÓA ĐƠN RA FILE (.TXT)
    # ---------------------------------------------------------
    thoi_gian_ hien_tai = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Nội dung hóa đơn văn bản
    noi_dung_hoa_don = f"""===================================
        HÓA ĐƠN BÁN HÀNG
           QUÁN TRÀ SỮA
===================================
Thời gian: {thoi_gian_ hien_tai}
Khách hàng: {ten_khach_hang}

-----------------------------------
Món: {loai_tra_sua}
Đơn giá trà sữa: {don_gia_tra_sua:,} VNĐ
Mức đường: {muc_duong}
Topping: {', '.join(toppings) if toppings else 'Không có'}
Số lượng: {so_luong} ly
-----------------------------------
TỔNG TIỀN: {tong_tien:,} VNĐ
===================================
Cảm ơn quý khách và hẹn gặp lại!
"""

    # Nút bấm thanh toán & Xuất file
    st.download_button(
        label="💳 Thanh toán & Xuất hóa đơn (File .txt)",
        data=noi_dung_hoa_don,
        file_name=f"HoaDon_{ten_khach_hang.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        type="primary"
    )
