"""
उपयोगिता फंक्शन
Utility Functions
"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_directories():
    """आवश्यक निर्देशिका बनाएं यदि वे मौजूद न हों"""
    directories = [
        "config",
        "data",
        "data/offline_model",
        "logs",
        "screenshots",
        "modules"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"निर्देशिका सुनिश्चित की गई: {directory}")


def load_json(filepath):
    """JSON फ़ाइल को सुरक्षित रूप से लोड करें"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"{filepath} से JSON लोड करने में त्रुटि: {e}")
        return None


def save_json(filepath, data):
    """JSON फ़ाइल में डेटा सुरक्षित रूप से सहेजें"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"डेटा {filepath} में सहेजा गया")
        return True
    except Exception as e:
        logger.error(f"{filepath} में JSON सहेजने में त्रुटि: {e}")
        return False


def setup_logging(log_level="INFO"):
    """अनुप्रयोग लॉगिंग सेटअप करें"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # फ़ाइल लॉगिंग
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.FileHandler('logs/jarvis.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger.info("लॉगिंग इनिशियलाइज़ किया गया")


def get_system_info():
    """सिस्टम जानकारी प्राप्त करें"""
    import platform
    import psutil
    
    try:
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "processor": platform.processor(),
            "ram": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "cpu_cores": psutil.cpu_count()
        }
        return info
    except Exception as e:
        logger.error(f"सिस्टम जानकारी प्राप्त करने में त्रुटि: {e}")
        return None


def check_dependencies():
    """जांचें कि सभी आवश्यक पैकेज इंस्टॉल हैं"""
    required_packages = [
        'pyaudio',
        'pyttsx3',
        'vosk',
        'requests',
        'pyautogui',
        'keyboard',
        'mouse',
        'pynput',
        'psutil',
        'sounddevice',
        'numpy',
        'googletrans',
        'gtts'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"लापता पैकेज: {missing_packages}")
        return False
    else:
        logger.info("सभी निर्भरताएं इंस्टॉल हैं")
        return True


def format_response(message, status="info"):
    """स्थिति के साथ प्रतिक्रिया संदेश को फॉर्मेट करें"""
    status_symbols = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    symbol = status_symbols.get(status, "ℹ️")
    return f"{symbol} {message}"


if __name__ == "__main__":
    setup_logging()
    setup_directories()
    
    print(get_system_info())
    print(f"निर्भरताएं ठीक हैं: {check_dependencies()}")
