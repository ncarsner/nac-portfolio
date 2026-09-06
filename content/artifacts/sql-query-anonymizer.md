Title: sql-query-anonymizer
Slug: sql-query-anonymizer
Date: 2025-12-16
Category: package
Oneliner: Strip identifying names out of a SQL query, and put them back afterwards.
Release: v0.1.2
Year: 2025
Stack: Python, stdlib only, pytest
Topics: SQL, Privacy, Zero-dep
Metrics: Version=0.1.2, Downloads/mo=7, Deps=0, Tests=73
Links: PyPI=https://pypi.org/project/sql-query-anonymizer/, Code=https://github.com/ncarsner/sql-query-anonymizer
Stagelabel: Use it

```console
$ sql-anonymizer --help
```

## Notes

You need help with a slow query, and the query names your tables, your columns
and sometimes your customers. The usual options are to redact it by hand and
introduce errors, or to not ask. This replaces every identifier with a generic
placeholder while leaving the SQL structurally intact, so the query still reads
as the same query to anyone diagnosing it.

The part that makes it usable is the return trip. Mappings persist between
sessions, so an anonymised query that comes back with a fix can be
de-anonymised into something that runs against the real schema — a guaranteed
roundtrip rather than a one-way redaction. Seventy-three tests exist mostly to
defend that guarantee.
