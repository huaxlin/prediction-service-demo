from importlib import import_module
from fastapi import FastAPI
from loguru import logger
from app.config import settings

# dynamic import by configuration
if not settings.ML_MODULE_NAME:
    raise ValueError(
        'got incorrect configurations, '
        f'ML_MODULE_NAME:{settings.ML_MODULE_NAME}'
    )
pkg_name = settings.ML_MODULE_NAME
predict_module_name = 'predict'
PREDICT_MODULE = f'{pkg_name}.{predict_module_name}'
try:
    logger.info(f'load predict module by config, predict module: {PREDICT_MODULE}')
    predict_module = import_module(PREDICT_MODULE)
    logger.info('get predict function("predict") from predict module')
    predict_fn = getattr(predict_module, 'predict')
except ModuleNotFoundError as exc:
    raise
except AttributeError as exc:
    raise


app = FastAPI()


@app.get("/health", response_model=str)
def read_root():
    return 'ok'


@app.post("/predict", response_model=dict)
def predict_handler(body: dict):
    ret = predict_fn(body)
    return ret


if __name__ == "__main__":
    # debugging mode
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
