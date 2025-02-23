import pytest
from pydantic import ValidationError

from llm_tool_commit.config import ModelOptions, ToolConfiguration


def test_model_options():
    """Tests the options model class."""
    model_options = ModelOptions()

    assert hasattr(model_options, "temperature"), "No attribute `temperature`"
    assert hasattr(model_options, "top_p"), "No attribute `top_p`"
    assert hasattr(model_options, "top_k"), "No attribute `top_k`"
    assert hasattr(model_options, "num_predict"), "No attribute `num_predict`"

    # Check validity of values
    assert (
        isinstance(model_options.temperature, float)
        and model_options.temperature >= 0
        and model_options.temperature <= 1.0
    ), "`temperature` should be a floating number between 0.0 and 1.0"
    assert (
        isinstance(model_options.top_p, float) and model_options.top_p >= 0.0 and model_options.top_p <= 1.0
    ), "`top_p` should be a floating number between 0.0 and 1.0"
    assert (
        isinstance(model_options.top_k, int) and model_options.top_k >= 1
    ), "`top_k` should be an integer greater than 1"
    assert (
        isinstance(model_options.num_predict, int) and model_options.num_predict >= 1
    ), "`num_predict` should be an integer greater than 1"


def test_default_configuration():
    """Tests the initialization of the configuration object."""
    config = ToolConfiguration()

    # Check each attribute
    assert hasattr(config, "model"), "No attribute `model`"
    assert hasattr(config, "message_max_length"), "No attribute `message_max_length`"
    assert hasattr(config, "max_size_diff"), "No attribute `max_size_diff`"

    # Check validity of values
    assert isinstance(config.model, str), "`model` should a string"
    assert (
        isinstance(config.message_max_length, int) and config.message_max_length >= 1
    ), "`message_max_length` should be an integer greater than 1"
    assert (
        isinstance(config.max_size_diff, int) and config.max_size_diff >= 1
    ), "`max_size_diff` should be an integer greater than 1"


def test_wrong_configuration():
    """Tests configuration objects with erroneous input."""
    with pytest.raises(ValidationError):
        ToolConfiguration(model=0)

    with pytest.raises(ValidationError):
        ToolConfiguration(message_max_length=0)

    with pytest.raises(ValidationError):
        ToolConfiguration(max_size_diff=0)


def test_wrong_model_options():
    """Tests model options objects with erroneous input."""

    with pytest.raises(ValidationError):
        ToolConfiguration(num_predict=-2)

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
