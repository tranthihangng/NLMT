"""
Solar Panel Performance Analysis Module
Thuật toán phân tích hiệu suất và phát hiện bất thường cho hệ thống pin mặt trời

Author: Solar Monitoring System
Date: 2024
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class AlertLevel(Enum):
    """Mức độ cảnh báo"""
    NORMAL = "normal"
    WARNING = "warning"  # Cảnh báo nhẹ
    CRITICAL = "critical"  # Cảnh báo nghiêm trọng


@dataclass
class PanelSpecs:
    """Thông số kỹ thuật của tấm pin mặt trời"""
    # Thông số công suất tối đa (MPP - Maximum Power Point)
    rated_power: float = 20.0  # Pmax: Công suất tối đa (W)
    rated_voltage: float = 16.0  # Vmp: Điện áp tại công suất tối đa (V)
    rated_current: float = 1.25  # Imp: Dòng điện tại công suất tối đa (A)
    
    # Thông số mạch hở/ngắn mạch
    open_circuit_voltage: float = 19.2  # Voc: Điện áp mạch hở (V)
    short_circuit_current: float = 1.5  # Isc: Dòng điện ngắn mạch (A)
    
    # Thông số vật lý
    panel_area: float = 0.14  # Diện tích tấm pin (m²) = 0.4m × 0.35m
    panel_length: float = 0.4  # Chiều dài (m)
    panel_width: float = 0.35  # Chiều rộng (m)
    panel_thickness: float = 0.017  # Độ dày (m) = 17mm
    
    # Thông số nhiệt độ
    temp_coefficient: float = -0.004  # Hệ số nhiệt độ (%/°C) - thường -0.4% đến -0.5%/°C
    
    # Điều kiện tiêu chuẩn STC
    stc_irradiance: float = 1000.0  # Bức xạ chuẩn STC (W/m²)
    stc_temperature: float = 25.0  # Nhiệt độ chuẩn STC (°C)
    stc_air_mass: float = 1.5  # Khối lượng không khí AM 1.5
    
    # Thông số hệ thống
    max_system_voltage: float = 1000.0  # Điện áp hệ thống tối đa (VDC)


@dataclass
class PerformanceMetrics:
    """Các chỉ số hiệu suất của tấm pin"""
    efficiency: float  # Hiệu suất thực tế (%)
    performance_ratio: float  # Tỷ lệ hiệu suất so với lý thuyết (%)
    power_output: float  # Công suất đầu ra (W)
    expected_power: float  # Công suất kỳ vọng (W)
    degradation: float  # Mức độ suy giảm (%)
    timestamp: datetime


@dataclass
class AnomalyReport:
    """Báo cáo bất thường"""
    timestamp: datetime
    anomaly_type: str
    parameter: str
    value: float
    expected_range: Tuple[float, float]
    severity: AlertLevel
    message: str


class SolarPanelAnalyzer:
    """
    Bộ phân tích hiệu suất tấm pin mặt trời
    
    Các thuật toán chính:
    1. Tính hiệu suất thực tế dựa trên điều kiện môi trường
    2. Phát hiện suy giảm hiệu suất theo thời gian
    3. Phát hiện bất thường trong các thông số
    4. Dự báo công suất dựa trên điều kiện hiện tại
    """
    
    def __init__(self, panel_specs: PanelSpecs = None):
        self.specs = panel_specs or PanelSpecs()
        self.history: List[PerformanceMetrics] = []
        self.anomalies: List[AnomalyReport] = []
        
        # Ngưỡng phát hiện bất thường
        self.thresholds = {
            'voltage_min': 0.5,  # V
            'voltage_max': 25.0,  # V
            'current_min': 0.0,  # A
            'current_max': 10.0,  # A
            'temp_min': -10.0,  # °C
            'temp_max': 85.0,  # °C - Max operating temp
            'power_efficiency_min': 5.0,  # % - Dưới ngưỡng này là bất thường
            'performance_ratio_warning': 70.0,  # % - Cảnh báo
            'performance_ratio_critical': 50.0,  # % - Nghiêm trọng
            'sudden_drop_threshold': 30.0,  # % - Sụt giảm đột ngột
        }
    
    def lux_to_irradiance(self, lux: float) -> float:
        """
        Chuyển đổi Lux sang Irradiance (W/m²)
        
        Công thức xấp xỉ: 1 W/m² ≈ 120 Lux (cho ánh sáng mặt trời)
        Tham khảo: https://www.researchgate.net/publication/283085804
        """
        # Hệ số chuyển đổi phụ thuộc vào phổ ánh sáng
        # Ánh sáng mặt trời: ~120 lux/W/m²
        conversion_factor = 120.0
        irradiance = lux / conversion_factor
        return max(0, min(irradiance, 1500))  # Giới hạn 0-1500 W/m²
    
    def calculate_expected_power(self, irradiance: float, temperature: float) -> float:
        """
        Tính công suất kỳ vọng dựa trên điều kiện môi trường
        
        Công thức:
        P_expected = P_rated × (G/G_stc) × [1 + α × (T - T_stc)]
        
        Trong đó:
        - P_rated: Công suất định mức (W)
        - G: Bức xạ thực tế (W/m²)
        - G_stc: Bức xạ tiêu chuẩn (1000 W/m²)
        - α: Hệ số nhiệt độ (%/°C)
        - T: Nhiệt độ thực tế (°C)
        - T_stc: Nhiệt độ tiêu chuẩn (25°C)
        """
        if irradiance <= 0:
            return 0.0
        
        # Tỷ lệ bức xạ
        irradiance_ratio = irradiance / self.specs.stc_irradiance
        
        # Hiệu chỉnh nhiệt độ
        temp_correction = 1 + self.specs.temp_coefficient * (temperature - self.specs.stc_temperature)
        
        # Công suất kỳ vọng
        expected_power = self.specs.rated_power * irradiance_ratio * temp_correction
        
        return max(0, expected_power)
    
    def calculate_efficiency(self, power_mw: float, irradiance: float) -> float:
        """
        Tính hiệu suất chuyển đổi thực tế
        
        η = P_output / (G × A) × 100%
        
        Trong đó:
        - P_output: Công suất đầu ra (W)
        - G: Bức xạ (W/m²)
        - A: Diện tích tấm pin (m²)
        """
        if irradiance <= 0:
            return 0.0
        
        power_w = power_mw / 1000.0  # Convert mW to W
        input_power = irradiance * self.specs.panel_area
        
        if input_power <= 0:
            return 0.0
        
        efficiency = (power_w / input_power) * 100
        return max(0, min(efficiency, 100))  # Giới hạn 0-100%
    
    def calculate_performance_ratio(self, actual_power_mw: float, 
                                     irradiance: float, 
                                     temperature: float) -> float:
        """
        Tính Performance Ratio (PR) - Tỷ lệ hiệu suất thực tế so với lý thuyết
        
        PR = P_actual / P_expected × 100%
        
        PR > 80%: Tốt
        70% < PR < 80%: Chấp nhận được
        PR < 70%: Cần kiểm tra
        """
        expected_power = self.calculate_expected_power(irradiance, temperature)
        
        if expected_power <= 0:
            return 0.0
        
        actual_power_w = actual_power_mw / 1000.0
        pr = (actual_power_w / expected_power) * 100
        
        return max(0, min(pr, 150))  # Giới hạn hợp lý
    
    def analyze_single_reading(self, voltage: float, current: float, 
                                power_mw: float, lux: float, 
                                temperature: float, humidity: float,
                                timestamp: datetime = None) -> PerformanceMetrics:
        """
        Phân tích một bản ghi đo lường
        """
        timestamp = timestamp or datetime.now()
        irradiance = self.lux_to_irradiance(lux)
        
        efficiency = self.calculate_efficiency(power_mw, irradiance)
        expected_power = self.calculate_expected_power(irradiance, temperature)
        pr = self.calculate_performance_ratio(power_mw, irradiance, temperature)
        
        # Tính mức độ suy giảm so với kỳ vọng
        if expected_power > 0:
            actual_power_w = power_mw / 1000.0
            degradation = max(0, (1 - actual_power_w / expected_power) * 100)
        else:
            degradation = 0.0
        
        metrics = PerformanceMetrics(
            efficiency=efficiency,
            performance_ratio=pr,
            power_output=power_mw / 1000.0,
            expected_power=expected_power,
            degradation=degradation,
            timestamp=timestamp
        )
        
        self.history.append(metrics)
        return metrics
    
    def detect_anomalies(self, voltage: float, current: float,
                         power_mw: float, lux: float,
                         temperature: float, humidity: float,
                         timestamp: datetime = None) -> List[AnomalyReport]:
        """
        Phát hiện các bất thường trong dữ liệu đo
        
        Các loại bất thường:
        1. Điện áp ngoài phạm vi
        2. Dòng điện bất thường
        3. Nhiệt độ quá cao/thấp
        4. Hiệu suất thấp bất thường
        5. Mất cân bằng công suất
        """
        timestamp = timestamp or datetime.now()
        anomalies = []
        
        # 1. Kiểm tra điện áp
        if voltage < self.thresholds['voltage_min'] and lux > 1000:
            anomalies.append(AnomalyReport(
                timestamp=timestamp,
                anomaly_type="LOW_VOLTAGE",
                parameter="voltage",
                value=voltage,
                expected_range=(self.thresholds['voltage_min'], self.thresholds['voltage_max']),
                severity=AlertLevel.WARNING,
                message=f"Điện áp thấp ({voltage:.2f}V) trong điều kiện có ánh sáng"
            ))
        
        if voltage > self.thresholds['voltage_max']:
            anomalies.append(AnomalyReport(
                timestamp=timestamp,
                anomaly_type="HIGH_VOLTAGE",
                parameter="voltage",
                value=voltage,
                expected_range=(self.thresholds['voltage_min'], self.thresholds['voltage_max']),
                severity=AlertLevel.CRITICAL,
                message=f"Điện áp quá cao ({voltage:.2f}V) - Có thể gây hư hỏng"
            ))
        
        # 2. Kiểm tra nhiệt độ
        if temperature > self.thresholds['temp_max']:
            anomalies.append(AnomalyReport(
                timestamp=timestamp,
                anomaly_type="HIGH_TEMPERATURE",
                parameter="temperature",
                value=temperature,
                expected_range=(self.thresholds['temp_min'], self.thresholds['temp_max']),
                severity=AlertLevel.CRITICAL,
                message=f"Nhiệt độ quá cao ({temperature:.1f}°C) - Nguy cơ hư hỏng tấm pin"
            ))
        
        # 3. Kiểm tra hiệu suất
        irradiance = self.lux_to_irradiance(lux)
        if irradiance > 100:  # Chỉ kiểm tra khi có đủ ánh sáng
            pr = self.calculate_performance_ratio(power_mw, irradiance, temperature)
            
            if pr < self.thresholds['performance_ratio_critical']:
                anomalies.append(AnomalyReport(
                    timestamp=timestamp,
                    anomaly_type="CRITICAL_LOW_PERFORMANCE",
                    parameter="performance_ratio",
                    value=pr,
                    expected_range=(self.thresholds['performance_ratio_critical'], 100),
                    severity=AlertLevel.CRITICAL,
                    message=f"Hiệu suất rất thấp ({pr:.1f}%) - Cần kiểm tra tấm pin ngay"
                ))
            elif pr < self.thresholds['performance_ratio_warning']:
                anomalies.append(AnomalyReport(
                    timestamp=timestamp,
                    anomaly_type="LOW_PERFORMANCE",
                    parameter="performance_ratio",
                    value=pr,
                    expected_range=(self.thresholds['performance_ratio_warning'], 100),
                    severity=AlertLevel.WARNING,
                    message=f"Hiệu suất thấp ({pr:.1f}%) - Nên kiểm tra tấm pin"
                ))
        
        # 4. Kiểm tra mất cân bằng V-I-P
        calculated_power = voltage * current * 1000  # mW
        power_diff = abs(calculated_power - power_mw)
        if power_mw > 100 and power_diff > power_mw * 0.2:  # Sai lệch > 20%
            anomalies.append(AnomalyReport(
                timestamp=timestamp,
                anomaly_type="POWER_MISMATCH",
                parameter="power",
                value=power_diff,
                expected_range=(0, power_mw * 0.1),
                severity=AlertLevel.WARNING,
                message=f"Sai lệch công suất: Đo={power_mw:.1f}mW, Tính={calculated_power:.1f}mW"
            ))
        
        self.anomalies.extend(anomalies)
        return anomalies
    
    def analyze_degradation_trend(self, data: pd.DataFrame) -> Dict:
        """
        Phân tích xu hướng suy giảm hiệu suất theo thời gian
        
        Sử dụng linear regression để ước tính tốc độ suy giảm
        """
        if len(data) < 10:
            return {
                'degradation_rate': 0,
                'trend': 'insufficient_data',
                'message': 'Không đủ dữ liệu để phân tích xu hướng'
            }
        
        # Tính PR cho mỗi bản ghi
        prs = []
        for _, row in data.iterrows():
            irradiance = self.lux_to_irradiance(row.get('Lux', 0))
            if irradiance > 100:  # Chỉ tính khi có ánh sáng
                pr = self.calculate_performance_ratio(
                    row.get('milliWatt', 0),
                    irradiance,
                    row.get('Temp', 25)
                )
                prs.append(pr)
        
        if len(prs) < 5:
            return {
                'degradation_rate': 0,
                'trend': 'insufficient_data',
                'message': 'Không đủ dữ liệu trong điều kiện ánh sáng tốt'
            }
        
        # Tính xu hướng bằng linear regression đơn giản
        x = np.arange(len(prs))
        prs_array = np.array(prs)
        
        # y = ax + b
        n = len(x)
        sum_x = np.sum(x)
        sum_y = np.sum(prs_array)
        sum_xy = np.sum(x * prs_array)
        sum_x2 = np.sum(x ** 2)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        # Đánh giá xu hướng
        avg_pr = np.mean(prs_array)
        if slope < -0.1:
            trend = 'degrading'
            message = f'Hiệu suất đang giảm, tốc độ: {abs(slope):.2f}%/đơn vị thời gian'
        elif slope > 0.1:
            trend = 'improving'
            message = f'Hiệu suất đang cải thiện, tốc độ: {slope:.2f}%/đơn vị thời gian'
        else:
            trend = 'stable'
            message = 'Hiệu suất ổn định'
        
        return {
            'degradation_rate': slope,
            'trend': trend,
            'average_pr': avg_pr,
            'min_pr': np.min(prs_array),
            'max_pr': np.max(prs_array),
            'message': message
        }
    
    def get_health_score(self, data: pd.DataFrame) -> Dict:
        """
        Tính điểm sức khỏe tổng thể của tấm pin (0-100)
        
        Các yếu tố:
        1. Performance Ratio trung bình (40%)
        2. Số lượng bất thường (30%)
        3. Xu hướng suy giảm (30%)
        """
        if len(data) < 5:
            return {
                'score': None,
                'grade': 'N/A',
                'message': 'Không đủ dữ liệu để đánh giá'
            }
        
        # 1. Tính PR trung bình
        prs = []
        anomaly_count = 0
        
        for _, row in data.iterrows():
            irradiance = self.lux_to_irradiance(row.get('Lux', 0))
            if irradiance > 100:
                pr = self.calculate_performance_ratio(
                    row.get('milliWatt', 0),
                    irradiance,
                    row.get('Temp', 25)
                )
                prs.append(pr)
                
                # Đếm bất thường
                anomalies = self.detect_anomalies(
                    row.get('U', 0),
                    row.get('Current', 0),
                    row.get('milliWatt', 0),
                    row.get('Lux', 0),
                    row.get('Temp', 25),
                    row.get('Humi', 50)
                )
                anomaly_count += len([a for a in anomalies if a.severity == AlertLevel.CRITICAL])
        
        if len(prs) == 0:
            return {
                'score': None,
                'grade': 'N/A',
                'message': 'Không có dữ liệu trong điều kiện ánh sáng tốt'
            }
        
        avg_pr = np.mean(prs)
        
        # Điểm từ PR (40%)
        pr_score = min(avg_pr, 100) * 0.4
        
        # Điểm từ số lượng bất thường (30%)
        anomaly_ratio = anomaly_count / len(data)
        anomaly_score = max(0, (1 - anomaly_ratio * 5)) * 30  # Mỗi 20% bất thường trừ hết điểm
        
        # Điểm từ xu hướng (30%)
        trend_analysis = self.analyze_degradation_trend(data)
        if trend_analysis['trend'] == 'stable':
            trend_score = 30
        elif trend_analysis['trend'] == 'improving':
            trend_score = 30
        elif trend_analysis['trend'] == 'degrading':
            trend_score = max(0, 30 + trend_analysis['degradation_rate'] * 10)
        else:
            trend_score = 15  # Không đủ dữ liệu
        
        total_score = pr_score + anomaly_score + trend_score
        
        # Xếp hạng
        if total_score >= 90:
            grade = 'A'
            message = 'Tấm pin hoạt động xuất sắc'
        elif total_score >= 80:
            grade = 'B'
            message = 'Tấm pin hoạt động tốt'
        elif total_score >= 70:
            grade = 'C'
            message = 'Tấm pin hoạt động bình thường'
        elif total_score >= 60:
            grade = 'D'
            message = 'Tấm pin cần được kiểm tra'
        else:
            grade = 'F'
            message = 'Tấm pin có vấn đề nghiêm trọng'
        
        return {
            'score': round(total_score, 1),
            'grade': grade,
            'message': message,
            'details': {
                'pr_contribution': round(pr_score, 1),
                'anomaly_contribution': round(anomaly_score, 1),
                'trend_contribution': round(trend_score, 1),
                'average_pr': round(avg_pr, 1),
                'anomaly_count': anomaly_count
            }
        }
    
    def generate_daily_report(self, data: pd.DataFrame, date: str) -> Dict:
        """
        Tạo báo cáo phân tích theo ngày
        """
        if len(data) == 0:
            return {
                'date': date,
                'status': 'no_data',
                'message': 'Không có dữ liệu cho ngày này'
            }
        
        # Tính các thống kê
        stats = {
            'voltage': {
                'min': data['U'].min() if 'U' in data else 0,
                'max': data['U'].max() if 'U' in data else 0,
                'avg': data['U'].mean() if 'U' in data else 0
            },
            'current': {
                'min': data['Current'].min() if 'Current' in data else 0,
                'max': data['Current'].max() if 'Current' in data else 0,
                'avg': data['Current'].mean() if 'Current' in data else 0
            },
            'power': {
                'min': data['milliWatt'].min() if 'milliWatt' in data else 0,
                'max': data['milliWatt'].max() if 'milliWatt' in data else 0,
                'avg': data['milliWatt'].mean() if 'milliWatt' in data else 0,
                'total_energy': (data['milliWatt'].sum() / 1000 / 3600) if 'milliWatt' in data else 0  # Wh
            },
            'temperature': {
                'min': data['Temp'].min() if 'Temp' in data else 0,
                'max': data['Temp'].max() if 'Temp' in data else 0,
                'avg': data['Temp'].mean() if 'Temp' in data else 0
            },
            'illuminance': {
                'min': data['Lux'].min() if 'Lux' in data else 0,
                'max': data['Lux'].max() if 'Lux' in data else 0,
                'avg': data['Lux'].mean() if 'Lux' in data else 0
            }
        }
        
        # Tính hiệu suất
        health = self.get_health_score(data)
        trend = self.analyze_degradation_trend(data)
        
        # Đếm bất thường
        all_anomalies = []
        for _, row in data.iterrows():
            anomalies = self.detect_anomalies(
                row.get('U', 0),
                row.get('Current', 0),
                row.get('milliWatt', 0),
                row.get('Lux', 0),
                row.get('Temp', 25),
                row.get('Humi', 50)
            )
            all_anomalies.extend(anomalies)
        
        anomaly_summary = {}
        for a in all_anomalies:
            key = a.anomaly_type
            if key not in anomaly_summary:
                anomaly_summary[key] = {'count': 0, 'severity': a.severity.value}
            anomaly_summary[key]['count'] += 1
        
        return {
            'date': date,
            'status': 'success',
            'record_count': len(data),
            'statistics': stats,
            'health_score': health,
            'trend_analysis': trend,
            'anomalies': anomaly_summary,
            'recommendations': self._generate_recommendations(health, trend, anomaly_summary)
        }
    
    def _generate_recommendations(self, health: Dict, trend: Dict, anomalies: Dict) -> List[str]:
        """Tạo các khuyến nghị dựa trên phân tích"""
        recommendations = []
        
        if health.get('score') and health['score'] < 70:
            recommendations.append("⚠️ Kiểm tra vệ sinh bề mặt tấm pin (bụi, lá cây, chim phóng uế)")
        
        if trend.get('trend') == 'degrading':
            recommendations.append("📉 Hiệu suất đang giảm - Kiểm tra kết nối điện và tình trạng tấm pin")
        
        if 'HIGH_TEMPERATURE' in anomalies:
            recommendations.append("🌡️ Nhiệt độ cao - Kiểm tra hệ thống thông gió/làm mát")
        
        if 'CRITICAL_LOW_PERFORMANCE' in anomalies:
            recommendations.append("🔴 Hiệu suất rất thấp - Kiểm tra ngay: có thể bị che bóng hoặc hỏng cell")
        
        if 'POWER_MISMATCH' in anomalies:
            recommendations.append("⚡ Sai lệch công suất - Kiểm tra cảm biến hoặc mạch đo")
        
        if not recommendations:
            recommendations.append("✅ Hệ thống hoạt động bình thường")
        
        return recommendations


def calculate_panel_efficiency_simple(voltage: float, current: float, 
                                       power_mw: float, lux: float,
                                       panel_area: float = 0.65) -> Dict:
    """
    Hàm tiện ích để tính nhanh hiệu suất tấm pin
    
    Returns:
        Dict với các thông số hiệu suất
    """
    analyzer = SolarPanelAnalyzer()
    irradiance = analyzer.lux_to_irradiance(lux)
    
    return {
        'irradiance_wm2': round(irradiance, 2),
        'efficiency_percent': round(analyzer.calculate_efficiency(power_mw, irradiance), 2),
        'power_output_w': round(power_mw / 1000, 4),
        'input_power_w': round(irradiance * panel_area, 2)
    }

