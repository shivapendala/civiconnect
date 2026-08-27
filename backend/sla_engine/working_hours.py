import datetime
from typing import Tuple, List, Optional
from django.utils import timezone
from .models import HolidayCalendar

class WorkingHoursCalculator:
    """
    Calculates precise business operating windows (e.g. 08:00 to 18:00 Mon-Fri)
    excluding municipal holidays and weekend shifts.
    """
    DEFAULT_START_TIME = datetime.time(8, 0)
    DEFAULT_END_TIME = datetime.time(18, 0)

    @classmethod
    def is_working_day(cls, tenant_id: str, check_date: datetime.date) -> bool:
        # Weekend check (5=Saturday, 6=Sunday)
        if check_date.weekday() in (5, 6):
            return False
            
        # Holiday check
        is_holiday = HolidayCalendar.objects.filter(
            tenant_id=tenant_id,
            holiday_date=check_date
        ).exists()
        
        return not is_holiday

    @classmethod
    def add_working_hours(cls, tenant_id: str, start_dt: datetime.datetime, hours_to_add: float) -> datetime.datetime:
        """
        Adds specified working hours to start_dt skipping non-business hours, weekends, and holidays.
        """
        current_dt = start_dt
        remaining_minutes = int(hours_to_add * 60)
        
        while remaining_minutes > 0:
            current_date = current_dt.date()
            if not cls.is_working_day(tenant_id, current_date):
                current_dt = datetime.datetime.combine(
                    current_date + datetime.timedelta(days=1),
                    cls.DEFAULT_START_TIME,
                    tzinfo=current_dt.tzinfo
                )
                continue
                
            day_start = datetime.datetime.combine(current_date, cls.DEFAULT_START_TIME, tzinfo=current_dt.tzinfo)
            day_end = datetime.datetime.combine(current_date, cls.DEFAULT_END_TIME, tzinfo=current_dt.tzinfo)
            
            if current_dt < day_start:
                current_dt = day_start
            elif current_dt >= day_end:
                current_dt = datetime.datetime.combine(
                    current_date + datetime.timedelta(days=1),
                    cls.DEFAULT_START_TIME,
                    tzinfo=current_dt.tzinfo
                )
                continue
                
            available_minutes = int((day_end - current_dt).total_seconds() / 60)
            if remaining_minutes <= available_minutes:
                current_dt += datetime.timedelta(minutes=remaining_minutes)
                remaining_minutes = 0
            else:
                remaining_minutes -= available_minutes
                current_dt = datetime.datetime.combine(
                    current_date + datetime.timedelta(days=1),
                    cls.DEFAULT_START_TIME,
                    tzinfo=current_dt.tzinfo
                )
                
        return current_dt
