from .clock import get_current_time
from .currency import convert_currency
from .math_eval import calculate_math
from .weather import get_weather
from .wiki import search_wikipedia

ALL_TOOLS = [
    get_current_time,
    get_weather,
    convert_currency,
    search_wikipedia,
    calculate_math,
]