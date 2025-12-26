"""
Solar Monitoring Dashboard - Streamlit Version
Dashboard theo dõi dữ liệu cảm biến năng lượng mặt trời từ Firebase
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Solar Monitoring Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== CSS TÙY CHỈNH ==================
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #f1f5f9 !important;
        font-size: 1.8rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        background: #1e293b;
        border-radius: 12px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #a855f7);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Date input */
    .stDateInput > div > div {
        background: #334155;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
    }
    
    /* Number input */
    .stNumberInput > div > div > input {
        background: #334155;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
        color: #f1f5f9;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #1e293b;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #334155;
        color: #f1f5f9;
    }
    
    /* Custom metric card styling */
    .metric-card {
        background: #1e293b;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .metric-unit {
        color: #64748b;
        font-size: 1rem;
    }
    
    /* Colors for different metrics */
    .voltage { color: #22c55e; border-top: 3px solid #22c55e; }
    .current { color: #3b82f6; border-top: 3px solid #3b82f6; }
    .power { color: #f97316; border-top: 3px solid #f97316; }
    .energy { color: #a855f7; border-top: 3px solid #a855f7; }
    .lux { color: #facc15; border-top: 3px solid #facc15; }
    .temp { color: #ef4444; border-top: 3px solid #ef4444; }
    .humi { color: #06b6d4; border-top: 3px solid #06b6d4; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Stats box */
    .stats-box {
        background: #1e293b;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    
    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .stat-label { color: #94a3b8; }
    .stat-min { color: #06b6d4; }
    .stat-avg { color: #f1f5f9; font-weight: 600; }
    .stat-max { color: #f97316; }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(135deg, #facc15, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Connection status */
    .status-connected {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)


# ================== KHỞI TẠO FIREBASE ==================
@st.cache_resource
def init_firebase():
    """Khởi tạo kết nối Firebase"""
    try:
        # Kiểm tra nếu đã khởi tạo
        if not firebase_admin._apps:
            # CÁCH 1: Sử dụng file service account JSON
            # Uncomment và thay đổi đường dẫn file JSON của bạn
            # cred = credentials.Certificate("path/to/your-service-account.json")
            
            # CÁCH 2: Sử dụng dictionary trực tiếp (KHÔNG KHUYẾN NGHỊ cho production)
            # Thay thế các giá trị bên dưới bằng thông tin của bạn
            service_account_info = {
                "type": "service_account",
                "project_id": "nlmt-duy",
                "private_key_id": "YOUR_PRIVATE_KEY_ID",
                "private_key": "YOUR_PRIVATE_KEY",
                "client_email": "YOUR_CLIENT_EMAIL",
                "client_id": "YOUR_CLIENT_ID",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "YOUR_CERT_URL"
            }
            
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://nlmt-duy-default-rtdb.firebaseio.com'
            })
        
        return True
    except Exception as e:
        st.error(f"Lỗi kết nối Firebase: {e}")
        return False


def load_data_from_firebase(date_str: str, hour: int) -> pd.DataFrame:
    """Load dữ liệu từ Firebase Realtime Database"""
    try:
        hour_str = str(hour).zfill(2)
        path = f"/sensor_data/{date_str}/{hour_str}"
        
        ref = db.reference(path)
        data = ref.get()
        
        if not data:
            return pd.DataFrame()
        
        # Chuyển đổi thành DataFrame
        records = []
        for time_key, values in data.items():
            record = {
                'Time': time_key,
                'Voltage': values.get('U', 0),
                'Current': values.get('Current', 0),
                'Power': values.get('milliWatt', 0),
                'Energy': values.get('energy', 0),
                'Lux': values.get('Lux', 0),
                'Temp': values.get('Temp', 0),
                'Humidity': values.get('Humi', 0)
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        
        # Sort theo thời gian
        df['Time_sort'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
        df = df.sort_values('Time_sort').reset_index(drop=True)
        df = df.drop('Time_sort', axis=1)
        
        return df
        
    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu: {e}")
        return pd.DataFrame()


def calculate_stats(df: pd.DataFrame, column: str) -> dict:
    """Tính thống kê cho một cột"""
    if df.empty or column not in df.columns:
        return {'min': 0, 'max': 0, 'avg': 0}
    
    values = df[column].dropna()
    if values.empty:
        return {'min': 0, 'max': 0, 'avg': 0}
    
    return {
        'min': values.min(),
        'max': values.max(),
        'avg': values.mean()
    }


def create_chart(df: pd.DataFrame, y_column: str, title: str, color: str, y_label: str):
    """Tạo biểu đồ Plotly"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#64748b")
        )
    else:
        fig = px.area(
            df, x='Time', y=y_column,
            title=title,
            color_discrete_sequence=[color]
        )
        
        fig.update_traces(
            fill='tozeroy',
            fillcolor=color.replace(')', ', 0.1)').replace('rgb', 'rgba'),
            line=dict(width=2)
        )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="JetBrains Mono, monospace", color="#94a3b8"),
        title=dict(font=dict(size=14, color="#f1f5f9")),
        xaxis=dict(
            gridcolor='rgba(148, 163, 184, 0.1)',
            title="",
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            gridcolor='rgba(148, 163, 184, 0.1)',
            title=y_label,
            titlefont=dict(size=11),
            tickfont=dict(size=10)
        ),
        margin=dict(l=40, r=20, t=40, b=30),
        height=250,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig


def render_metric_card(title: str, value: float, unit: str, delta: float = None, 
                       color_class: str = "", decimals: int = 2):
    """Render một metric card HTML"""
    delta_html = ""
    if delta is not None:
        if delta > 0:
            delta_html = f'<span style="color: #22c55e; font-size: 0.8rem;">↑ +{delta:.1f}%</span>'
        elif delta < 0:
            delta_html = f'<span style="color: #ef4444; font-size: 0.8rem;">↓ {delta:.1f}%</span>'
        else:
            delta_html = f'<span style="color: #64748b; font-size: 0.8rem;">— 0%</span>'
    
    st.markdown(f"""
        <div class="metric-card {color_class}">
            <div class="metric-title">{title}</div>
            <div class="metric-value" style="color: inherit;">
                {value:.{decimals}f} <span class="metric-unit">{unit}</span>
            </div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


# ================== MAIN APP ==================
def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #facc15, #f97316); 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center; 
                            font-size: 28px;">☀️</div>
                <div>
                    <h1 class="main-title">Solar Monitoring Dashboard</h1>
                    <p class="subtitle">Real-time Sensor Data Visualization</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="text-align: right; padding-top: 10px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; color: #f1f5f9;">
                    {datetime.now().strftime('%H:%M:%S')}
                </div>
                <div style="color: #64748b; font-size: 0.8rem;">
                    {datetime.now().strftime('%A, %d %B %Y')}
                </div>
                <div class="status-connected" style="margin-top: 8px;">
                    <span class="status-dot"></span> Firebase Connected
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Sidebar - Controls
    with st.sidebar:
        st.markdown("## ⚙️ Controls")
        st.markdown("---")
        
        # Date picker
        selected_date = st.date_input(
            "📅 Select Date",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
        
        # Hour picker
        selected_hour = st.number_input(
            "🕐 Select Hour (0-23)",
            min_value=0,
            max_value=23,
            value=datetime.now().hour
        )
        
        st.markdown("---")
        
        # Load button
        load_clicked = st.button("🔄 Load Data", use_container_width=True)
        
        # Auto refresh
        auto_refresh = st.checkbox("⚡ Auto Refresh (10s)")
        
        st.markdown("---")
        
        # Export
        if st.button("📥 Export CSV", use_container_width=True):
            if 'df' in st.session_state and not st.session_state.df.empty:
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(
                    "💾 Download",
                    csv,
                    f"solar_data_{selected_date}_{selected_hour}h.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No data to export")
        
        st.markdown("---")
        st.markdown("""
            <div style="color: #64748b; font-size: 0.75rem; text-align: center;">
                <p>Solar Monitoring v1.0</p>
                <p>Powered by Streamlit + Firebase</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()
    
    # Load data
    if load_clicked or auto_refresh:
        date_str = selected_date.strftime('%Y-%m-%d')
        
        # Hiển thị trạng thái loading
        with st.spinner('Loading data from Firebase...'):
            # Kiểm tra kết nối Firebase
            # Bỏ comment dòng dưới sau khi cấu hình Firebase
            # if init_firebase():
            #     st.session_state.df = load_data_from_firebase(date_str, selected_hour)
            
            # Demo data (xóa khi sử dụng Firebase thật)
            st.session_state.df = generate_demo_data()
        
        if st.session_state.df.empty:
            st.warning("⚠️ No data found for selected date/time")
        else:
            st.success(f"✅ Loaded {len(st.session_state.df)} records successfully!")
    
    # Auto refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()
    
    df = st.session_state.df
    
    # Metric Cards
    st.markdown("### 📊 Current Readings")
    
    if not df.empty:
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # Calculate deltas
        def calc_delta(curr, prev_val):
            if prev_val == 0:
                return 0
            return ((curr - prev_val) / prev_val) * 100
        
        cols = st.columns(7)
        
        metrics = [
            ("Voltage", latest['Voltage'], "V", calc_delta(latest['Voltage'], prev['Voltage']), "voltage", 2),
            ("Current", latest['Current'], "A", calc_delta(latest['Current'], prev['Current']), "current", 3),
            ("Power", latest['Power'], "mW", calc_delta(latest['Power'], prev['Power']), "power", 2),
            ("Energy", latest['Energy'], "Wh", calc_delta(latest['Energy'], prev['Energy']), "energy", 2),
            ("Lux", latest['Lux'], "Lux", calc_delta(latest['Lux'], prev['Lux']), "lux", 0),
            ("Temp", latest['Temp'], "°C", calc_delta(latest['Temp'], prev['Temp']), "temp", 1),
            ("Humidity", latest['Humidity'], "%", calc_delta(latest['Humidity'], prev['Humidity']), "humi", 1),
        ]
        
        for i, (title, value, unit, delta, color, decimals) in enumerate(metrics):
            with cols[i]:
                render_metric_card(title, value, unit, delta, color, decimals)
    else:
        st.info("👆 Select date and hour, then click 'Load Data' to view metrics")
    
    # Charts
    st.markdown("### 📈 Time Series Charts")
    
    chart_cols = st.columns(3)
    
    charts_config = [
        ("Voltage", "⚡ Voltage", "rgb(34, 197, 94)", "V"),
        ("Current", "🔌 Current", "rgb(59, 130, 246)", "A"),
        ("Power", "💡 Power", "rgb(249, 115, 22)", "mW"),
        ("Lux", "🌞 Illuminance", "rgb(250, 204, 21)", "Lux"),
        ("Temp", "🌡️ Temperature", "rgb(239, 68, 68)", "°C"),
        ("Humidity", "💧 Humidity", "rgb(6, 182, 212)", "%"),
    ]
    
    for i, (column, title, color, y_label) in enumerate(charts_config):
        with chart_cols[i % 3]:
            fig = create_chart(df, column, title, color, y_label)
            st.plotly_chart(fig, use_container_width=True)
    
    # Bottom section - Table and Stats
    st.markdown("### 📋 Data Records & Statistics")
    
    col_table, col_stats = st.columns([2, 1])
    
    with col_table:
        if not df.empty:
            # Style DataFrame
            styled_df = df.style.format({
                'Voltage': '{:.2f}',
                'Current': '{:.3f}',
                'Power': '{:.2f}',
                'Energy': '{:.2f}',
                'Lux': '{:.0f}',
                'Temp': '{:.1f}',
                'Humidity': '{:.1f}'
            }).set_properties(**{
                'background-color': '#1e293b',
                'color': '#f1f5f9',
                'border-color': 'rgba(148, 163, 184, 0.1)'
            })
            
            st.dataframe(
                df.iloc[::-1],  # Newest first
                use_container_width=True,
                height=400
            )
        else:
            st.markdown("""
                <div style="background: #1e293b; border-radius: 12px; padding: 60px; text-align: center;">
                    <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.5;">📊</div>
                    <p style="color: #94a3b8; margin-bottom: 8px;">No data loaded</p>
                    <p style="color: #64748b; font-size: 0.85rem;">Select date and hour, then click Load Data</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col_stats:
        st.markdown("#### 📈 Statistics")
        
        if not df.empty:
            stats_data = [
                ("Voltage", "V"),
                ("Current", "A"),
                ("Power", "mW"),
                ("Temp", "°C"),
                ("Humidity", "%"),
                ("Lux", "Lux")
            ]
            
            for col_name, unit in stats_data:
                stats = calculate_stats(df, col_name)
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 8px 0; 
                                border-bottom: 1px solid rgba(148, 163, 184, 0.1);">
                        <span style="color: #94a3b8;">{col_name}</span>
                        <span>
                            <span style="color: #06b6d4;">{stats['min']:.2f}</span> / 
                            <span style="color: #f1f5f9; font-weight: 600;">{stats['avg']:.2f}</span> / 
                            <span style="color: #f97316;">{stats['max']:.2f}</span>
                            <span style="color: #64748b;"> {unit}</span>
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="margin-top: 16px; padding: 12px; background: rgba(34, 197, 94, 0.1); 
                            border-radius: 8px; text-align: center;">
                    <span style="color: #22c55e;">📊 Total: {len(df)} records</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Load data to view statistics")


def generate_demo_data():
    """Tạo dữ liệu demo để test (xóa khi dùng Firebase thật)"""
    import random
    
    records = []
    base_time = datetime.now().replace(minute=0, second=0)
    
    for i in range(60):
        time_str = (base_time + timedelta(seconds=i*30)).strftime('%H:%M:%S')
        records.append({
            'Time': time_str,
            'Voltage': 12 + random.uniform(-0.5, 0.5),
            'Current': 0.5 + random.uniform(-0.1, 0.1),
            'Power': 6000 + random.uniform(-500, 500),
            'Energy': 100 + i * 0.5,
            'Lux': 50000 + random.uniform(-5000, 5000),
            'Temp': 28 + random.uniform(-2, 2),
            'Humidity': 65 + random.uniform(-5, 5)
        })
    
    return pd.DataFrame(records)


if __name__ == "__main__":
    main()

