Title: wordup
Slug: wordup
Date: 2026-08-09
Category: package
Oneliner: Walk your own prose one word at a time and choose better ones in context.
Release: v0.2.0
Year: 2026
Stack: Python 3.11+, stdlib only
Topics: Writing, CLI, Zero-dep
Metrics: Version=0.2.0, Downloads/mo=51, Deps=0, Lexicon=86
Links: PyPI=https://pypi.org/project/wordup/, Code=https://github.com/ncarsner/wordup
Stagelabel: Use it

```console
$ uvx wordup "the big problem with this approach"
```

## Notes

A curated lexicon of eighty-six common base words. When one appears in your
text, wordup shows you the sentence it sits in and offers alternatives. You
pick one, or you decline.

The constraint that defines it is that **it never rewrites anything on its own**.
Whether a word is an improvement depends entirely on the sentence around it, and
that judgement belongs to the person reading it — so the tool's job is to
interrupt at the right moment and then get out of the way. That is also why the
lexicon is small and hand-picked rather than generated: a suggestion you have to
evaluate and reject costs more than it saves.
