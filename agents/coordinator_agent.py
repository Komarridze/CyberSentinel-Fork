import os
import logging
from datetime import datetime
from llm_log_parser_agent import LLMLogParserAgent
from pattern_detection_agent import PatternDetectionAgent
from response_agents import ResponseAgent

# Build the log file path relative to this file's directory.
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logfiles", "coordinator.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Set up a logger for CoordinatorAgent.
logger = logging.getLogger("CoordinatorAgent")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class CoordinatorAgent:
    def __init__(self):
        self.log_parser = LLMLogParserAgent()
        self.pattern_detector = PatternDetectionAgent()
        self.response_agents = [
            ResponseAgent(agent_type="containment"),
            ResponseAgent(agent_type="alert"),
            ResponseAgent(agent_type="data_collector")
        ]
        
    def coordinate(self, zeek_log_entry: str, traffic_data) -> dict:
        """
        Process a Zeek log entry and corresponding traffic data:
          1. Parses the log entry to extract threat indicators.
          2. Analyzes the traffic data to detect patterns.
          3. Dispatches the aggregated threat data to each response agent.
        Returns an aggregated result with a timestamp.
        """
        try:
            parsed = self.log_parser.parse_log(zeek_log_entry)
            pattern = self.pattern_detector.detect_pattern(traffic_data)
            threat_data = {
                "parsed": parsed.get("parsed_result", ""),
                "pattern": pattern
            }
            responses = [agent.respond(threat_data) for agent in self.response_agents]
            aggregated = {
                "timestamp": datetime.utcnow().isoformat(),
                "threat_details": threat_data,
                "responses": responses
            }
            logger.info("Successfully coordinated threat data: %s", aggregated)
            return aggregated
        except Exception as e:
            logger.exception("Error coordinating log entry: %s, Traffic Data: %s", zeek_log_entry, traffic_data)
            return {"error": str(e)}
