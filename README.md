# Sage & Seed

Static, accessible resource website for meaningful one-to-one intergenerational engagement.

## View locally

From this folder run `python3 -m http.server 8000`, then open `http://localhost:8000`.

## GitHub Pages

Push this folder to a GitHub repository. In **Settings → Pages**, choose **Deploy from a branch**, then select the main branch and `/ (root)`. All links are relative, so the site works in a repository subdirectory.

The production custom domain is `sageandseed.org`, configured by the root `CNAME` file. The domain DNS must point to GitHub Pages before enabling **Enforce HTTPS**.

## Structure

- Root HTML files: primary site pages
- `guides/`: practical conversation guides
- `activities/`: detailed activity guides
- `assets/css/site.css`: shared design system
- `assets/js/site.js`: navigation and activity filtering
- `assets/images/`: locally stored site imagery
- `assets/downloads/`: print-ready HTML resources (use the browser's Print → Save as PDF)

No build step or external JavaScript dependency is required.

## Multilingual resource release

`guides.html` is the central English resource hub and includes a two-group language chooser. It links to `guides-more-languages.html`, which contains complete Spanish, Mandarin, Hindi, Kannada, Marathi, and Bengali collections. Every language has four training modes: starter guides, 15 situation topics, 12 activity topics, and two pocket cards. Forty-two principal PDFs are stored under `assets/downloads/`.

The source reviews are summarized in `EVIDENCE_NOTES.md`. `GUIDE_CONTENT_MAP.md` maps every resource and language.

To regenerate the web resource pages, run `node tools/build_resources.mjs` with a current Node release. To regenerate PDFs, run `/opt/anaconda3/bin/python tools/build_pdfs.py` in the authoring environment.
