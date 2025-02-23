import pytest
from pydantic import ValidationError

from llm_tool_commit.config import ToolConfiguration


def test_default_configuration():
    """Test the initialization of the configuration object."""
    config = ToolConfiguration()

    # Check each attribute
    assert hasattr(config, "model") and isinstance(config.model, str), "No attribute `model`"
    assert hasattr(config, "max_size"), "No attribute `max_size`"
    assert hasattr(config, "temperature"), "No attribute `temperature`"
    assert hasattr(config, "top_p"), "No attribute `top_p`"
    assert hasattr(config, "top_k") and isinstance(config.top_k, int), "No attribute `top_k`"

    # Check validity of values
    assert isinstance(config.model, str), "`model` should a string"
    assert isinstance(config.max_size, int) and config.max_size >= 1, "`max_size` should be an integer greater than 1"
    assert (
        isinstance(config.temperature, float) and config.temperature >= 0 and config.temperature <= 1.0
    ), "`temperature` should be a floating number between 0.0 and 1.0"
    assert (
        isinstance(config.top_p, float) and config.top_p >= 0.0 and config.top_p <= 1.0
    ), "`top_p` should be a floating number between 0.0 and 1.0"
    assert isinstance(config.top_k, int) and config.top_k >= 1, "`top_k` should be an integer greater than 1"


def test_wrong_configuration():
    """Test configuration objects with erroneous input."""
    with pytest.raises(ValidationError):
        ToolConfiguration(model=0)

    with pytest.raises(ValidationError):
        ToolConfiguration(max_size=1.5)

    with pytest.raises(ValidationError):
        ToolConfiguration(temperature=2.0)

    with pytest.raises(ValidationError):
        ToolConfiguration(temperature=-1.0)

    with pytest.raises(ValidationError):
        ToolConfiguration(top_p=2.0)

    with pytest.raises(ValidationError):
        ToolConfiguration(top_k=1.5)

    with pytest.raises(ValidationError):
        ToolConfiguration(top_k=0)
