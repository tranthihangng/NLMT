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
from analysis import SolarPanelAnalyzer, PanelSpecs, AlertLevel


def apply_custom_css(theme='dark'):
    """Áp dụng CSS tùy chỉnh với hỗ trợ dark/light mode - Phiên bản chuyên nghiệp"""
    
    # Định nghĩa màu sắc theo theme
    if theme == 'light':
        # Theme sáng - Phong cách Clean & Modern
        bg_gradient = "linear-gradient(135deg, #f0f4f8 0%, #ffffff 50%, #f0f4f8 100%)"
        sidebar_bg = "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"
        card_bg = "linear-gradient(145deg, #ffffff 0%, #f8fafc 100%)"
        card_shadow = "0 4px 15px -3px rgba(0, 0, 0, 0.08)"
        card_hover_shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.12)"
        text_primary = "#1a202c"
        text_secondary = "#4a5568"
        text_muted = "#718096"
        border_color = "rgba(0, 0, 0, 0.08)"
        accent_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    else:
        # Theme tối - Phong cách Premium Dark
        bg_gradient = "linear-gradient(135deg, #0a0f1a 0%, #1a1f2e 50%, #0a0f1a 100%)"
        sidebar_bg = "linear-gradient(180deg, #1a1f2e 0%, #0a0f1a 100%)"
        card_bg = "linear-gradient(145deg, #1e2538 0%, #2d3548 100%)"
        card_shadow = "0 4px 15px -3px rgba(0, 0, 0, 0.4)"
        card_hover_shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.5)"
        text_primary = "#f7fafc"
        text_secondary = "#a0aec0"
        text_muted = "#718096"
        border_color = "rgba(255, 255, 255, 0.06)"
        accent_gradient = "linear-gradient(135deg, #f59e0b 0%, #f97316 100%)"
    
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
</style>
""", unsafe_allow_html=True)


# ================== KHỞI TẠO FIREBASE ==================
@st.cache_resource
def init_firebase():
    """Khởi tạo kết nối Firebase"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://nlmt-duy-default-rtdb.firebaseio.com'
            })
        return True
    except Exception as e:
        st.error(f"Lỗi kết nối Firebase: {e}")
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
        connection_timeout: Thời gian timeout (giây) để coi là mất kết nối
    
    Returns:
        (status, is_connected): 
        - status: 'live', 'stale', 'no_data', 'disconnected'
        - is_connected: True nếu còn kết nối, False nếu mất kết nối
    """
    if df.empty:
        return 'no_data', False
    
    # Kiểm tra thời gian cập nhật (nếu có datetime)
    if 'datetime' in df.columns:
        now = datetime.now()
        last_update = df['datetime'].max()
        time_diff = (now - last_update).total_seconds()
        
        # Mất kết nối nếu không có dữ liệu mới trong connection_timeout giây
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
@st.cache_data(ttl=1)  # Cache 1 giây - phù hợp với tần suất cập nhật 1s/lần
def fetch_data_for_hour(date: str, hour: int, clean_method: str = 'auto_fill') -> pd.DataFrame:
    """
    Lấy dữ liệu từ Firebase cho một giờ cụ thể
    Cache 1s để tránh gọi Firebase liên tục nhưng vẫn cập nhật real-time
    """
    try:
        hour_str = str(hour).zfill(2)
        ref = db.reference(f'/sensor_data/{date}/{hour_str}')
        data = ref.get()
        
        if not data:
            return pd.DataFrame()
        
        records = []
        for time_key, values in data.items():
            try:
                # Xử lý timestamp - có thể có format khác nhau (H:M:S hoặc H:M:S.microseconds)
                try:
                    # Thử parse với format có milliseconds
                    if '.' in time_key:
                        dt = datetime.strptime(f"{date} {time_key}", "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        dt = datetime.strptime(f"{date} {time_key}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # Fallback: parse format cơ bản
                    dt = datetime.strptime(f"{date} {time_key}", "%Y-%m-%d %H:%M:%S")
                
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
            except (ValueError, TypeError) as e:
                continue  # Bỏ qua record lỗi
        
        if not records:
            return pd.DataFrame()
            
        df = pd.DataFrame(records)
        # Sắp xếp theo datetime để đảm bảo thứ tự đúng
        df = df.sort_values('datetime').reset_index(drop=True)
        
        return df
    except Exception as e:
        # Không hiển thị lỗi để tránh spam - sẽ xử lý ở tầng view
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
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f1f5f9'},
        height=200,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def create_time_series_chart(df: pd.DataFrame, columns: list, colors: list, 
                              title: str, y_label: str) -> go.Figure:
    """Tạo biểu đồ time series"""
    fig = go.Figure()
    
    for col, color in zip(columns, colors):
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df['datetime'] if 'datetime' in df.columns else df['time'],
                y=df[col],
                name=col,
                line=dict(color=color, width=2),
                fill='tozeroy',
                fillcolor=color.replace('rgb', 'rgba').replace(')', ', 0.1)')
            ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#f1f5f9')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(
            gridcolor='rgba(148, 163, 184, 0.1)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.2)'
        ),
        yaxis=dict(
            title=y_label,
            gridcolor='rgba(148, 163, 184, 0.1)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.2)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=350,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    return fig


def create_performance_chart(df: pd.DataFrame, analyzer: SolarPanelAnalyzer) -> go.Figure:
    """Tạo biểu đồ hiệu suất"""
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
        vertical_spacing=0.15
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
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    fig.update_xaxes(gridcolor='rgba(148, 163, 184, 0.1)')
    fig.update_yaxes(gridcolor='rgba(148, 163, 184, 0.1)')
    
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
        
        if view_mode in ["Real-time", "Phân tích theo giờ"]:
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
        
        # Cấu hình tấm pin
        st.subheader("⚙️ Thông số tấm pin")
        with st.expander("Cấu hình", expanded=True):
            st.markdown("**📊 Thông số công suất tối đa (MPP):**")
            col1, col2, col3 = st.columns(3)
            with col1:
                rated_power = st.number_input("Pmax (W)", value=20.0, min_value=0.1, step=0.1, help="Công suất tối đa")
            with col2:
                rated_voltage = st.number_input("Vmp (V)", value=16.0, min_value=0.1, step=0.1, help="Điện áp tại công suất tối đa")
            with col3:
                rated_current = st.number_input("Imp (A)", value=1.25, min_value=0.01, step=0.01, help="Dòng điện tại công suất tối đa")
            
            st.markdown("**🔌 Thông số mạch hở/ngắn mạch:**")
            col4, col5 = st.columns(2)
            with col4:
                voc = st.number_input("Voc - Điện áp mạch hở (V)", value=19.2, min_value=0.1, step=0.1, help="Open Circuit Voltage")
            with col5:
                isc = st.number_input("Isc - Dòng ngắn mạch (A)", value=1.5, min_value=0.01, step=0.01, help="Short Circuit Current")
            
            st.markdown("**📐 Kích thước tấm pin:**")
            col6, col7, col8 = st.columns(3)
            with col6:
                panel_length = st.number_input("Chiều dài (m)", value=0.4, min_value=0.01, step=0.01, help="400mm = 0.4m")
            with col7:
                panel_width = st.number_input("Chiều rộng (m)", value=0.35, min_value=0.01, step=0.01, help="350mm = 0.35m")
            with col8:
                panel_thickness = st.number_input("Độ dày (m)", value=0.017, min_value=0.001, step=0.001, format="%.3f", help="17mm = 0.017m")
            
            # Tính diện tích tự động
            panel_area = panel_length * panel_width
            st.info(f"📏 **Diện tích tấm pin:** {panel_area:.3f} m² (tự động tính từ {panel_length}m × {panel_width}m)")
            
            st.markdown("**🌡️ Thông số nhiệt độ:**")
            temp_coefficient = st.number_input(
                "Hệ số nhiệt độ (%/°C)", 
                value=-0.004, 
                min_value=-0.01, 
                max_value=0.0, 
                step=0.0001,
                format="%.4f",
                help="Hệ số suy giảm công suất theo nhiệt độ. Thường -0.4% đến -0.5%/°C"
            )
            
            st.markdown("**📋 Điều kiện tiêu chuẩn STC:**")
            st.caption("💡 STC: 1000 W/m², AM 1.5, 25°C (tiêu chuẩn - không đổi)")
            
            # Cập nhật tất cả thông số
            analyzer.specs.rated_power = rated_power
            analyzer.specs.rated_voltage = rated_voltage
            analyzer.specs.rated_current = rated_current
            analyzer.specs.open_circuit_voltage = voc
            analyzer.specs.short_circuit_current = isc
            analyzer.specs.panel_area = panel_area
            analyzer.specs.panel_length = panel_length
            analyzer.specs.panel_width = panel_width
            analyzer.specs.panel_thickness = panel_thickness
            analyzer.specs.temp_coefficient = temp_coefficient
            
            # Hiển thị thông tin tóm tắt
            st.markdown("---")
            st.markdown(f"""
            **📊 Tóm tắt thông số:**
            - **Công suất:** {rated_power}W @ {rated_voltage}V / {rated_current}A
            - **Mạch hở:** {voc}V | **Ngắn mạch:** {isc}A
            - **Kích thước:** {panel_length}m × {panel_width}m × {panel_thickness}m
            - **Diện tích:** {panel_area:.3f} m²
            - **Hiệu suất lý thuyết:** {(rated_power / (1000 * panel_area) * 100):.2f}% (tại STC)
            """)
        
        # Nút refresh thủ công
        if st.button("🔄 Làm mới ngay", use_container_width=True, key="dashboard_refresh"):
            st.cache_data.clear()
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
        
        show_realtime_view(analyzer, str(selected_date), selected_hour, clean_method)
    
    elif view_mode == "Phân tích theo giờ":
        show_hourly_analysis(analyzer, str(selected_date), selected_hour, clean_method)
    
    elif view_mode == "Phân tích theo ngày":
        show_daily_analysis(analyzer, str(selected_date), clean_method)
    
    else:
        show_historical_comparison(analyzer, str(start_date), str(end_date), clean_method)


def show_realtime_view(analyzer: SolarPanelAnalyzer, date: str, hour: int, clean_method: str = 'auto_fill'):
    """Hiển thị chế độ real-time - Ổn định, không nhấp nháy"""
    
    # Khởi tạo session state
    if 'last_valid_values' not in st.session_state:
        st.session_state.last_valid_values = {}
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = datetime.now()
    
    # Lấy dữ liệu từ Firebase
    df = fetch_data_for_hour(date, hour, clean_method)
    
    if df.empty:
        st.warning(f"⚠️ Không có dữ liệu cho {date} lúc {hour}:00")
        return
    
    # Kiểm tra trạng thái kết nối
    data_status, is_connected = get_data_status(df, connection_timeout=10.0)
    
    # Layout header với trạng thái
    col_header, col_status = st.columns([4, 1])
    with col_header:
        st.markdown("### 📊 Dashboard Real-time")
    with col_status:
        status_labels = {
            'live': ('🟢 Live', 'data-status live'),
            'stale': ('🟡 Cũ', 'data-status stale'),
            'no_data': ('🔴 Không dữ liệu', 'data-status no-data'),
            'disconnected': ('🔴 Mất kết nối', 'data-status no-data')
        }
        status_text, status_class = status_labels.get(data_status, ('❓', 'data-status'))
        st.markdown(f'<span class="{status_class}">{status_text}</span>', unsafe_allow_html=True)
    
    # Hiển thị cảnh báo mất kết nối
    if not is_connected:
        st.error("⚠️ **MẤT KẾT NỐI**: Không nhận được dữ liệu mới trong 10 giây.")
    
    # Lấy dữ liệu ỔN ĐỊNH (không nhấp nháy)
    latest = get_stable_latest_data(df, clean_method)
    
    if latest is None:
        st.warning("Không thể lấy dữ liệu")
        return
    
    # Nếu mất kết nối, đặt về 0
    if not is_connected:
        latest = {
            'U': 0.0,
            'Current': 0.0,
            'milliWatt': 0.0,
            'energy': latest.get('energy', 0.0),
            'Lux': 0.0,
            'Temp': 0.0,
            'Humi': 0.0
        }
    
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
        
        fig.update_layout(
            title='Công suất trung bình theo giờ',
            xaxis_title='Giờ',
            yaxis_title='mW',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            height=300
        )
        fig.update_xaxes(gridcolor='rgba(148, 163, 184, 0.1)')
        fig.update_yaxes(gridcolor='rgba(148, 163, 184, 0.1)')
        
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
    
    fig.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    
    fig.update_xaxes(gridcolor='rgba(148, 163, 184, 0.1)')
    fig.update_yaxes(gridcolor='rgba(148, 163, 184, 0.1)')
    
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
    
    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        showlegend=False
    )
    
    fig.update_xaxes(gridcolor='rgba(148, 163, 184, 0.1)')
    fig.update_yaxes(gridcolor='rgba(148, 163, 184, 0.1)')
    
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
            
            fig.update_layout(
                title='Performance Ratio theo ngày',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                height=300,
                yaxis_title='PR (%)'
            )
            fig.update_xaxes(gridcolor='rgba(148, 163, 184, 0.1)')
            fig.update_yaxes(gridcolor='rgba(148, 163, 184, 0.1)')
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Bảng dữ liệu tổng hợp
    st.divider()
    st.subheader("📋 Dữ liệu tổng hợp theo ngày")
    st.dataframe(daily_stats, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    # Chỉ set_page_config khi chạy trực tiếp file này
    st.set_page_config(
        page_title="Solar Panel Monitoring System",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()

