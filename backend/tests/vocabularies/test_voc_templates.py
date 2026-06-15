from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabTemplates:
    name = "plone.formblock.mail.templates"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["default", "default"],
        ],
    )
    def test_term(self, token, title):
        term = self.vocab.getTermByToken(token)
        assert term is not None
        assert term.title == title
