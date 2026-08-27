import json
import logging
from typing import Dict, Any, List
from django.utils import timezone
from .models import SensorDevice, TelemetryReading, SensorAlert

logger = logging.getLogger(__name__)

class IoTStreamProcessor:
    """Real-time MQTT / WebSocket high-frequency sensor telemetry stream batch aggregator."""
    
    def __init__(self, buffer_size: int = 100):
        self.buffer_size = buffer_size
        self._buffer: List[Dict[str, Any]] = []

    def push_packet(self, packet: Dict[str, Any]):
        self._buffer.append(packet)
        if len(self._buffer) >= self.buffer_size:
            self.flush()

    def flush(self):
        if not self._buffer:
            return
        batch = list(self._buffer)
        self._buffer.clear()
        
        device_ids = {p["device_id"] for p in batch}
        devices = {d.device_id: d for d in SensorDevice.objects.filter(device_id__in=device_ids)}
        
        readings_to_create = []
        now = timezone.now()
        
        for p in batch:
            dev = devices.get(p["device_id"])
            if dev:
                val = float(p.get("value", 0.0))
                readings_to_create.append(
                    TelemetryReading(
                        device=dev,
                        value=val,
                        unit=p.get("unit", "units"),
                        raw_payload=p.get("payload", {}),
                        is_anomaly=(val >= dev.threshold_warning),
                        timestamp=now
                    )
                )
                
        if readings_to_create:
            TelemetryReading.objects.bulk_create(readings_to_create)
            logger.info(f"Flushed {len(readings_to_create)} IoT telemetry readings in bulk.")
