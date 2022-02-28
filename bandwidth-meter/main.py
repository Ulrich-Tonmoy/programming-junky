import time
import psutil

last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

while True:
    received = psutil.net_io_counters().bytes_recv
    sent = psutil.net_io_counters().bytes_sent
    total = received + sent

    new_received = received - last_received
    new_sent = sent - last_sent
    new_total = total - last_total

    new_received_mb = new_received / 1024 / 1024
    new_sent_mb = new_sent / 1024 / 1024
    new_total_mb = new_total / 1024 / 1024

    print(f"{new_received_mb:.3f} MB Received, {new_sent_mb:.3f} MB Sent, {new_total_mb:.3f} MB Total")

    last_received = received
    last_sent = sent
    last_total = total

    time.sleep(1)
