Title: wordle-words
Slug: wordle-words
Date: 2026-08-21
Category: package
Oneliner: Generate sets of five-letter words that share no letters, to cover the alphabet fast.
Release: v0.4.0
Year: 2026
Stack: Python, stdlib only
Topics: Puzzles, CLI, Zero-dep
Metrics: Version=0.4.0, Downloads/mo=23, Deps=0
Links: PyPI=https://pypi.org/project/wordle-words/, Code=https://github.com/ncarsner/wordle-words
Stagelabel: Use it

```console
$ ww 3
Selected words: ['clack', 'biter', 'found']
Used letters: ABCDEF__I_KL_NO__R_TU_____
```

## Notes

The opening move in Wordle is an information problem, not a vocabulary one. Any
letter you test twice is a letter you did not test at all, so the best opening
sequence is the one where no letter repeats across guesses — three words with
fifteen distinct letters eliminate more of the alphabet than three good guesses
chosen for feel.

`ww` generates those sets: pass the number of words you want, add `-u` to
require no repeated letters within a word as well as across them, and it prints
the set plus a coverage map of which letters you have spent. No dependencies,
which means it installs and runs faster than opening the puzzle.
