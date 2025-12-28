"""
Solar Monitoring Dashboard - Advanced Version
Giao diện web nâng cao với phân tích hiệu suất và phát hiện bất thường

Features:
1. Giám sát real-time
2. Phân tích hiệu suất từng tấm pin
3. Phát hiện bất thường và cảnh báo
4. Phân tích lịch sử (ngày/tuần/tháng)
5. Báo cáo và xuất dữ liệu
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import json
import numpy as np
import os
from analysis import SolarPanelAnalyzer, PanelSpecs, AlertLevel


def apply_custom_css(theme='dark'):
    """Áp dụng CSS tùy chỉnh với hỗ trợ dark/light mode - Phiên bản chuyên nghiệp"""
    
    # Lưu theme vào session state để các function khác sử dụng
    st.session_state.current_theme = theme
    
    # Định nghĩa màu sắc theo theme
    if theme == 'light':
        # Theme sáng - Professional Light (dễ đọc, contrast tốt)
        bg_gradient = "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)"
        sidebar_bg = "linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%)"
        card_bg = "#ffffff"
        card_shadow = "0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)"
        card_hover_shadow = "0 8px 25px rgba(0, 0, 0, 0.12)"
        text_primary = "#0f172a"  # Đậm hơn để dễ đọc
        text_secondary = "#334155"  # Đậm hơn
        text_muted = "#64748b"
        border_color = "#e2e8f0"
        accent_gradient = "linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)"
        chart_text_color = "#334155"
        chart_grid_color = "rgba(51, 65, 85, 0.1)"
    else:
        # Theme tối - Premium Dark (dễ nhìn ban đêm)
        bg_gradient = "linear-gradient(180deg, #0f172a 0%, #1e293b 100%)"
        sidebar_bg = "linear-gradient(180deg, #1e293b 0%, #0f172a 100%)"
        card_bg = "#1e293b"
        card_shadow = "0 2px 8px rgba(0, 0, 0, 0.3)"
        card_hover_shadow = "0 8px 25px rgba(0, 0, 0, 0.4)"
        text_primary = "#f1f5f9"
        text_secondary = "#cbd5e1"
        text_muted = "#94a3b8"
        border_color = "#334155"
        accent_gradient = "linear-gradient(135deg, #f59e0b 0%, #f97316 100%)"
        chart_text_color = "#cbd5e1"
        chart_grid_color = "rgba(148, 163, 184, 0.15)"
    
    st.markdown(f"""
<style>
    /* ===== BASE THEME: {theme.upper()} ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    .stApp {{
        background: {bg_gradient};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: {text_secondary};
    }}
    
    /* Header styling */
    .main-header {{
        background: {accent_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
        padding: 0.5rem 0;
        letter-spacing: -0.5px;
    }}
    
    .sub-header {{
        color: {text_muted};
        text-align: center;
        font-size: 0.95rem;
        margin-top: -5px;
        margin-bottom: 1.5rem;
    }}
    
    /* ===== METRIC CARDS - ỔN ĐỊNH ===== */
    .metric-container {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 1rem 1.2rem;
        box-shadow: {card_shadow};
        transition: box-shadow 0.3s ease, transform 0.3s ease;
        min-height: 80px;
    }}
    
    .metric-container:hover {{
        transform: translateY(-2px);
        box-shadow: {card_hover_shadow};
    }}
    
    .metric-label {{
        color: {text_muted};
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }}
    
    .metric-value {{
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
    }}
    
    .metric-value.green {{ color: #22c55e; }}
    .metric-value.blue {{ color: #3b82f6; }}
    .metric-value.orange {{ color: #f97316; }}
    .metric-value.purple {{ color: #a855f7; }}
    .metric-value.yellow {{ color: #facc15; }}
    .metric-value.red {{ color: #ef4444; }}
    .metric-value.cyan {{ color: #06b6d4; }}
    
    /* Alert cards */
    .alert-card {{
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        border-left: 4px solid;
    }}
    
    .alert-warning {{
        background: rgba(250, 204, 21, 0.1);
        border-left-color: #facc15;
    }}
    
    .alert-critical {{
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #ef4444;
    }}
    
    .alert-normal {{
        background: rgba(34, 197, 94, 0.1);
        border-left-color: #22c55e;
    }}
    
    /* Health score circle */
    .health-score {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0 auto;
    }}
    
    .health-a {{ background: linear-gradient(135deg, #22c55e, #16a34a); color: white; }}
    .health-b {{ background: linear-gradient(135deg, #84cc16, #65a30d); color: white; }}
    .health-c {{ background: linear-gradient(135deg, #facc15, #eab308); color: #1e293b; }}
    .health-d {{ background: linear-gradient(135deg, #f97316, #ea580c); color: white; }}
    .health-f {{ background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {'rgba(241, 245, 249, 0.8)' if theme == 'light' else 'rgba(30, 41, 59, 0.8)'};
        border-radius: 10px;
        padding: 10px 20px;
        color: {text_secondary};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Data status indicators */
    .data-status {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }}
    
    .data-status.live {{
        background: rgba(34, 197, 94, 0.2);
        color: #16a34a;
    }}
    
    .data-status.stale {{
        background: rgba(250, 204, 21, 0.2);
        color: #ca8a04;
    }}
    
    .data-status.no-data {{
        background: rgba(239, 68, 68, 0.2);
        color: #dc2626;
    }}
    
    /* ===== CHART CONTAINERS - FIXED SIZE ===== */
    [data-testid="stPlotlyChart"] {{
        max-height: 400px !important;
        overflow: hidden !important;
    }}
    
    [data-testid="stPlotlyChart"] > div {{
        max-height: 400px !important;
    }}
    
    /* Responsive text for light theme */
    {'[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color: ' + text_primary + ' !important; }' if theme == 'light' else ''}
    
    /* Better metric styling */
    [data-testid="stMetricValue"] {{
        color: {text_primary} !important;
        font-weight: 700;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {text_muted} !important;
    }}
    
    /* Info/Warning/Error boxes */
    .stAlert {{
        border-radius: 12px;
    }}
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
    }}
</style>
""", unsafe_allow_html=True)


# ================== KHỞI TẠO FIREBASE ==================
def init_firebase():
    """Khởi tạo kết nối Firebase - Hỗ trợ Streamlit Secrets và file local
    
    Không dùng @st.cache_resource vì cần kiểm tra mỗi lần xem đã init chưa
    """
    try:
        # Kiểm tra xem Firebase đã được khởi tạo chưa (có thể từ app.py)
        if firebase_admin._apps:
            return True
        
        # Chưa khởi tạo - cần khởi tạo mới
        # Kiểm tra Streamlit secrets TRƯỚC (cho production/cloud)
        has_secrets = False
        try:
            has_secrets = 'firebase' in st.secrets and st.secrets['firebase'] is not None
        except:
            pass
        
        if has_secrets:
            try:
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
            except Exception as secrets_error:
                if os.path.exists("firebase-key.json"):
                    cred = credentials.Certificate("firebase-key.json")
                    database_url = 'https://nlmt-duy-default-rtdb.firebaseio.com'
                else:
                    raise FileNotFoundError(f"Lỗi đọc Streamlit secrets: {secrets_error}")
        elif os.path.exists("firebase-key.json"):
            cred = credentials.Certificate("firebase-key.json")
            database_url = 'https://nlmt-duy-default-rtdb.firebaseio.com'
        else:
            raise FileNotFoundError("Không tìm thấy Firebase credentials")
        
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})
        return True
        
    except FileNotFoundError as e:
        st.error(f"❌ **Lỗi cấu hình Firebase**: {e}")
        st.info("""
        **Hướng dẫn khắc phục:**
        1. **Streamlit Cloud:** Vào **Settings** → **Secrets** → Thêm cấu hình Firebase
        2. **Local:** Đảm bảo file `firebase-key.json` có trong thư mục dự án
        """)
        return False
    except Exception as e:
        st.error(f"❌ **Lỗi kết nối Firebase**: {e}")
        return False


# ================== XỬ LÝ DỮ LIỆU 0 ==================
def clean_zero_data(df: pd.DataFrame, method: str = 'auto_fill', last_valid_values: dict = None) -> pd.DataFrame:
    """
    Xử lý dữ liệu 0 không hợp lý từ Firebase - Forward fill tự động cho tất cả giá trị 0
    
    Args:
        df: DataFrame chứa dữ liệu
        method: Phương pháp xử lý
            - 'auto_fill': Tự động forward fill tất cả giá trị 0 (mặc định)
            - 'none': Không xử lý
            - 'smart': Chỉ xử lý khi có ánh sáng nhưng công suất = 0
        last_valid_values: Dict chứa giá trị hợp lệ cuối cùng để forward fill
    
    Returns:
        DataFrame đã được xử lý
    """
    if df.empty:
        return df
    
    df_cleaned = df.copy()
    
    # Nếu method = 'none', trả về dữ liệu gốc
    if method == 'none':
        return df_cleaned
    
    # Ngưỡng để xác định giá trị 0 không hợp lý
    zero_thresholds = {
        'U': 0.1,
        'Current': 0.001,
        'milliWatt': 1.0,
        'Lux': 0,
        'Temp': -10,
        'Humi': 0,
    }
    
    # Xử lý theo phương pháp
    if method == 'auto_fill':
        # Tự động forward fill TẤT CẢ giá trị 0 hoặc <= threshold
        for col in ['U', 'Current', 'milliWatt', 'Lux', 'Temp', 'Humi']:
            if col not in df_cleaned.columns:
                continue
            
            threshold = zero_thresholds.get(col, 0)
            
            # Đánh dấu các giá trị cần thay thế
            if col in ['U', 'Current', 'milliWatt']:
                # Với điện áp/dòng/công suất: thay thế nếu <= threshold
                mask = df_cleaned[col] <= threshold
            elif col == 'Lux':
                # Lux: chỉ thay thế nếu = 0 và có công suất (không hợp lý)
                if 'milliWatt' in df_cleaned.columns:
                    mask = (df_cleaned[col] <= threshold) & (df_cleaned['milliWatt'] > 10)
                else:
                    mask = df_cleaned[col] <= threshold
            elif col == 'Temp':
                # Temp: thay thế nếu <= -10 hoặc = 0
                mask = (df_cleaned[col] <= threshold) | (df_cleaned[col] == 0)
            elif col == 'Humi':
                # Humi: thay thế nếu = 0
                mask = df_cleaned[col] <= threshold
            else:
                mask = pd.Series([False] * len(df_cleaned))
            
            if mask.any():
                # Forward fill từ giá trị hợp lệ trước đó
                df_cleaned.loc[mask, col] = np.nan
                df_cleaned[col] = df_cleaned[col].fillna(method='ffill')
                
                # Nếu vẫn còn NaN ở đầu, dùng giá trị từ last_valid_values hoặc backward fill
                if df_cleaned[col].isna().any():
                    if last_valid_values and col in last_valid_values:
                        df_cleaned[col] = df_cleaned[col].fillna(last_valid_values[col])
                    else:
                        df_cleaned[col] = df_cleaned[col].fillna(method='bfill')
    
    elif method == 'smart':
        # Chỉ xử lý khi có ánh sáng nhưng công suất = 0
        invalid_masks = {}
        for col in ['U', 'Current', 'milliWatt', 'Lux', 'Temp', 'Humi']:
            if col not in df_cleaned.columns:
                continue
            
            threshold = zero_thresholds.get(col, 0)
            invalid_mask = pd.Series([False] * len(df_cleaned))
            
            if col in ['U', 'Current', 'milliWatt']:
                if 'Lux' in df_cleaned.columns:
                    invalid_mask = (df_cleaned[col] <= threshold) & (df_cleaned['Lux'] > 100)
                else:
                    invalid_mask = df_cleaned[col] <= threshold
            elif col == 'Lux':
                if 'milliWatt' in df_cleaned.columns:
                    invalid_mask = (df_cleaned[col] <= threshold) & (df_cleaned['milliWatt'] > 10)
            elif col == 'Temp':
                invalid_mask = (df_cleaned[col] <= threshold) | ((df_cleaned[col] == 0) & (df_cleaned.get('Lux', 0) > 100))
            elif col == 'Humi':
                invalid_mask = df_cleaned[col] <= threshold
            
            if invalid_mask.any():
                df_cleaned.loc[invalid_mask, col] = np.nan
                df_cleaned[col] = df_cleaned[col].fillna(method='ffill')
                if df_cleaned[col].isna().any():
                    if last_valid_values and col in last_valid_values:
                        df_cleaned[col] = df_cleaned[col].fillna(last_valid_values[col])
                    else:
                        df_cleaned[col] = df_cleaned[col].fillna(method='bfill')
    
    return df_cleaned


def get_data_status(df: pd.DataFrame, connection_timeout: float = 10.0) -> tuple[str, bool]:
    """
    Xác định trạng thái dữ liệu và kiểm tra mất kết nối
    
    Args:
        df: DataFrame chứa dữ liệu
        connection_timeout: Thời gian timeout (giây) để coi là mất kết nối (mặc định 10s)
    
    Returns:
        (status, is_connected): 
        - status: 'live', 'stale', 'no_data', 'disconnected'
        - is_connected: True nếu còn kết nối, False nếu mất kết nối (>10s không có dữ liệu mới)
    """
    if df.empty:
        return 'no_data', False
    
    # Kiểm tra thời gian cập nhật - QUAN TRỌNG NHẤT
    now = datetime.now()
    last_update = None
    
    # Tìm thời gian cập nhật mới nhất
    if 'datetime' in df.columns:
        last_update = df['datetime'].max()
    elif 'time' in df.columns and not df.empty:
        # Nếu chỉ có 'time', cố gắng parse
        try:
            date_str = str(datetime.now().date())
            last_time_str = df['time'].iloc[-1]
            last_update = datetime.strptime(f"{date_str} {last_time_str}", "%Y-%m-%d %H:%M:%S")
        except:
            pass
    
    # Nếu không tìm thấy thời gian cập nhật, coi như mất kết nối
    if last_update is None:
        return 'disconnected', False
    
    # Tính thời gian chênh lệch
    time_diff = (now - last_update).total_seconds()
    
    # MẤT KẾT NỐI nếu không có dữ liệu mới trong connection_timeout giây
    if time_diff > connection_timeout:
        return 'disconnected', False
    
    # Kiểm tra dữ liệu mới nhất
    latest = df.iloc[-1]
    
    # Nếu có nhiều giá trị 0 không hợp lý
    zero_count = 0
    if latest.get('U', 0) <= 0.1:
        zero_count += 1
    if latest.get('Current', 0) <= 0.001:
        zero_count += 1
    if latest.get('milliWatt', 0) <= 1.0:
        zero_count += 1
    if latest.get('Temp', 0) <= 0:
        zero_count += 1
    if latest.get('Humi', 0) <= 0:
        zero_count += 1
    
    # Nếu có ánh sáng nhưng không có công suất
    if latest.get('Lux', 0) > 100 and latest.get('milliWatt', 0) <= 1.0:
        return 'stale', True
    
    if zero_count >= 3:  # Nếu có >= 3 giá trị = 0
        return 'stale', True
    
    return 'live', True


# ================== HÀM LẤY DỮ LIỆU ==================
# Tắt cache để đảm bảo luôn lấy dữ liệu mới nhất từ Firebase (giống index.html)
def fetch_data_for_hour(date: str, hour: int, clean_method: str = 'auto_fill') -> pd.DataFrame:
    """
    Lấy dữ liệu từ Firebase cho một giờ cụ thể
    Cache 1s để tránh gọi Firebase liên tục nhưng vẫn cập nhật real-time
    
    Args:
        date: Ngày theo format YYYY-MM-DD (ví dụ: "2025-12-28")
        hour: Giờ từ 0-23
        clean_method: Phương pháp làm sạch dữ liệu (không dùng ở đây)
    
    Returns:
        DataFrame chứa dữ liệu hoặc DataFrame rỗng nếu không có dữ liệu
    """
    try:
        # Đảm bảo format đúng: date phải là YYYY-MM-DD, hour phải là 00-23 (GIỐNG HỆT index.html)
        if isinstance(date, datetime):
            date_str = date.strftime("%Y-%m-%d")
        elif hasattr(date, 'strftime'):
            date_str = date.strftime("%Y-%m-%d")
        else:
            date_str = str(date).strip()
        
        # Đảm bảo hour là số nguyên và format đúng (giống index.html: String(hourInput).padStart(2, '0'))
        hour_int = int(hour) if hour is not None else datetime.now().hour
        hour_str = str(hour_int).zfill(2)  # padStart(2, '0') trong JS = zfill(2) trong Python
        
        firebase_path = f'/sensor_data/{date_str}/{hour_str}'
        
        # Lấy dữ liệu từ Firebase
        ref = db.reference(firebase_path)
        data = ref.get()
        
        if not data:
            return pd.DataFrame()
        
        records = []
        for time_key, values in data.items():
            try:
                # Xử lý timestamp - GIỐNG HỆT index.html (không sort, chỉ parse)
                # index.html không parse datetime, chỉ dùng time_key
                try:
                    # Thử parse với format có milliseconds
                    if '.' in time_key:
                        dt = datetime.strptime(f"{date_str} {time_key}", "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        dt = datetime.strptime(f"{date_str} {time_key}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # Fallback: parse format cơ bản
                    try:
                        dt = datetime.strptime(f"{date_str} {time_key}", "%Y-%m-%d %H:%M:%S")
                    except:
                        # Nếu vẫn lỗi, dùng thời gian hiện tại
                        dt = datetime.now()
                
                # Parse dữ liệu - GIỐNG HỆT index.html
                # index.html: record.U = record.U || 0
                record = {
                    'time': time_key,
                    'datetime': dt,
                    'U': float(values.get('U', 0) or 0),
                    'Current': float(values.get('Current', 0) or 0),
                    'milliWatt': float(values.get('milliWatt', 0) or 0),
                    'energy': float(values.get('energy', 0) or 0),
                    'Lux': float(values.get('Lux', 0) or 0),
                    'Temp': float(values.get('Temp', 0) or 0),
                    'Humi': float(values.get('Humi', 0) or 0)
                }
                records.append(record)
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                # Log lỗi để debug (chỉ trong development)
                continue  # Bỏ qua record lỗi
        
        if not records:
            return pd.DataFrame()
            
        df = pd.DataFrame(records)
        # Sắp xếp theo datetime để đảm bảo thứ tự đúng
        df = df.sort_values('datetime').reset_index(drop=True)
        
        return df
    except Exception as e:
        # Log lỗi để debug (chỉ trong development)
        import traceback
        error_msg = f"Lỗi khi lấy dữ liệu từ Firebase: {str(e)}"
        # Không hiển thị lỗi ở đây để tránh spam - sẽ xử lý ở tầng view
        return pd.DataFrame()


def get_stable_latest_data(df: pd.DataFrame, clean_method: str = 'auto_fill') -> dict:
    """
    Lấy dữ liệu mới nhất ỔN ĐỊNH - không bị nhấp nháy về 0
    
    Vì các thông số được gửi lệch nhau trong cùng 1 giây, hàm này sẽ:
    1. Lấy giá trị MỚI NHẤT KHÔNG PHẢI 0 của từng thông số riêng biệt
    2. Nếu không có giá trị hợp lệ, dùng giá trị từ session state
    3. Đảm bảo mỗi thông số luôn có giá trị ổn định
    """
    if df.empty:
        return None
    
    # Khởi tạo session state
    if 'last_valid_values' not in st.session_state:
        st.session_state.last_valid_values = {}
    
    # Định nghĩa ngưỡng hợp lệ cho từng thông số
    valid_thresholds = {
        'U': 0.1,
        'Current': 0.001,
        'milliWatt': 1.0,
        'Lux': -1,  # Lux có thể = 0 (ban đêm)
        'Temp': -10,  # Temp có thể âm nhưng không nên quá thấp
        'Humi': 0,  # Humi không nên = 0
        'energy': 0  # Energy tích lũy, có thể = 0
    }
    
    # Khởi tạo dict kết quả
    latest = {}
    
    # Với mỗi thông số, tìm giá trị mới nhất hợp lệ
    for col in ['U', 'Current', 'milliWatt', 'energy', 'Lux', 'Temp', 'Humi']:
        if col not in df.columns:
            # Nếu không có cột, dùng giá trị từ session state
            latest[col] = st.session_state.last_valid_values.get(col, 0.0)
            continue
        
        threshold = valid_thresholds.get(col, 0)
        
        # Tìm giá trị mới nhất hợp lệ (từ cuối lên đầu)
        valid_value = None
        for idx in range(len(df) - 1, -1, -1):
            val = df.iloc[idx][col]
            
            # Kiểm tra giá trị có hợp lệ không
            if col == 'Lux':
                # Lux: bất kỳ giá trị nào cũng hợp lệ (có thể = 0 ban đêm)
                valid_value = val
                break
            elif col == 'Temp':
                # Temp: > threshold (ví dụ > -10)
                if val > threshold:
                    valid_value = val
                    break
            elif col == 'energy':
                # Energy: bất kỳ giá trị nào (có thể = 0)
                valid_value = val
                break
            else:
                # Các thông số khác: > threshold
                if val > threshold:
                    valid_value = val
                    break
        
        # Nếu tìm thấy giá trị hợp lệ
        if valid_value is not None:
            latest[col] = valid_value
            # Cập nhật session state
            st.session_state.last_valid_values[col] = valid_value
        else:
            # Không tìm thấy giá trị hợp lệ, dùng giá trị từ session state
            if col in st.session_state.last_valid_values:
                latest[col] = st.session_state.last_valid_values[col]
            else:
                # Nếu chưa có trong session state, dùng 0 hoặc giá trị mặc định
                if col == 'energy':
                    latest[col] = df.iloc[-1].get(col, 0.0)  # Energy giữ nguyên
                else:
                    latest[col] = 0.0
    
    # Đảm bảo có datetime và time từ bản ghi mới nhất
    if not df.empty:
        if 'datetime' in df.columns:
            latest['datetime'] = df.iloc[-1]['datetime']
        if 'time' in df.columns:
            latest['time'] = df.iloc[-1]['time']
        else:
            # Nếu không có 'time', tạo từ datetime hoặc dùng giá trị mặc định
            if 'datetime' in latest:
                latest['time'] = latest['datetime'].strftime("%H:%M:%S")
            else:
                latest['time'] = datetime.now().strftime("%H:%M:%S")
    else:
        # Nếu DataFrame rỗng, dùng thời gian hiện tại
        now = datetime.now()
        latest['datetime'] = now
        latest['time'] = now.strftime("%H:%M:%S")
    
    return latest


def fetch_data_for_day(date: str) -> pd.DataFrame:
    """Lấy dữ liệu cả ngày"""
    all_data = []
    for hour in range(24):
        df = fetch_data_for_hour(date, hour)
        if not df.empty:
            all_data.append(df)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def fetch_data_for_range(start_date: str, end_date: str) -> pd.DataFrame:
    """Lấy dữ liệu trong khoảng thời gian"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    all_data = []
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        df = fetch_data_for_day(date_str)
        if not df.empty:
            df['date'] = date_str
            all_data.append(df)
        current += timedelta(days=1)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


# ================== HÀM VẼ BIỂU ĐỒ ==================
def create_realtime_gauge(value: float, title: str, min_val: float, max_val: float, 
                          color: str, unit: str) -> go.Figure:
    """Tạo gauge chart cho giá trị real-time"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#94a3b8'}},
        number={'suffix': f" {unit}", 'font': {'size': 24, 'color': color}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': '#64748b'},
            'bar': {'color': color},
            'bgcolor': '#1e293b',
            'borderwidth': 0,
            'steps': [
                {'range': [min_val, max_val * 0.3], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [max_val * 0.3, max_val * 0.7], 'color': 'rgba(250, 204, 21, 0.2)'},
                {'range': [max_val * 0.7, max_val], 'color': 'rgba(34, 197, 94, 0.2)'}
            ],
        }
    ))
    
    colors_theme = get_chart_colors()
    fig.update_layout(
        paper_bgcolor=colors_theme['bg'],
        plot_bgcolor=colors_theme['bg'],
        font={'color': colors_theme['text']},
        height=180,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def get_chart_colors():
    """Lấy màu sắc cho biểu đồ theo theme hiện tại"""
    theme = st.session_state.get('current_theme', 'dark')
    if theme == 'light':
        return {
            'text': '#1e293b',
            'title': '#0f172a',
            'grid': 'rgba(51, 65, 85, 0.12)',
            'line': 'rgba(51, 65, 85, 0.3)',
            'bg': 'rgba(255,255,255,0.5)'
        }
    else:
        return {
            'text': '#cbd5e1',
            'title': '#f1f5f9',
            'grid': 'rgba(148, 163, 184, 0.12)',
            'line': 'rgba(148, 163, 184, 0.2)',
            'bg': 'rgba(0,0,0,0)'
        }


def create_time_series_chart(df: pd.DataFrame, columns: list, colors: list, 
                              title: str, y_label: str) -> go.Figure:
    """Tạo biểu đồ time series - Fixed size, theme-aware"""
    colors_theme = get_chart_colors()
    fig = go.Figure()
    
    # Giới hạn số điểm hiển thị để biểu đồ không quá rộng
    max_points = 200
    if len(df) > max_points:
        df_plot = df.iloc[-max_points:]  # Lấy 200 điểm mới nhất
    else:
        df_plot = df
    
    for col, color in zip(columns, colors):
        if col in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot['datetime'] if 'datetime' in df_plot.columns else df_plot['time'],
                y=df_plot[col],
                name=col,
                line=dict(color=color, width=2),
                fill='tozeroy',
                fillcolor=color.replace('rgb', 'rgba').replace(')', ', 0.15)')
            ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=colors_theme['title'])),
        paper_bgcolor=colors_theme['bg'],
        plot_bgcolor=colors_theme['bg'],
        font=dict(color=colors_theme['text'], size=11),
        xaxis=dict(
            gridcolor=colors_theme['grid'],
            showline=True,
            linecolor=colors_theme['line'],
            tickfont=dict(size=10),
            nticks=8  # Giới hạn số tick trên trục X
        ),
        yaxis=dict(
            title=dict(text=y_label, font=dict(size=11)),
            gridcolor=colors_theme['grid'],
            showline=True,
            linecolor=colors_theme['line'],
            tickfont=dict(size=10)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10)
        ),
        height=280,  # Fixed height
        margin=dict(l=50, r=20, t=50, b=40),
        autosize=True
    )
    return fig


def create_performance_chart(df: pd.DataFrame, analyzer: SolarPanelAnalyzer) -> go.Figure:
    """Tạo biểu đồ hiệu suất - Fixed size, theme-aware"""
    colors_theme = get_chart_colors()
    
    # Giới hạn số điểm
    max_points = 200
    if len(df) > max_points:
        df = df.iloc[-max_points:]
    
    # Tính PR cho mỗi điểm
    prs = []
    efficiencies = []
    
    for _, row in df.iterrows():
        irradiance = analyzer.lux_to_irradiance(row.get('Lux', 0))
        if irradiance > 50:
            pr = analyzer.calculate_performance_ratio(
                row.get('milliWatt', 0),
                irradiance,
                row.get('Temp', 25)
            )
            eff = analyzer.calculate_efficiency(row.get('milliWatt', 0), irradiance)
        else:
            pr = None
            eff = None
        prs.append(pr)
        efficiencies.append(eff)
    
    df_plot = df.copy()
    df_plot['Performance Ratio'] = prs
    df_plot['Efficiency'] = efficiencies
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Performance Ratio (%)', 'Hiệu suất chuyển đổi (%)'),
        vertical_spacing=0.18
    )
    
    # Performance Ratio
    fig.add_trace(
        go.Scatter(
            x=df_plot['datetime'] if 'datetime' in df_plot.columns else df_plot['time'],
            y=df_plot['Performance Ratio'],
            name='PR',
            line=dict(color='#22c55e', width=2),
            fill='tozeroy',
            fillcolor='rgba(34, 197, 94, 0.1)'
        ),
        row=1, col=1
    )
    
    # Thêm ngưỡng cảnh báo
    x_range = df_plot['datetime'] if 'datetime' in df_plot.columns else df_plot['time']
    fig.add_hline(y=70, line_dash="dash", line_color="#facc15", 
                  annotation_text="Cảnh báo (70%)", row=1, col=1)
    fig.add_hline(y=50, line_dash="dash", line_color="#ef4444", 
                  annotation_text="Nghiêm trọng (50%)", row=1, col=1)
    
    # Efficiency
    fig.add_trace(
        go.Scatter(
            x=df_plot['datetime'] if 'datetime' in df_plot.columns else df_plot['time'],
            y=df_plot['Efficiency'],
            name='η',
            line=dict(color='#3b82f6', width=2),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ),
        row=2, col=1
    )
    
    colors_theme = get_chart_colors()
    fig.update_layout(
        paper_bgcolor=colors_theme['bg'],
        plot_bgcolor=colors_theme['bg'],
        font=dict(color=colors_theme['text']),
        height=380,  # Fixed height
        showlegend=False,
        margin=dict(l=50, r=20, t=40, b=40)
    )
    
    fig.update_xaxes(gridcolor=colors_theme['grid'], tickfont=dict(size=10), nticks=8)
    fig.update_yaxes(gridcolor=colors_theme['grid'], tickfont=dict(size=10))
    
    return fig


def create_health_score_display(health: dict) -> None:
    """Hiển thị điểm sức khỏe tấm pin"""
    if health.get('score') is None:
        st.warning("Không đủ dữ liệu để đánh giá")
        return
    
    score = health['score']
    grade = health['grade']
    
    # Chọn màu dựa trên grade
    color_class = f"health-{grade.lower()}"
    
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="health-score {color_class}">
            {grade}
        </div>
        <div style="margin-top: 1rem;">
            <span style="font-size: 2rem; font-weight: bold; color: #f1f5f9;">{score}</span>
            <span style="color: #94a3b8;">/100</span>
        </div>
        <p style="color: #94a3b8; margin-top: 0.5rem;">{health['message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'details' in health:
        details = health['details']
        cols = st.columns(3)
        with cols[0]:
            st.metric("PR Trung bình", f"{details.get('average_pr', 0):.1f}%")
        with cols[1]:
            st.metric("Số cảnh báo", details.get('anomaly_count', 0))
        with cols[2]:
            st.metric("Điểm xu hướng", f"{details.get('trend_contribution', 0):.1f}/30")


# ================== TRANG CHÍNH ==================
def main():
    # Khởi tạo theme (mặc định dark)
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Áp dụng CSS theo theme
    apply_custom_css(st.session_state.theme)
    
    # # Header
    # st.markdown('<h1 class="main-header">☀️ Solar Panel Monitoring System</h1>', unsafe_allow_html=True)
    # st.markdown('<p class="sub-header">Hệ thống giám sát và phân tích hiệu suất pin mặt trời thời gian thực</p>', unsafe_allow_html=True)
    
    # Khởi tạo Firebase
    if not init_firebase():
        st.stop()
    
    # Khởi tạo analyzer
    analyzer = SolarPanelAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/solar-panel.png", width=80)
        st.title("Điều khiển")
        
        # Theme toggle - Nổi bật hơn
        st.markdown("---")
        st.markdown("### 🎨 Chuyển đổi giao diện")
        st.markdown("Chọn giao diện bạn muốn:")
        
        # Hiển thị trạng thái hiện tại
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
                        key="dashboard_theme_dark"):
                st.session_state.theme = 'dark'
                st.rerun()
        with col2:
            if st.button("☀️ Sáng", 
                        use_container_width=True,
                        disabled=current_theme == 'light',
                        type="primary",
                        key="dashboard_theme_light"):
                st.session_state.theme = 'light'
                st.rerun()
        
        st.markdown("---")
        
        # Chọn chế độ xem
        view_mode = st.radio(
            "📊 Chế độ xem",
            ["Real-time", "Phân tích theo giờ", "Phân tích theo ngày", "So sánh lịch sử"],
            index=0
        )
        
        st.divider()
        
        # Cấu hình thời gian
        st.subheader("⏰ Thời gian")
        
        if view_mode == "Real-time":
            # Real-time: Tự động dùng thời gian hiện tại
            selected_date = datetime.now().date()
            selected_hour = datetime.now().hour
            st.success(f"🔴 **LIVE** - {selected_date.strftime('%d/%m/%Y')} lúc {selected_hour}:00")
            st.caption("Dữ liệu tự động cập nhật theo thời gian thực")
        
        elif view_mode == "Phân tích theo giờ":
            # Phân tích theo giờ: Cho phép chọn thủ công
            selected_date = st.date_input(
                "Chọn ngày",
                value=datetime.now().date(),
                max_value=datetime.now().date()
            )
            selected_hour = st.slider("Chọn giờ", 0, 23, datetime.now().hour)
        
        elif view_mode == "Phân tích theo ngày":
            selected_date = st.date_input(
                "Chọn ngày phân tích",
                value=datetime.now().date(),
                max_value=datetime.now().date()
            )
        
        else:  # So sánh lịch sử
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Từ ngày",
                    value=datetime.now().date() - timedelta(days=7)
                )
            with col2:
                end_date = st.date_input(
                    "Đến ngày",
                    value=datetime.now().date()
                )
        
        st.divider()
        
        # Cấu hình xử lý dữ liệu
        st.subheader("🔧 Xử lý dữ liệu")
        clean_method = st.selectbox(
            "Phương pháp xử lý giá trị 0",
            ["auto_fill", "smart", "none"],
            index=0,  # Mặc định là 'auto_fill'
            help="'auto_fill' = Tự động forward fill tất cả giá trị 0 (khuyến nghị). 'smart' = Chỉ xử lý khi không hợp lý. 'none' = Giữ nguyên"
        )
        
        # Auto refresh cho real-time
        if view_mode == "Real-time":
            st.divider()
            st.subheader("🔄 Auto Refresh")
            auto_refresh = st.checkbox("Tự động cập nhật", value=True)
            if auto_refresh:
                refresh_rate = st.select_slider(
                    "Tần suất (giây)",
                    options=[2, 3, 5, 10, 15, 30],
                    value=3,
                    help="Dữ liệu Firebase cập nhật 1s/lần, chọn tần suất phù hợp"
                )
        else:
            auto_refresh = False
            refresh_rate = 10
        
        st.divider()
        
        # Hiển thị thông số tấm pin (chỉ xem, không edit)
        st.subheader("☀️ Thông số tấm pin")
        with st.expander("📋 Xem thông số", expanded=False):
            st.markdown(f"""
            **📊 Thông số công suất:**
            - **Pmax:** {analyzer.specs.rated_power}W
            - **Vmp:** {analyzer.specs.rated_voltage}V
            - **Imp:** {analyzer.specs.rated_current}A
            
            **📐 Kích thước:** 400×350×17mm ({analyzer.specs.panel_area:.3f} m²)
            
            **🌡️ STC:** 1000 W/m², 25°C
            """)
        
        # Nút refresh thủ công và clear cache
        col_refresh1, col_refresh2 = st.columns(2)
        with col_refresh1:
            if st.button("🔄 Làm mới ngay", use_container_width=True, key="dashboard_refresh"):
                st.cache_data.clear()
                st.rerun()
        with col_refresh2:
            if st.button("🗑️ Clear Cache", use_container_width=True, key="dashboard_clear_cache"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("✅ Đã clear cache!")
                st.rerun()
    
    # Main content
    if view_mode == "Real-time":
        # Auto refresh nếu bật
        if auto_refresh:
            try:
                from streamlit_autorefresh import st_autorefresh
                # Tự động refresh theo tần suất đã chọn
                st_autorefresh(interval=refresh_rate * 1000, limit=None, key="realtime_refresh")
            except ImportError:
                # Fallback nếu không có streamlit_autorefresh
                st.info(f"💡 Trang sẽ tự động cập nhật. Bấm 'Làm mới ngay' nếu cần.")
        
        # Đảm bảo format date giống hệt index.html (YYYY-MM-DD)
        date_str = selected_date.strftime("%Y-%m-%d") if hasattr(selected_date, 'strftime') else str(selected_date)
        show_realtime_view(analyzer, date_str, selected_hour, clean_method)
    
    elif view_mode == "Phân tích theo giờ":
        date_str = selected_date.strftime("%Y-%m-%d") if hasattr(selected_date, 'strftime') else str(selected_date)
        show_hourly_analysis(analyzer, date_str, selected_hour, clean_method)
    
    elif view_mode == "Phân tích theo ngày":
        date_str = selected_date.strftime("%Y-%m-%d") if hasattr(selected_date, 'strftime') else str(selected_date)
        show_daily_analysis(analyzer, date_str, clean_method)
    
    else:
        start_date_str = start_date.strftime("%Y-%m-%d") if hasattr(start_date, 'strftime') else str(start_date)
        end_date_str = end_date.strftime("%Y-%m-%d") if hasattr(end_date, 'strftime') else str(end_date)
        show_historical_comparison(analyzer, start_date_str, end_date_str, clean_method)


def show_realtime_view(analyzer: SolarPanelAnalyzer, date: str, hour: int, clean_method: str = 'auto_fill', auto_fallback: bool = True):
    """Hiển thị chế độ real-time - Ổn định, không nhấp nháy
    
    Args:
        auto_fallback: Nếu True, tự động thử giờ trước nếu giờ hiện tại không có data
    """
    
    # Khởi tạo session state
    if 'last_valid_values' not in st.session_state:
        st.session_state.last_valid_values = {}
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = datetime.now()
    
    # Đảm bảo format date đúng (YYYY-MM-DD)
    if hasattr(date, 'strftime'):
        date_str = date.strftime("%Y-%m-%d")
    elif isinstance(date, datetime):
        date_str = date.strftime("%Y-%m-%d")
    else:
        date_str = str(date)
    
    # Đảm bảo hour là số nguyên
    hour_int = int(hour) if hour is not None else datetime.now().hour
    
    # Lấy dữ liệu từ Firebase - thử giờ hiện tại trước
    df = fetch_data_for_hour(date_str, hour_int, clean_method)
    actual_hour = hour_int
    
    # Nếu không có data và auto_fallback=True, thử các giờ trước
    if df.empty and auto_fallback:
        for prev_hour in range(hour_int - 1, -1, -1):
            df = fetch_data_for_hour(date_str, prev_hour, clean_method)
            if not df.empty:
                actual_hour = prev_hour
                st.info(f"📡 Hiển thị dữ liệu mới nhất từ giờ {prev_hour}:00 (giờ {hour_int}:00 chưa có data)")
                break
    
    if df.empty:
        # Thử kiểm tra Firebase để xác định nguyên nhân
        error_msg = None
        try:
            if not firebase_admin._apps:
                error_msg = "Firebase chưa được khởi tạo"
            else:
                # Kiểm tra xem có data ở bất kỳ giờ nào không
                test_ref = db.reference(f'/sensor_data/{date_str}')
                test_data = test_ref.get()
                if test_data:
                    available_hours = list(test_data.keys())
                    st.warning(f"📭 **Không có dữ liệu** cho giờ {hour_int}:00")
                    st.info(f"**Các giờ có dữ liệu ngày {date_str}:** {', '.join(sorted(available_hours))}")
                else:
                    st.warning(f"📭 **Không có dữ liệu** cho ngày {date_str}")
                    st.info("Sensor chưa gửi dữ liệu cho ngày này. Kiểm tra Dashboard HTML xem có hoạt động không.")
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ **Lỗi kết nối Firebase:** {error_msg}")
            st.info("Kiểm tra **Streamlit Secrets** đã cấu hình Firebase chưa")
        return
    
    # Kiểm tra trạng thái kết nối
    data_status, is_connected = get_data_status(df, connection_timeout=10.0)
    
    # Layout header với trạng thái
    col_header, col_status = st.columns([4, 1])
    with col_header:
        st.markdown("### 📊 Dashboard Real-time")
    # with col_status:
    #     status_labels = {
    #         'live': ('🟢 Live', 'data-status live'),
    #         'stale': ('🟡 Cũ', 'data-status stale'),
    #         'no_data': ('🔴 Không dữ liệu', 'data-status no-data'),
    #         'disconnected': ('🔴 Mất kết nối', 'data-status no-data')
    #     }
    #     status_text, status_class = status_labels.get(data_status, ('❓', 'data-status'))
    #     st.markdown(f'<span class="{status_class}">{status_text}</span>', unsafe_allow_html=True)
    
    # Hiển thị cảnh báo mất kết nối - NỔI BẬT
    if not is_connected:
        st.error("""
        ⚠️ **HỆ THỐNG MẤT KẾT NỐI**
        """)
    
    # Nếu mất kết nối, đặt TẤT CẢ về 0 ngay lập tức (không cần lấy dữ liệu)
    if not is_connected:
        latest = {
            'U': 0.0,
            'Current': 0.0,
            'milliWatt': 0.0,
            'energy': st.session_state.last_valid_values.get('energy', 0.0),  # Giữ energy cuối cùng
            'Lux': 0.0,
            'Temp': 0.0,
            'Humi': 0.0,
            'datetime': datetime.now(),
            'time': datetime.now().strftime("%H:%M:%S")
        }
    else:
        # Chỉ lấy dữ liệu nếu còn kết nối
        latest = get_stable_latest_data(df, clean_method)
        
        if latest is None:
            st.warning("Không thể lấy dữ liệu")
            return
    
    # Tính hiệu suất
    irradiance = analyzer.lux_to_irradiance(latest['Lux'])
    efficiency = analyzer.calculate_efficiency(latest['milliWatt'], irradiance)
    pr = analyzer.calculate_performance_ratio(latest['milliWatt'], irradiance, latest['Temp'])
    
    # Tab views
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Biểu đồ", "🔔 Cảnh báo"])
    
    with tab1:
        # Metric cards - hàng 1
        st.subheader("⚡ Thông số hiện tại")
        cols = st.columns(7)
        
        metrics = [
            ("Điện áp", f"{latest['U']:.2f}", "V", "green"),
            ("Dòng điện", f"{latest['Current']:.3f}", "A", "blue"),
            ("Công suất", f"{latest['milliWatt']:.1f}", "mW", "orange"),
            ("Năng lượng", f"{latest['energy']:.2f}", "Wh", "purple"),
            ("Ánh sáng", f"{latest['Lux']:.0f}", "Lux", "yellow"),
            ("Nhiệt độ", f"{latest['Temp']:.1f}", "°C", "red"),
            ("Độ ẩm", f"{latest['Humi']:.1f}", "%", "cyan"),
        ]
        
        for col, (label, value, unit, color) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value {color}">{value}<span style="font-size: 0.8rem; color: #94a3b8;"> {unit}</span></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Metric cards - hàng 2 (Hiệu suất)
        st.subheader("📊 Chỉ số hiệu suất")
        cols = st.columns(4)
        
        with cols[0]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Bức xạ (ước tính)</div>
                <div class="metric-value yellow">{irradiance:.1f}<span style="font-size: 0.8rem; color: #94a3b8;"> W/m²</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Hiệu suất</div>
                <div class="metric-value blue">{efficiency:.2f}<span style="font-size: 0.8rem; color: #94a3b8;"> %</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            pr_color = "green" if pr >= 70 else ("orange" if pr >= 50 else "red")
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Performance Ratio</div>
                <div class="metric-value {pr_color}">{pr:.1f}<span style="font-size: 0.8rem; color: #94a3b8;"> %</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[3]:
            expected = analyzer.calculate_expected_power(irradiance, latest['Temp'])
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Công suất kỳ vọng</div>
                <div class="metric-value purple">{expected*1000:.1f}<span style="font-size: 0.8rem; color: #94a3b8;"> mW</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        # Thống kê
        st.divider()
        st.subheader("📈 Thống kê")
        
        col1, col2 = st.columns(2)
        with col1:
            stats_df = pd.DataFrame({
                'Thông số': ['Điện áp (V)', 'Dòng điện (A)', 'Công suất (mW)', 'Nhiệt độ (°C)', 'Ánh sáng (Lux)'],
                'Min': [df['U'].min(), df['Current'].min(), df['milliWatt'].min(), df['Temp'].min(), df['Lux'].min()],
                'Trung bình': [df['U'].mean(), df['Current'].mean(), df['milliWatt'].mean(), df['Temp'].mean(), df['Lux'].mean()],
                'Max': [df['U'].max(), df['Current'].max(), df['milliWatt'].max(), df['Temp'].max(), df['Lux'].max()]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.metric("Tổng số bản ghi", len(df))
            # Hiển thị thời gian cập nhật an toàn
            update_time = latest.get('time', latest.get('datetime', 'N/A'))
            if isinstance(update_time, datetime):
                update_time = update_time.strftime("%H:%M:%S")
            st.metric("Thời gian cập nhật", update_time)
            total_energy = df['milliWatt'].sum() / 1000 / 3600  # Wh
            st.metric("Tổng năng lượng (ước tính)", f"{total_energy:.4f} Wh")
    
    with tab2:
        # Biểu đồ
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_time_series_chart(
                df, ['U'], ['rgb(34, 197, 94)'],
                '⚡ Điện áp theo thời gian', 'V'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_time_series_chart(
                df, ['Current'], ['rgb(59, 130, 246)'],
                '🔌 Dòng điện theo thời gian', 'A'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_time_series_chart(
                df, ['milliWatt'], ['rgb(249, 115, 22)'],
                '💡 Công suất theo thời gian', 'mW'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            fig = create_time_series_chart(
                df, ['Lux'], ['rgb(250, 204, 21)'],
                '🌞 Ánh sáng theo thời gian', 'Lux'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Biểu đồ hiệu suất
        st.subheader("📊 Phân tích hiệu suất")
        fig = create_performance_chart(df, analyzer)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Phát hiện bất thường
        st.subheader("🔔 Phát hiện bất thường")
        
        anomalies = analyzer.detect_anomalies(
            latest['U'], latest['Current'], latest['milliWatt'],
            latest['Lux'], latest['Temp'], latest['Humi']
        )
        
        if not anomalies:
            st.markdown("""
            <div class="alert-card alert-normal">
                <strong>✅ Hệ thống hoạt động bình thường</strong>
                <p style="margin: 0; color: #94a3b8;">Không phát hiện bất thường nào trong bản ghi mới nhất.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for anomaly in anomalies:
                alert_class = "alert-critical" if anomaly.severity == AlertLevel.CRITICAL else "alert-warning"
                icon = "🔴" if anomaly.severity == AlertLevel.CRITICAL else "⚠️"
                st.markdown(f"""
                <div class="alert-card {alert_class}">
                    <strong>{icon} {anomaly.anomaly_type}</strong>
                    <p style="margin: 0.5rem 0 0 0; color: #f1f5f9;">{anomaly.message}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Kiểm tra toàn bộ dữ liệu trong giờ
        st.divider()
        st.subheader("📋 Tổng hợp cảnh báo trong giờ")
        
        all_anomalies = []
        for _, row in df.iterrows():
            row_anomalies = analyzer.detect_anomalies(
                row['U'], row['Current'], row['milliWatt'],
                row['Lux'], row['Temp'], row['Humi']
            )
            all_anomalies.extend(row_anomalies)
        
        if all_anomalies:
            # Nhóm theo loại
            anomaly_counts = {}
            for a in all_anomalies:
                key = a.anomaly_type
                if key not in anomaly_counts:
                    anomaly_counts[key] = {'count': 0, 'severity': a.severity.value}
                anomaly_counts[key]['count'] += 1
            
            anomaly_df = pd.DataFrame([
                {'Loại': k, 'Số lần': v['count'], 'Mức độ': v['severity']}
                for k, v in anomaly_counts.items()
            ])
            st.dataframe(anomaly_df, use_container_width=True, hide_index=True)
        else:
            st.success("Không có cảnh báo nào trong giờ này!")


def show_hourly_analysis(analyzer: SolarPanelAnalyzer, date: str, hour: int, clean_method: str = 'auto_fill'):
    """Hiển thị phân tích theo giờ"""
    df = fetch_data_for_hour(date, hour, clean_method)
    
    if df.empty:
        st.warning(f"Không có dữ liệu cho {date} lúc {hour}:00")
        return
    
    st.subheader(f"📊 Phân tích chi tiết - {date} lúc {hour}:00")
    
    # Health score
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🏥 Điểm sức khỏe")
        health = analyzer.get_health_score(df)
        create_health_score_display(health)
    
    with col2:
        st.markdown("### 📈 Xu hướng hiệu suất")
        trend = analyzer.analyze_degradation_trend(df)
        
        trend_icon = "📈" if trend['trend'] == 'improving' else ("📉" if trend['trend'] == 'degrading' else "➡️")
        st.info(f"{trend_icon} {trend['message']}")
        
        if trend.get('average_pr'):
            cols = st.columns(3)
            cols[0].metric("PR Min", f"{trend['min_pr']:.1f}%")
            cols[1].metric("PR Trung bình", f"{trend['average_pr']:.1f}%")
            cols[2].metric("PR Max", f"{trend['max_pr']:.1f}%")
    
    st.divider()
    
    # Biểu đồ hiệu suất
    fig = create_performance_chart(df, analyzer)
    st.plotly_chart(fig, use_container_width=True)
    
    # Báo cáo chi tiết
    st.divider()
    st.subheader("📋 Báo cáo chi tiết")
    
    report = analyzer.generate_daily_report(df, date)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Thống kê công suất:**")
        power_stats = report['statistics']['power']
        st.write(f"- Min: {power_stats['min']:.2f} mW")
        st.write(f"- Max: {power_stats['max']:.2f} mW")
        st.write(f"- Trung bình: {power_stats['avg']:.2f} mW")
    
    with col2:
        st.markdown("**Khuyến nghị:**")
        for rec in report['recommendations']:
            st.write(f"- {rec}")
    
    # Bảng dữ liệu
    st.divider()
    st.subheader("📊 Dữ liệu chi tiết")
    st.dataframe(df, use_container_width=True, hide_index=True)


def show_daily_analysis(analyzer: SolarPanelAnalyzer, date: str, clean_method: str = 'auto_fill'):
    """Hiển thị phân tích theo ngày"""
    with st.spinner(f"Đang tải dữ liệu ngày {date}..."):
        # Lấy dữ liệu và xử lý
        all_data = []
        for hour in range(24):
            df_hour = fetch_data_for_hour(date, hour, clean_method)
            if not df_hour.empty:
                all_data.append(df_hour)
        
        if all_data:
            df = pd.concat(all_data, ignore_index=True)
        else:
            df = pd.DataFrame()
    
    if df.empty:
        st.warning(f"Không có dữ liệu cho ngày {date}")
        return
    
    st.subheader(f"📊 Báo cáo ngày {date}")
    
    # Tổng quan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng số bản ghi", len(df))
    
    with col2:
        total_energy = df['energy'].max() - df['energy'].min() if 'energy' in df.columns else 0
        st.metric("Năng lượng tích lũy", f"{total_energy:.2f} Wh")
    
    with col3:
        st.metric("Công suất max", f"{df['milliWatt'].max():.1f} mW")
    
    with col4:
        st.metric("Nhiệt độ max", f"{df['Temp'].max():.1f} °C")
    
    st.divider()
    
    # Health score và xu hướng
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🏥 Điểm sức khỏe")
        health = analyzer.get_health_score(df)
        create_health_score_display(health)
    
    with col2:
        # Biểu đồ công suất theo giờ
        hourly_power = df.groupby(df['datetime'].dt.hour)['milliWatt'].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hourly_power.index,
            y=hourly_power.values,
            marker_color='rgb(249, 115, 22)',
            name='Công suất TB'
        ))
        
        colors_theme = get_chart_colors()
        fig.update_layout(
            title='Công suất trung bình theo giờ',
            xaxis_title='Giờ',
            yaxis_title='mW',
            paper_bgcolor=colors_theme['bg'],
            plot_bgcolor=colors_theme['bg'],
            font=dict(color=colors_theme['text']),
            height=280
        )
        fig.update_xaxes(gridcolor=colors_theme['grid'], nticks=12)
        fig.update_yaxes(gridcolor=colors_theme['grid'])
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Biểu đồ tổng hợp
    st.subheader("📈 Biểu đồ theo thời gian")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Điện áp & Dòng điện', 'Công suất', 'Ánh sáng & Nhiệt độ', 'Hiệu suất'),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # Điện áp & Dòng điện
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['U'], name='Voltage', 
                             line=dict(color='#22c55e')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['Current']*10, name='Current (x10)', 
                             line=dict(color='#3b82f6')), row=1, col=1)
    
    # Công suất
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['milliWatt'], name='Power',
                             fill='tozeroy', line=dict(color='#f97316')), row=1, col=2)
    
    # Ánh sáng & Nhiệt độ
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['Lux']/1000, name='Lux (k)',
                             line=dict(color='#facc15')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['Temp'], name='Temp',
                             line=dict(color='#ef4444')), row=2, col=1)
    
    # Tính hiệu suất
    prs = []
    for _, row in df.iterrows():
        irr = analyzer.lux_to_irradiance(row['Lux'])
        if irr > 50:
            pr = analyzer.calculate_performance_ratio(row['milliWatt'], irr, row['Temp'])
        else:
            pr = None
        prs.append(pr)
    
    fig.add_trace(go.Scatter(x=df['datetime'], y=prs, name='PR',
                             fill='tozeroy', line=dict(color='#a855f7')), row=2, col=2)
    
    colors_theme = get_chart_colors()
    fig.update_layout(
        height=450,  # Fixed height
        paper_bgcolor=colors_theme['bg'],
        plot_bgcolor=colors_theme['bg'],
        font=dict(color=colors_theme['text'], size=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5, font=dict(size=9))
    )
    
    fig.update_xaxes(gridcolor=colors_theme['grid'], tickfont=dict(size=9), nticks=8)
    fig.update_yaxes(gridcolor=colors_theme['grid'], tickfont=dict(size=9))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Báo cáo và khuyến nghị
    st.divider()
    report = analyzer.generate_daily_report(df, date)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Thống kê chi tiết")
        for param, stats in report['statistics'].items():
            if isinstance(stats, dict):
                st.write(f"**{param.title()}:** Min={stats.get('min', 0):.2f}, "
                        f"Avg={stats.get('avg', 0):.2f}, Max={stats.get('max', 0):.2f}")
    
    with col2:
        st.subheader("💡 Khuyến nghị")
        for rec in report['recommendations']:
            st.write(rec)


def show_historical_comparison(analyzer: SolarPanelAnalyzer, start_date: str, end_date: str, clean_method: str = 'auto_fill'):
    """Hiển thị so sánh lịch sử"""
    with st.spinner(f"Đang tải dữ liệu từ {start_date} đến {end_date}..."):
        # Lấy dữ liệu và xử lý
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        all_data = []
        current = start
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            for hour in range(24):
                df_hour = fetch_data_for_hour(date_str, hour, clean_method)
                if not df_hour.empty:
                    df_hour['date'] = date_str
                    all_data.append(df_hour)
            current += timedelta(days=1)
        
        if all_data:
            df = pd.concat(all_data, ignore_index=True)
        else:
            df = pd.DataFrame()
    
    if df.empty:
        st.warning(f"Không có dữ liệu trong khoảng thời gian này")
        return
    
    st.subheader(f"📊 So sánh lịch sử: {start_date} - {end_date}")
    
    # Tổng quan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Số ngày có dữ liệu", df['date'].nunique())
    
    with col2:
        st.metric("Tổng số bản ghi", len(df))
    
    with col3:
        st.metric("Công suất max", f"{df['milliWatt'].max():.1f} mW")
    
    with col4:
        avg_power = df['milliWatt'].mean()
        st.metric("Công suất TB", f"{avg_power:.1f} mW")
    
    st.divider()
    
    # Biểu đồ so sánh theo ngày
    daily_stats = df.groupby('date').agg({
        'milliWatt': ['mean', 'max'],
        'U': 'mean',
        'Lux': 'mean',
        'Temp': 'mean'
    }).reset_index()
    daily_stats.columns = ['date', 'power_avg', 'power_max', 'voltage_avg', 'lux_avg', 'temp_avg']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Công suất theo ngày', 'Điện áp theo ngày', 
                       'Ánh sáng theo ngày', 'Nhiệt độ theo ngày'),
        vertical_spacing=0.15
    )
    
    fig.add_trace(go.Bar(x=daily_stats['date'], y=daily_stats['power_avg'], 
                        name='Power Avg', marker_color='#f97316'), row=1, col=1)
    fig.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['power_max'],
                            name='Power Max', line=dict(color='#ef4444', width=2)), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['voltage_avg'],
                            name='Voltage', line=dict(color='#22c55e'), fill='tozeroy'), row=1, col=2)
    
    fig.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['lux_avg'],
                            name='Lux', line=dict(color='#facc15'), fill='tozeroy'), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=daily_stats['date'], y=daily_stats['temp_avg'],
                            name='Temp', line=dict(color='#ef4444'), fill='tozeroy'), row=2, col=2)
    
    colors_theme = get_chart_colors()
    fig.update_layout(
        height=380,  # Fixed height
        paper_bgcolor=colors_theme['bg'],
        plot_bgcolor=colors_theme['bg'],
        font=dict(color=colors_theme['text'], size=10),
        showlegend=False
    )
    
    fig.update_xaxes(gridcolor=colors_theme['grid'], tickfont=dict(size=9), nticks=8)
    fig.update_yaxes(gridcolor=colors_theme['grid'], tickfont=dict(size=9))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Xu hướng hiệu suất
    st.divider()
    st.subheader("📈 Phân tích xu hướng")
    
    trend = analyzer.analyze_degradation_trend(df)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        trend_icon = "📈" if trend['trend'] == 'improving' else ("📉" if trend['trend'] == 'degrading' else "➡️")
        
        if trend['trend'] == 'degrading':
            st.error(f"{trend_icon} **Hiệu suất đang giảm**")
        elif trend['trend'] == 'improving':
            st.success(f"{trend_icon} **Hiệu suất đang cải thiện**")
        else:
            st.info(f"{trend_icon} **Hiệu suất ổn định**")
        
        st.write(trend['message'])
        
        if trend.get('average_pr'):
            st.metric("PR Trung bình", f"{trend['average_pr']:.1f}%")
    
    with col2:
        # Tính PR theo ngày
        daily_pr = []
        for date in df['date'].unique():
            day_df = df[df['date'] == date]
            prs = []
            for _, row in day_df.iterrows():
                irr = analyzer.lux_to_irradiance(row['Lux'])
                if irr > 100:
                    pr = analyzer.calculate_performance_ratio(row['milliWatt'], irr, row['Temp'])
                    prs.append(pr)
            if prs:
                daily_pr.append({'date': date, 'pr': np.mean(prs)})
        
        if daily_pr:
            pr_df = pd.DataFrame(daily_pr)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pr_df['date'], y=pr_df['pr'],
                mode='lines+markers',
                name='PR',
                line=dict(color='#22c55e', width=3),
                marker=dict(size=10)
            ))
            
            # Thêm trendline
            if len(pr_df) > 1:
                z = np.polyfit(range(len(pr_df)), pr_df['pr'], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=pr_df['date'], y=p(range(len(pr_df))),
                    mode='lines',
                    name='Xu hướng',
                    line=dict(color='#f97316', width=2, dash='dash')
                ))
            
            fig.add_hline(y=70, line_dash="dash", line_color="#facc15", 
                         annotation_text="Ngưỡng cảnh báo")
            
            colors_theme = get_chart_colors()
            fig.update_layout(
                title='Performance Ratio theo ngày',
                paper_bgcolor=colors_theme['bg'],
                plot_bgcolor=colors_theme['bg'],
                font=dict(color=colors_theme['text']),
                height=280,
                yaxis_title='PR (%)'
            )
            fig.update_xaxes(gridcolor=colors_theme['grid'], nticks=10)
            fig.update_yaxes(gridcolor=colors_theme['grid'])
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Bảng dữ liệu tổng hợp
    st.divider()
    st.subheader("📋 Dữ liệu tổng hợp theo ngày")
    st.dataframe(daily_stats, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    # Chỉ set_page_config khi chạy trực tiếp file này
    # st.set_page_config(
    #     page_title="Solar Panel Monitoring System",
    #     page_icon="☀️",
    #     layout="wide",
    #     initial_sidebar_state="expanded"
    # )
    main()

