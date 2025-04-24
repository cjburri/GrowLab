from app.hardware.WaterPump import WaterPump

pump = WaterPump(23, debug_mode=True)

pump.pulse_water(1, 1, 1)

print(pump.get_usage_stats())
