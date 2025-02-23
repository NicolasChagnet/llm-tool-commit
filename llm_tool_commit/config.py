from dataclasses import dataclass


@dataclass(slots=True)
class ToolConfiguration:
    """Configuration class.

    Attributes:
        model (str): Name of model to use (available through Ollama). Defaults to Qwen2.5-coder with 1.5B parameters.
        max_size (int): Maximum size of the git diff to use before truncating. Defaults to 4096.
        temperature (float): Temperature of the model. Defaults to 0.5.
        top_p (float): Top p cumulative probability truncation. Defaults to 0.9.
        top_k (int): Top k tokens truncation. Defaults to 40.
    """

    model: str = "qwen2.5-coder:1.5b"
    max_size: int = 4096
    temperature: float = 0.5
    top_p: float = 1.0
    top_k: int = 40
