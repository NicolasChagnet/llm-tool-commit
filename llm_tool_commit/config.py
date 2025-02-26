from pydantic import BaseModel, confloat, conint


class ModelOptions(BaseModel):
    """Class to store options to give the model.

    Attributes:
        temperature (float): Temperature of the model. Should be between 0.0 and 1.0. Defaults to 0.4.
        top_p (float): Top p cumulative probability truncation. Should be between 0.0 and 1.0.  Defaults to 0.9.
        top_k (int): Top k tokens truncation. Should be greater than 1. Defaults to 40.
        num_predict (int): Maximum number of tokens for the LLM to predict. Should be positive or -1 (no limit).  Defaults to 2048.
    """

    temperature: confloat(ge=0.0, le=1.0) = 0.8
    top_p: confloat(ge=0.0, le=1.0) = 0.9
    top_k: conint(ge=1) = 40
    num_predict: conint(ge=-1) = 2048


class ToolConfiguration(BaseModel):
    """Configuration class.

    Attributes:
        model (str): Name of model to use (available through Ollama). Defaults to Qwen2.5-coder with 3B parameters.
        max_size_diff (int): Maximum size of the git diff to use before truncating. Should be an integer greater than 1. Defaults to 4096.
        message_max_length (int): Maximal length of the commit message. Should be an integer greater than 1. Defaults to 150.
        type_commit (str | None): Type of the commit to guide the LLM. Defaults to None.
    """

    model: str = "qwen2.5-coder:3b"
    max_size_diff: conint(ge=1) = 4096
    message_max_length: conint(ge=1) = 150
    type_commit: str | None = None
