Title: Teams Transcript Shortener
Slug: ms-teams-transcription-shortener
Date: 2026-08-08
Category: tool
Oneliner: Condense a Teams meeting transcript by merging each speaker's adjacent blocks.
Release: Unreleased
Year: 2026
Stack: Python 3.14, stdlib only, uv
Topics: Regex, CLI, Zero-dep
Metrics: Deps=0, Python=3.14
Links: Code=https://github.com/ncarsner/ms-teams-transcription-shortener
Stagelabel: Use it

```console
$ uv run slimchat samples/sample_transcript_1.txt

00:00:00.000 --> 00:00:49.610
Client RepA
Combined spoken text for that merged speaker block.
```

Write the condensed transcript out, and optionally an index of every speaker's
blocks:

```console
$ uv run slimchat transcript.txt --output condensed.txt --index-output speakers.json
```

## Notes

A Teams transcript is mostly repetition. One person talks for two minutes and
the export splits it into fifteen blocks, each re-stamping the speaker's name
and a new timestamp, because the segmentation follows pauses in speech rather
than turns in the conversation. Read as a document, it is unusable.

This merges sequential blocks from the same speaker, carries the timestamp from
the first start time to the last end time, and flattens multiline speech into
one block — so the output is still a transcript, just one where the structure
matches the conversation. It has no dependencies beyond the standard library,
which is what lets it run against a sensitive transcript without a review of
what else got installed alongside it.
