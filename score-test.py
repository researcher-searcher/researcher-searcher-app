from functions import api_search
from loguru import logger

query='genome wide association studies'

res1 = api_search(text=query,method='full')
res2 = api_search(text=query,method='vec')
logger.info(res1)
logger.info(res2)