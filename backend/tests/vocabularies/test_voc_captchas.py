from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabCaptchas:
    name = "plone.formblock.captcha.providers"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["honeypot", "Honeypot Support"],
        ],
    )
    def test_term(self, token, title):
        term = self.vocab.getTermByToken(token)
        assert term is not None
        assert term.title == title
