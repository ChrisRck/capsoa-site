# CAPSOA — future multilingual website

Approved French source: `src/fr/`. Translation catalogues: `translations/{fr,en,es,pt}.json`.
The root-level HTML files are the historical website; deploy **public/** generated below, not the repository root.

## Build and check

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node tests/language.test.cjs
```

Build fails if the French source text changes without updating the translation catalogue. Every paragraph, heading and list item is retained. The tests compare numeric terms, structure, language coverage and internal links. They are not a legal opinion or a substitute for legal validation.

## Preview

```sh
firebase hosting:channel:deploy langues-20261024 --expires 30d --project capsoa
```

Preview: https://capsoa-vitrine--langues-20261024-aa1grrn1.web.app/fr/

Each of the seven pages exists at `/fr/`, `/en/`, `/es/`, `/pt/` (home) and `/{language}/{document}`. Document slugs remain stable across languages. Legacy root URLs and `.html` URLs remain usable. Explicit language paths override browser and stored preferences. Language switching preserves the document and article fragment. Links work without JavaScript; preference detection is progressive enhancement.

The contact button opens `https://capsoa.web.app/contact?lang=xx`. The matching app change honours this on the contact entry point and does not silently change the user's profile language. Legal links from the app choose the current language at click time.

## Release status

As of 30 October 2026, the full homepage remains preview-only. Production uses
`firebase.waiting.json`: the unchanged FR/EN/ES/PT waiting homepages plus the six
approved legal documents in all four languages and their French root aliases.
The homepages do not link to these documents yet. Legal documents are public by
direct URL and carry both a robots meta tag and an X-Robots-Tag with
`noindex, follow`. Crawling must remain allowed so search engines can read this
instruction. This is not an access restriction.

```sh
python3 scripts/build_waiting.py
firebase deploy --only hosting --config firebase.waiting.json --project capsoa
```

The full-site build also retains noindex on legal documents for launch. The
production homepage content was compared byte-for-byte before this deployment;
hashes are recorded in `docs/waiting-homepage-hashes-2026-10-30.json`.
