import os
import logging
from langchain.llms.openai import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

# Set up logging so that logs go into cyber_centinel/logfiles/llm_log_parser.log
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logfiles", "llm_log_parser.log")
# Ensure the log directory exists.
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("LLMLogParserAgent")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

class LLMLogParserAgent:
    """
    An agent that uses a language model via LangChain to parse Zeek log entries 
    and extract suspicious threat indicators.
    """

    def __init__(self):
        # Initialize the language model (ensure your API keys are set in your environment)
        self.llm = OpenAI(temperature=0)
        template = (
            "Given the following Zeek log entry, extract the suspicious information.\n"
            "Log: {log_line}\n"
            "Extract: suspicious IP addresses, failed login attempts, and any anomalies."
        )
        self.prompt = PromptTemplate(input_variables=["log_line"], template=template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
    def parse_log(self, log_line: str) -> dict:
        """
        Parse a single Zeek log entry and extract threat indicators.
        
        :param log_line: A raw Zeek log entry as a string.
        :return: A dict containing the key 'parsed_result' with the LLM output.
                 In case of error, returns a dict with the error message.
        """
        try:
            result_text = self.chain.run(log_line=log_line)
            parsed_result = {"parsed_result": result_text}
            logger.info("Successfully parsed log entry. Log: %s | Result: %s", log_line, result_text)
            return parsed_result
        except Exception as e:
            logger.exception("Error parsing log entry: %s", log_line)
            return {"error": str(e)}