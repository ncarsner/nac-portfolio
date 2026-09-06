Title: pythodds
Slug: pythodds
Date: 2026-08-23
Category: package
Oneliner: Command-line statistics: distributions, hypothesis tests, regression and correlation.
Release: v0.24.0
Year: 2026
Stack: Python 3.13+, NumPy, SciPy
Topics: Statistics, CLI, Library
Metrics: Version=0.24.0, Downloads/mo=468, Deps=2
Links: PyPI=https://pypi.org/project/pythodds/, Code=https://github.com/ncarsner/pythodds
Stagelabel: Use it

```console
$ uv tool install pythodds
$ binom --n 20 --k 12 --p 0.5
```

## Notes

Seventeen statistical procedures, each as its own command and each also
importable as a library function: binomial, normal and Poisson distributions,
Bayes' theorem, z-scores, expected value and entropy, primality, streak
probability, Pearson and Spearman correlation, OLS regression with full
inference, sample-size and power analysis, bootstrap and parametric confidence
intervals, hypothesis tests and t-tests.

The design bet is that a statistic you need once belongs at a shell prompt, not
in a notebook you have to create first. Every command takes its inputs as flags
and prints a result, so it composes with the rest of a shell session — and the
same functions are importable when the one-off turns into something repeated.
It is the most developed thing here, at twenty-four releases.
