from dotenv.main import load_dotenv
import uvicorn
from app import app
from app.core.config import load_config

CONFIG = load_config()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=CONFIG.WEB_SERVER_PORT,
        reload=CONFIG.PROJ_RELOAD,
    )
