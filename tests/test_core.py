from tokendiet import llm_backend, split_sentences, subtract

DOC = """Nimbus Cloud plans.

The Team plan is capped at 25 seats; beyond that you must upgrade. The Free plan allows 3 seats. Business and Enterprise allow unlimited seats."""


def test_split_sentences():
    assert len(split_sentences(DOC)) >= 3


def test_subtract_actually_subtracts():
    res = subtract("How many seats on the Team plan?", DOC)
    # It must drop something and keep something — that's the whole point.
    assert res.stats["n_kept"] >= 1
    assert res.stats["n_kept"] < res.stats["n_chunks"]
    assert res.stats["kept_tokens"] < res.stats["raw_tokens"]
    assert 0 < res.stats["ratio"] < 1.0


def test_llm_backend_selects_and_flags():
    # A fake model that keeps sentence 0 and flags sentence 1 as a distractor.
    fake = lambda prompt: '{"keep": [0], "distractors": [1]}'
    res = subtract("q", DOC, backend=llm_backend(fake))
    assert res.stats["n_kept"] == 1
    assert res.stats["n_distractors"] == 1
    assert res.text == split_sentences(DOC)[0]


def test_llm_backend_never_empty():
    # If the model returns nothing, we must still keep at least one sentence.
    res = subtract("q", DOC, backend=llm_backend(lambda p: '{"keep": [], "distractors": []}'))
    assert res.stats["n_kept"] >= 1
