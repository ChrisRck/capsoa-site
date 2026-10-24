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

**Preview only as of 24 October 2026.** The existing capsoa.fr waiting page has not been replaced. The app integration is saved and built but not released to the live web app or a native build in this change. Deploy the translated website documents before releasing app links to `capsoa.fr/{language}/…`.

See `docs/review-2026-10-24.md` for unresolved inconsistencies already present in the French legal source before launch. Do not treat the translation as validation of those statements.
