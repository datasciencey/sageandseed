# Sage & Seed

Static, accessible resource website for meaningful one-to-one intergenerational engagement.

## View locally

From this folder run `python3 -m http.server 8000`, then open `http://localhost:8000`.

## GitHub Pages

Push this folder to a GitHub repository. In **Settings → Pages**, choose **Deploy from a branch**, then select the main branch and `/ (root)`. All links are relative, so the site works in a repository subdirectory.

## Structure

- Root HTML files: primary site pages
- `guides/`: practical conversation guides
- `activities/`: detailed activity guides
- `assets/css/site.css`: shared design system
- `assets/js/site.js`: navigation and activity filtering
- `assets/images/`: locally stored site imagery
- `assets/downloads/`: print-ready HTML resources (use the browser's Print → Save as PDF)

No build step or external JavaScript dependency is required.
