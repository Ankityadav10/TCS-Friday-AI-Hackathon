import random
import pandas as pd
from datetime import datetime, timedelta

# Synthetic parameters
levels = ["INFO", "WARN", "ERROR", "CRITICAL"]
components = ["Database", "API", "Cache", "AuthService", "LoadBalancer"]
messages = [
    "Connection timeout",
    "Memory usage high",
    "Disk I/O spike detected",
    "Database connection lost",
    "Cache miss rate increased",
    "CPU usage exceeded threshold",
    "Network latency above threshold",
    "Out of memory error",
    "Authentication service unavailable",
    "Read/write lock contention detected"
]

# Generate timestamps for 2 hours
start_time = datetime.now() - timedelta(hours=2)
rows = []
for i in range(400):
    ts = start_time + timedelta(seconds=i * 15)
    level = random.choices(levels, weights=[0.5, 0.3, 0.15, 0.05])[0]
    comp = random.choice(components)
    msg = random.choice(messages)
    rows.append({
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "component": comp,
        "message": msg
    })

# Add a few correlated error bursts (simulated outage)
for i in range(10):
    rows.append({
        "timestamp": (start_time + timedelta(minutes=90 + i)).strftime("%Y-%m-%d %H:%M:%S"),
        "level": "CRITICAL",
        "component": "Database",
        "message": "Connection pool exhausted, unable to allocate connection"
    })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Shuffle for realism
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv("synthetic_logs.csv", index=False)
print("✅ Synthetic log data generated: synthetic_logs.csv")
print(df.head())
