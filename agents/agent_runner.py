import threading
import time
from coordinator_agent import CoordinatorAgent
from logger_monitor_agent import LoggerMonitorAgent
from app.routes import push_log_update

def run_coordinator():
    coordinator = CoordinatorAgent()
    while True:
        # Simulated Zeek log entry and corresponding network traffic data.
        zeek_log_entry = "2023-10-10 12:00:00, Suspicious IP 192.168.1.100 observed, failed login attempt for user 'admin'"
        traffic_data = [
            ("192.168.1.100", "10.0.0.5"),
            ("192.168.1.101", "10.0.0.5")
        ]
        result = coordinator.coordinate(zeek_log_entry, traffic_data)
        push_log_update(result)  # Pushes the aggregated result to connected Socket.IO clients.
        print("Coordinator Result:", result)
        time.sleep(5)  # Pause for 5 seconds between threat evaluations.

def run_logger():
    logger_event = LoggerMonitorAgent()
    while True:
        logger_event.log_event("Heartbeat", {"status": "running"})
        time.sleep(10)  # Log heartbeat every 10 seconds.

if __name__ == "__main__":
    # Start coordinator agent in its own thread.
    coordinator_thread = threading.Thread(target=run_coordinator)
    coordinator_thread.daemon = True
    coordinator_thread.start()

    # Start logger agent in its own thread.
    logger_thread = threading.Thread(target=run_logger)
    logger_thread.daemon = True
    logger_thread.start()

    # Keep the main thread alive.
    while True:
        time.sleep(1)
