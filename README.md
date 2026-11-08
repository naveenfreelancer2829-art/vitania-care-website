# Vitania Care Website (final)

## Live site
https://naveenfreelancer2829-art.github.io/vitania-care-website/

Repository: https://github.com/naveenfreelancer2829-art/vitania-care-website
(branches `main` and `gh-pages` hold the same final version)

If the live link shows "404 There isn't a GitHub Pages site here", switch Pages on once:
Repository → Settings → Pages → Build and deployment → Source: "Deploy from a branch" →
Branch: `main`, folder `/ (root)` → Save. The site goes live within 1–2 minutes.

## Contents
- The repository root is the complete live site. Upload these files to any web host.
- `builder_source/`: `build.py` generates every page; `styles.css` and `site.js` are the shared style and script.

## Editing
Copy the three files in `builder_source/` into the repository root, edit `build.py`, and run `python3 build.py`.
All pages, the sitemap and the search data are regenerated.

## Phone number
Set near the top of `build.py`:

    PHONE, PHONE_TEL = "+91 91806 06295", "+919180606295"

It appears in the top bar, page headers, contact sections, footer and search data.

## Enquiry form
Enquiries go to prateeksha@vitaniacare.com, copied to chairman@vitaniacare.com, via FormSubmit.co.
The first submission sends a one-time activation email to prateeksha@vitaniacare.com that must be confirmed.

## Custom domain (www.vitaniacare.com)
Settings → Pages → Custom domain, then change `SITE` at the top of `build.py` to the new address and rebuild.
