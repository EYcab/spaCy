# coding: utf8
from __future__ import unicode_literals

from ...attrs import LANG
from ...language import Language
from ...tokens import Doc


class ChineseDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters[LANG] = lambda text: 'zh'  # for pickling
    use_jieba = True


class Chinese(Language):
    lang = 'zh'
    Defaults = ChineseDefaults  # override defaults

    def make_doc(self, text):
        if self.Defaults.use_jieba:
            try:
                import jieba
            except ImportError:
                msg = ("Jieba not installed. Either set Chinese.use_jieba = False, "
                       "or install it https://github.com/fxsjy/jieba")
                raise ImportError(msg)
            words = list(jieba.cut(text, cut_all=False))
            words = [x for x in words if x]
            return Doc(self.vocab, words=words, spaces=[False]*len(words))
        else:
            words = []
            spaces = []
            doc = self.tokenizer(text)
            for token in self.tokenizer(text):
                words.extend(list(token.text))
                spaces.extend([False]*len(token.text))
                spaces[-1] = bool(token.whitespace_)
            return Doc(self.vocab, words=words, spaces=spaces)


__all__ = ['Chinese']
