from abc import ABC, abstractmethod
from enum import Enum

class OPTION_TYPE(Enum):
    CALL_OPTION = 'Call Option'
    PUT_OPTION = 'Put Option'

class OptionPricingModel(ABC):
    """Abstract class defining interface for option pricing models."""

    @abstractmethod
    def calculate_option_price(self, option_type):
        """Calculates option price based on the specified option type."""
        pass
