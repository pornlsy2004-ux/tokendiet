"""tokendiet — keep only the context your task actually needs."""
from .core import (
    SubtractionResult,
    count_tokens,
    lexical_scores,
    llm_backend,
    split_sentences,
    subtract,
)

__all__ = [
    "subtract",
    "llm_backend",
    "lexical_scores",
    "split_sentences",
    "count_tokens",
    "SubtractionResult",
]
__version__ = "0.1.0"
