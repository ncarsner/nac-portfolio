Title: Math & Finance Tools
Slug: math-and-finance-tools
Date: 2026-09-06
Category: app
Oneliner: Debt payoff and blended-rate calculators, side by side, in the browser.
Release: v0.1.0
Year: 2026
Stack: Python, Streamlit, Plotly, uv
Topics: Finance, Calculators, Streamlit
Metrics: Calculators=2, Python=3.14, Tests=yes
Links: Code=https://github.com/ncarsner/math-and-finance-tools
Embed: https://math-and-finance-tools.streamlit.app/?embed=true
Stagelabel: Running now

## Notes

Two calculators that answer questions a spreadsheet answers badly. The **Debt
Payoff Calculator** runs Snowball and Avalanche against the same set of loans
and shows them side by side — any number of accounts, each with its own APR,
minimum payment, compounding mode and optional intro rate, resolved into a
month-by-month schedule with total interest and a remaining-balance chart per
strategy. The comparison is the point: the two strategies disagree about which
debt to attack, and the disagreement is only legible when both are on screen.

The **Composite Rate Calculator** answers the prior question — what is the
blended rate across everything you owe. Accounts above the composite are the
ones worth attacking; accounts at or below it are comparatively cheap money.
A scatter plot splits them on that line, which turns "where do I start" from a
judgement call into something you can read off an axis.
