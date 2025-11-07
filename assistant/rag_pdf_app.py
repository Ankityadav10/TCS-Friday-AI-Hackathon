import random
import pandas as pd
from datetime import datetime, timedelta

# Generate synthetic logs
levels = ["INFO", "WARN", "ERROR", "CRITICAL"]
components = ["Database", "API", "Cache", "AuthService", "LoadBalancer"]
messages = [
    "Connection timeout",
    "Memory usage high",
    "Disk I/O spike detected",
    "Database connection lost",
    "Cache miss rate increased",
    "CPU usage exceeded threshold"
]

start_time = datetime.now() - timedelta(hours=1)
data = []
for i in range(200):
    ts = start_time + timedelta(seconds=i * 20)
    data.append({
        "timestamp": ts,
        "level": random.choice(levels),
        "component": random.choice(components),
        "message": random.choice(messages)
    })

logs_df = pd.DataFrame(data)
logs_df.to_csv("synthetic_logs.csv", index=False)
print("✅ Synthetic logs saved to synthetic_logs.csv")
