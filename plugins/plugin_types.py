from enum import Enum

class PluginType(Enum):
    DATA_RETRIEVAL = 0
    DATA_PROCESSING = 1
    SECONDARY_PROCESSING = 2
    DATA_VISUALIZATION = 3
    GENERIC = 3
