"""Quickstart — subtract a context down to what the question needs.

    python examples/quickstart.py
"""
from tokendiet import subtract

context = """Global Travel & Expense Policy

Economy class is required for flights under 6 hours; business class requires VP approval.

Lodging: the standard reimbursable hotel rate is capped at $220 per night. A higher cap of $260 applies to high-cost domestic metros (New York, San Francisco, Boston). For designated high-cost international cities - Tokyo, Zurich, and Singapore - the nightly hotel cap is raised to $340.

Meals are reimbursed per-diem: $75/day domestic, $90/day international."""

# Local lexical backend — no API key required.
res = subtract("What is the hotel rate cap for Tokyo?", context)
print("SUBTRACTED CONTEXT:\n", res.text, "\n")
print("STATS:", res.stats)

# Answer-impact backend — bring your own model (wins on the hard cases):
#
#     from tokendiet import llm_backend
#
#     def my_llm(prompt: str) -> str:
#         ...  # call OpenAI / a local model / anything; return the text
#
#     res = subtract(question, context, backend=llm_backend(my_llm))
#     print(res.text, res.distractors, res.stats)
