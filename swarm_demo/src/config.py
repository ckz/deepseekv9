"""
Configuration management for the financial news analysis system.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

class Config:
    """配置管理类"""
    
    @staticmethod
    def get_api_keys() -> Dict[str, str]:
        """获取API密钥配置"""
        keys = {
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
            "serpapi": os.getenv("SERPAPI_API_KEY"),
            "openrouter_base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        }
        
        # 验证必要的API密钥
        missing_keys = [k for k, v in keys.items() if not v]
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
            
        return keys
    
    @staticmethod
    def get_llm_config() -> Dict[str, Any]:
        """获取LLM配置"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Set OpenAI API key for AutoGen
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        return {
            "temperature": float(os.getenv("TEMPERATURE", 0.7)),
            "max_tokens": int(os.getenv("MAX_TOKENS", 4000)),
            "model": os.getenv("LLM_MODEL", "anthropic/claude-3-sonnet"),
            "request_timeout": 300,
            "seed": 42,
            "config_list_timeout": 120,
            "use_cache": True,
            "context_length": 4096,
            "api_base": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "api_type": "openai",
            "api_key": api_key,
            "default_headers": {
                "HTTP-Referer": "https://github.com/microsoft/autogen",
                "X-Title": "AutoGen Financial News Analysis"
            }
        }
    
    @staticmethod
    def get_system_config() -> Dict[str, Any]:
        """获取系统配置"""
        return {
            "debug": os.getenv("DEBUG", "False").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO")
        }

def validate_config():
    """验证配置完整性"""
    try:
        # 验证API密钥
        Config.get_api_keys()
        
        # 验证LLM配置
        llm_config = Config.get_llm_config()
        required_fields = ["temperature", "max_tokens", "model", "api_key", "api_base"]
        if not all(k in llm_config for k in required_fields):
            raise ValueError(f"Missing required LLM configuration parameters: {required_fields}")
        
        # 验证系统配置
        system_config = Config.get_system_config()
        if not all(k in system_config for k in ["debug", "log_level"]):
            raise ValueError("Missing required system configuration parameters")
            
        logger.info("Configuration validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        raise

def get_agent_configs() -> Dict[str, Dict[str, Any]]:
    """获取Agent配置"""
    llm_config = Config.get_llm_config()
    
    return {
        "yahoo_analyst": {
            "name": "Yahoo_Analyst",
            "llm_config": {
                **llm_config,
                "request_timeout": 120
            }
        },
        "google_analyst": {
            "name": "Google_Analyst",
            "llm_config": {
                **llm_config,
                "request_timeout": 120
            }
        },
        "report_writer": {
            "name": "Report_Writer",
            "llm_config": {
                **llm_config,
                "request_timeout": 180
            }
        }
    }