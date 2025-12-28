"""
Solar Monitoring Dashboard - Main Application
Ứng dụng chính với 2 chế độ:
1. Dashboard HTML (Real-time đơn giản)
2. Dashboard Streamlit (Phân tích nâng cao)

Author: Solar Monitoring System
"""

import streamlit as st

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Solar Panel Monitoring System",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CSS ==================
def apply_theme_css(theme='dark'):
    """Áp dụng CSS theo theme - Phiên bản chuyên nghiệp"""
    
    # Định nghĩa màu sắc theo theme
    if theme == 'light':
        # Theme sáng - Clean & Professional
        bg_gradient = "linear-gradient(135deg, #f0f4f8 0%, #ffffff 50%, #f0f4f8 100%)"
        sidebar_bg = "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"
        card_bg = "linear-gradient(145deg, #ffffff 0%, #f8fafc 100%)"
        card_shadow = "0 8px 25px -5px rgba(0, 0, 0, 0.08)"
        card_hover_shadow = "0 15px 35px -5px rgba(0, 0, 0, 0.12)"
        text_primary = "#1a202c"
        text_secondary = "#4a5568"
        text_muted = "#718096"
        border_color = "rgba(0, 0, 0, 0.08)"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        info_bg = "rgba(66, 153, 225, 0.1)"
    else:
        # Theme tối - Premium Dark
        bg_gradient = "linear-gradient(135deg, #0a0f1a 0%, #1a1f2e 50%, #0a0f1a 100%)"
        sidebar_bg = "linear-gradient(180deg, #1a1f2e 0%, #0a0f1a 100%)"
        card_bg = "linear-gradient(145deg, #1e2538 0%, #2d3548 100%)"
        card_shadow = "0 8px 25px -5px rgba(0, 0, 0, 0.4)"
        card_hover_shadow = "0 15px 35px -5px rgba(0, 0, 0, 0.5)"
        text_primary = "#f7fafc"
        text_secondary = "#a0aec0"
        text_muted = "#718096"
        border_color = "rgba(255, 255, 255, 0.06)"
        accent_gradient = "linear-gradient(135deg, #f59e0b 0%, #f97316 100%)"
        info_bg = "rgba(66, 153, 225, 0.15)"
    
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .stApp {{
        background: {bg_gradient};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    [data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}
    
    .welcome-header {{
        background: {accent_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.5px;
    }}
    
    .welcome-sub {{
        color: {text_muted};
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }}
    
    .mode-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }}
    
    .mode-card:hover {{
        transform: translateY(-4px);
        box-shadow: {card_hover_shadow};
        border-color: rgba(102, 126, 234, 0.5);
    }}
    
    .mode-icon {{
        font-size: 3rem;
        margin-bottom: 0.75rem;
    }}
    
    .mode-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 0.5rem;
    }}
    
    .mode-desc {{
        color: {text_secondary};
        font-size: 0.85rem;
        line-height: 1.5;
    }}
    
    .feature-list {{
        text-align: left;
        margin-top: 0.75rem;
        padding-left: 0.75rem;
    }}
    
    .feature-list li {{
        color: {text_secondary};
        margin: 0.35rem 0;
        font-size: 0.8rem;
    }}
    
    .feature-list li::marker {{
        color: #22c55e;
    }}
    
    /* Theme toggle styling */
    .theme-btn {{
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }}
    
    /* Info boxes */
    [data-testid="stAlert"] {{
        background: {info_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
</style>
""", unsafe_allow_html=True)

# Áp dụng theme CSS
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
apply_theme_css(st.session_state.theme)


def main():
    # Khởi tạo theme (mặc định dark)
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Welcome header
    st.markdown('<h1 class="welcome-header">☀️ Solar Panel Monitoring System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-sub">Hệ thống giám sát và phân tích hiệu suất pin mặt trời</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/solar-panel.png", width=80)
        # st.title("Chọn chế độ")
        
        # Theme toggle - Thêm vào đây
        st.markdown("---")
        st.markdown("### 🎨 Chuyển đổi giao diện")
        
        current_theme = st.session_state.theme
        if current_theme == 'dark':
            st.info("🌙 **Đang dùng:** Giao diện tối")
        else:
            st.info("☀️ **Đang dùng:** Giao diện sáng")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Tối", 
                        use_container_width=True, 
                        disabled=current_theme == 'dark',
                        type="secondary",
                        key="main_theme_dark"):
                st.session_state.theme = 'dark'
                st.rerun()
        with col2:
            if st.button("☀️ Sáng", 
                        use_container_width=True,
                        disabled=current_theme == 'light',
                        type="primary",
                        key="main_theme_light"):
                st.session_state.theme = 'light'
                st.rerun()
        
        st.markdown("---")
        
        mode = st.radio(
            "",
            ["🏠 Trang chủ", "📊 Dashboard Real-time", "🔬 Phân tích nâng cao"],
            index=0,
            label_visibility="collapsed"
        )
        
        # st.divider()
        
        # st.markdown("""
        # ### 📌 Hướng dẫn
        
        # **Dashboard Real-time:**
        # - Hiển thị dữ liệu trực tiếp
        # - Cập nhật tự động
        # - Giao diện nhẹ, nhanh
        
        # **Phân tích nâng cao:**
        # - Phân tích hiệu suất
        # - Phát hiện bất thường
        # - Báo cáo chi tiết
        # - So sánh lịch sử
        # """)
        
        st.divider()
        
        # st.markdown("""
        # ### 🔗 Liên kết
        # - [Firebase Console](https://console.firebase.google.com/)
        # - [Tài liệu hướng dẫn](./HUONG_DAN_CHAY.md)
        # """)
    
    # Main content based on mode
    if mode == "🏠 Trang chủ":
        show_home()
    elif mode == "📊 Dashboard Real-time":
        show_realtime_dashboard()
    else:
        show_advanced_analysis()


def show_home():
    """Trang chủ với lựa chọn chế độ"""
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">📊</div>
            <div class="mode-title">Dashboard Real-time</div>
            <div class="mode-desc">
                Giám sát dữ liệu cảm biến theo thời gian thực với giao diện nhẹ, tốc độ cao.
            </div>
            <ul class="feature-list">
                <li>Cập nhật tự động mỗi 10 giây</li>
                <li>Biểu đồ trực quan</li>
                <li>Xuất dữ liệu CSV</li>
                <li>Thống kê cơ bản</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Mở Dashboard Real-time", use_container_width=True, key="btn_realtime"):
            st.session_state['mode'] = 'realtime'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🔬</div>
            <div class="mode-title">Phân tích nâng cao</div>
            <div class="mode-desc">
                Phân tích hiệu suất chi tiết, phát hiện bất thường và dự báo suy giảm.
            </div>
            <ul class="feature-list">
                <li>Tính hiệu suất thực tế</li>
                <li>Phát hiện bất thường tự động</li>
                <li>Điểm sức khỏe tấm pin</li>
                <li>So sánh lịch sử</li>
                <li>Khuyến nghị bảo trì</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Mở Phân tích nâng cao", use_container_width=True, key="btn_analysis"):
            st.session_state['mode'] = 'analysis'
            st.rerun()
    
    # Thông tin hệ thống
    st.markdown("---")
    st.subheader("📋 Thông tin hệ thống")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔌 Phần cứng**
        - Node cảm biến LoRa
        - Cảm biến INA219 (V, I, P)
        - Cảm biến BH1750 (Lux)
        - Cảm biến DHT22 (T, H)
        """)
    
    with col2:
        st.info("""
        **☁️ Backend**
        - Firebase Realtime Database
        - Cập nhật real-time
        - Lưu trữ lịch sử
        """)
    
    with col3:
        st.info("""
        **📊 Phân tích**
        - Hiệu suất PV
        - Performance Ratio
        - Phát hiện bất thường
        - Xu hướng suy giảm
        """)
    
    # Công thức tính toán
    st.markdown("---")
    st.subheader("📐 Công thức tính toán")
    
    with st.expander("Xem các công thức phân tích", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Hiệu suất chuyển đổi (η):**
            
            $$η = \\frac{P_{output}}{G \\times A} \\times 100\\%$$
            
            Trong đó:
            - $P_{output}$: Công suất đầu ra (W)
            - $G$: Bức xạ mặt trời (W/m²)
            - $A$: Diện tích tấm pin (m²)
            """)
        
        with col2:
            st.markdown("""
            **Công suất kỳ vọng:**
            
            $$P_{expected} = P_{rated} \\times \\frac{G}{G_{STC}} \\times [1 + α(T - T_{STC})]$$
            
            Trong đó:
            - $P_{rated}$: Công suất định mức (W)
            - $G_{STC}$: Bức xạ chuẩn (1000 W/m²)
            - $α$: Hệ số nhiệt độ (%/°C)
            - $T_{STC}$: Nhiệt độ chuẩn (25°C)
            """)
        
        st.markdown("""
        **Performance Ratio (PR):**
        
        $$PR = \\frac{P_{actual}}{P_{expected}} \\times 100\\%$$
        
        **Đánh giá PR:**
        - PR > 80%: Tốt
        - 70% < PR < 80%: Chấp nhận được
        - PR < 70%: Cần kiểm tra
        - PR < 50%: Bất thường nghiêm trọng
        """)


def show_realtime_dashboard():
    """Hiển thị dashboard real-time (HTML embed)"""
    import streamlit.components.v1 as components
    
    # Ẩn các elements không cần thiết
    st.markdown("""
    <style>
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        components.html(html_content, height=2000, scrolling=True)
    except FileNotFoundError:
        st.error("Không tìm thấy file index.html. Vui lòng kiểm tra lại.")


def show_advanced_analysis():
    """Hiển thị phân tích nâng cao"""
    # Import và chạy dashboard nâng cao
    try:
        import dashboard
        dashboard.main()
    except ImportError as e:
        st.error(f"Lỗi import dashboard: {e}")
        st.info("Đang chuyển sang chế độ inline...")
        
        # Fallback: chạy inline nếu import lỗi
        run_inline_analysis()
    except FileNotFoundError as e:
        # Lỗi Firebase credentials
        if "firebase-key.json" in str(e) or "Firebase credentials" in str(e):
            st.error(f"❌ **Lỗi cấu hình Firebase**: {e}")
            st.info("""
            **Hướng dẫn khắc phục:**
            
            1. **Nếu chạy trên Streamlit Cloud:**
               - Vào **Settings** → **Secrets**
               - Thêm cấu hình Firebase (xem `HUONG_DAN_STREAMLIT_SECRETS.md`)
            
            2. **Nếu chạy local:**
               - Đảm bảo file `firebase-key.json` có trong thư mục dự án
            
            3. **Xem chi tiết:** Mở file `HUONG_DAN_STREAMLIT_SECRETS.md`
            """)
        else:
            st.error(f"Lỗi: {e}")
    except Exception as e:
        # Bất kỳ lỗi nào khác
        st.error(f"Lỗi không xác định: {e}")
        st.info("Đang chuyển sang chế độ inline...")
        run_inline_analysis()


def init_firebase_credentials():
    """Khởi tạo Firebase credentials từ secrets hoặc file"""
    import os
    import firebase_admin
    from firebase_admin import credentials
    
    if not firebase_admin._apps:
        # Ưu tiên dùng Streamlit secrets (cho production/cloud)
        # Fallback về file local (cho development)
        try:
            if 'firebase' in st.secrets:
                # Lấy credentials từ Streamlit secrets
                firebase_config = st.secrets['firebase']
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": firebase_config.get("project_id", ""),
                    "private_key_id": firebase_config.get("private_key_id", ""),
                    "private_key": firebase_config.get("private_key", "").replace('\\n', '\n'),
                    "client_email": firebase_config.get("client_email", ""),
                    "client_id": firebase_config.get("client_id", ""),
                    "auth_uri": firebase_config.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                    "token_uri": firebase_config.get("token_uri", "https://oauth2.googleapis.com/token"),
                    "auth_provider_x509_cert_url": firebase_config.get("auth_provider_x509_cert_url", ""),
                    "client_x509_cert_url": firebase_config.get("client_x509_cert_url", "")
                })
                database_url = firebase_config.get('databaseURL', 'https://nlmt-duy-default-rtdb.firebaseio.com')
            elif os.path.exists("firebase-key.json"):
                # Fallback: dùng file local nếu có (cho development)
                cred = credentials.Certificate("firebase-key.json")
                database_url = 'https://nlmt-duy-default-rtdb.firebaseio.com'
            else:
                raise FileNotFoundError(
                    "Không tìm thấy Firebase credentials. "
                    "Vui lòng cấu hình trong Streamlit secrets hoặc đặt file firebase-key.json"
                )
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            return True
        except FileNotFoundError:
            # Re-raise để xử lý ở tầng trên
            raise
        except Exception as e:
            # Bất kỳ lỗi nào khác
            raise Exception(f"Lỗi khởi tạo Firebase: {e}")
    return True

def run_inline_analysis():
    """Chạy phân tích nội tuyến nếu import dashboard thất bại"""
    import pandas as pd
    import firebase_admin
    from firebase_admin import db
    from datetime import datetime
    
    st.subheader("🔬 Phân tích nâng cao (Chế độ nội tuyến)")
    
    # Khởi tạo Firebase
    try:
        init_firebase_credentials()
    except FileNotFoundError as e:
        st.error(f"❌ **Lỗi cấu hình Firebase**: {e}")
        st.info("""
        **Hướng dẫn khắc phục:**
        
        1. **Nếu chạy trên Streamlit Cloud:**
           - Vào **Settings** → **Secrets**
           - Thêm cấu hình Firebase (xem `HUONG_DAN_STREAMLIT_SECRETS.md`)
        
        2. **Nếu chạy local:**
           - Đảm bảo file `firebase-key.json` có trong thư mục dự án
        
        3. **Xem chi tiết:** Mở file `HUONG_DAN_STREAMLIT_SECRETS.md`
        """)
        return
    except Exception as e:
        st.error(f"❌ **Lỗi kết nối Firebase**: {e}")
        st.info("Kiểm tra lại credentials và kết nối mạng.")
        return
    
    # Chọn thời gian
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Chọn ngày", value=datetime.now().date())
    with col2:
        hour = st.slider("Chọn giờ", 0, 23, datetime.now().hour)
    
    if st.button("📊 Phân tích", use_container_width=True, key="inline_analysis_btn"):
        with st.spinner("Đang phân tích..."):
            try:
                # Lấy dữ liệu
                hour_str = str(hour).zfill(2)
                ref = db.reference(f'/sensor_data/{date}/{hour_str}')
                data = ref.get()
                
                if not data:
                    st.warning("Không có dữ liệu cho thời gian đã chọn")
                    return
                
                # Chuyển đổi thành DataFrame
                records = []
                for time_key, values in data.items():
                    records.append({
                        'time': time_key,
                        'U': values.get('U', 0),
                        'Current': values.get('Current', 0),
                        'milliWatt': values.get('milliWatt', 0),
                        'Lux': values.get('Lux', 0),
                        'Temp': values.get('Temp', 0),
                        'Humi': values.get('Humi', 0)
                    })
                
                df = pd.DataFrame(records)
                
                # Hiển thị thống kê
                st.subheader("📈 Thống kê")
                col1, col2, col3 = st.columns(3)
                col1.metric("Số bản ghi", len(df))
                col2.metric("Công suất TB", f"{df['milliWatt'].mean():.1f} mW")
                col3.metric("Nhiệt độ TB", f"{df['Temp'].mean():.1f} °C")
                
                # Hiển thị dữ liệu
                st.subheader("📋 Dữ liệu chi tiết")
                st.dataframe(df, use_container_width=True)
                
            except Exception as e:
                st.error(f"Lỗi phân tích: {e}")


if __name__ == "__main__":
    main()
