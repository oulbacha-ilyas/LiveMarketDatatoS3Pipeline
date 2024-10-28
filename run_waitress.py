import logging
from waitress import serve
from datastreamer import app, streaming_agent

# Configure Waitress server logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [Waitress] %(levelname)s: %(message)s')
waitress_logger = logging.getLogger('waitress')

if __name__ == "__main__":
    waitress_logger.info("Starting Waitress server...")
    try:
        serve(app, host="0.0.0.0", port=5000)
    except Exception as e:
        waitress_logger.error("Error running Waitress server: %s", e)
