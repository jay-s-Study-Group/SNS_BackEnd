import uvicorn
from dotenv import load_dotenv
from app.core.config import load_config

CONFIG = load_config()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=CONFIG.WEB_SERVER_PORT,
        reload=CONFIG.PROJ_RELOAD,
    )
