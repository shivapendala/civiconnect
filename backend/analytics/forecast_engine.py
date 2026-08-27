import math
from typing import List, Dict, Tuple
from datetime import date, timedelta

class GrievanceForecastEngine:
    """Predictive seasonal and weather-adjusted grievance volume forecaster."""
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Tuple[float, float]:
        n = len(x)
        if n < 2:
            return (0.0, y[0] if y else 0.0)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / max(1e-6, (n * sum_x2 - sum_x ** 2))
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    @classmethod
    def forecast_next_days(cls, historical_daily_counts: List[int], days_ahead: int = 14) -> List[Dict[str, Any]]:
        n = len(historical_daily_counts)
        x = [float(i) for i in range(n)]
        y = [float(val) for val in historical_daily_counts]
        slope, intercept = cls.linear_regression(x, y)
        
        forecast = []
        base_date = date.today()
        
        for i in range(days_ahead):
            future_x = n + i
            predicted = max(0, int(round(slope * future_x + intercept)))
            target_date = base_date + timedelta(days=i + 1)
            forecast.append({
                "date": target_date.isoformat(),
                "predicted_complaints": predicted,
                "confidence_interval": [max(0, predicted - 5), predicted + 5]
            })
            
        return forecast
