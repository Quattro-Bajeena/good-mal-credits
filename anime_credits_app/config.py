from pathlib import Path

import anime_credits_app
from anime_credits_app import app



app_root = Path(anime_credits_app.__file__).parent
#print("app root from config", app_root)

anime_credits_app.adc.config.config_database(app_root)
#print("resurce types", anime_credits_app.adc.config.resource_types)

@app.context_processor
def inject_python_functions():
    return {'len' : len}