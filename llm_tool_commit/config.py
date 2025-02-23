from pydantic import BaseModel, confloat, conint


class ModelOptions(BaseModel):
    """Class to store options to give the model.

    Attributes:
        temperature (float): Temperature of the model. Should be between 0.0 and 1.0. Defaults to 0.8.
        top_p (float): Top p cumulative probability truncation. Should be between 0.0 and 1.0.  Defaults to 0.9.
        top_k (int): Top k tokens truncation. Should be greater than 1. Defaults to 40.
    """

    temperature: confloat(ge=0.0, le=1.0) = 0.8
    top_p: confloat(ge=0.0, le=1.0) = 1.0
    top_k: conint(ge=1) = 40


class ToolConfiguration(BaseModel):
    """Configuration class.

    Attributes:
        model (str): Name of model to use (available through Ollama). Defaults to Qwen2.5-coder with 1.5B parameters.
        max_size (int): Maximum size of the git diff to use before truncating. Should be greater than 1. Defaults to 4096.
        message_max_length (int): Maximal length of the commit message. Should be an integer greater than 1. Defaults to 150.
    """

    model: str = "qwen2.5-coder:1.5b"
    max_size: conint(ge=1) = 4096
    message_max_length: conint(ge=1) = 150
