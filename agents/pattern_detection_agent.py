import os
import io
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import logging
from transformers import ViTForImageClassification, ViTFeatureExtractor

# Construct the log file path relative to this file's directory (agents/)
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logfiles", "pattern_detection.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Set up the logger for PatternDetectionAgent.
logger = logging.getLogger("PatternDetectionAgent")
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()

file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class PatternDetectionAgent:
    def __init__(self):
        # Initialize the Vision Transformer components
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
        self.model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
        
    def generate_graph_image(self, traffic_data) -> io.BytesIO:
        """
        Builds a NetworkX graph from a list of edge tuples (traffic data),
        draws it with matplotlib, and returns a BytesIO image buffer.
        """
        try:
            G = nx.Graph()
            G.add_edges_from(traffic_data)
            fig, ax = plt.subplots()
            nx.draw(G, ax=ax, with_labels=True)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            logger.info("Graph image generated successfully from traffic data: %s", traffic_data)
            return buf
        except Exception as e:
            logger.exception("Error generating graph image from traffic data: %s", traffic_data)
            raise e
        
    def detect_pattern(self, traffic_data) -> dict:
        """
        Uses the generated graph image as input to a Vision Transformer (ViT)
        for pattern detection.
        
        :param traffic_data: A list of edge tuples representing network traffic.
        :return: A dictionary with the key 'predicted_class' containing the detection result.
        """
        try:
            logger.info("Starting pattern detection for traffic data: %s", traffic_data)
            # Generate the graph image based on traffic data.
            image_buf = self.generate_graph_image(traffic_data)
            # Open the image from the in-memory buffer.
            image = Image.open(image_buf)
            # Preprocess the image and obtain model inputs.
            inputs = self.feature_extractor(images=image, return_tensors="pt")
            # Get predictions from the Vision Transformer.
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class = logits.argmax(-1).item()
            result = {"predicted_class": predicted_class}
            logger.info("Pattern detection result: %s", result)
            return result
        except Exception as e:
            logger.exception("Error detecting pattern from traffic data: %s", traffic_data)
            return {"error": str(e)}
