# Current Sage & Seed Site Audit

Audit date: August 6, 2026. Public site inspected at `https://www.sageandseed.org/` through its HTML, compiled JavaScript/CSS, and public assets. The public experience is a single-page React site; `/admin` and `/admin/login` are application routes, not public content pages.

## Global identity and navigation

- **Visible structure:** fixed header with circular logo, “Sage And Seed” wordmark, and anchor navigation: About, How It Works, Offerings, Benefits, Research, News, Contact.
- **Visual language:** Merriweather headings, Inter body copy; deep blue (`#163172`), slate (`#2c3e50`), pale blue (`#D6E4F0`), peach (`#FFE5D9`), sage (`#C8D5B9`), and warm white (`#F6F6F6`). Rounded cards, soft shadows, blurred/color-washed backgrounds, gentle motion.
- **Retain:** recognizable logo, serif/sans pairing, navy/pastel palette, rounded imagery, friendly visual rhythm.
- **Expand/replace:** anchors become a clear multi-page information architecture; mobile menu, keyboard focus, reduced motion, print styles, and larger reading sizes are strengthened.

## Hero

- **Purpose:** establish mission and tone.
- **Visible text:** “Connecting Generations, Nurturing Minds,” “Where Wisdom Meets Wonder,” and a description of one-to-one video conversations.
- **Layout/image:** full-height dark photographic background; copy left, rounded portrait composition right. Uses `/hero-background.jpg` and `/hero-right.png`.
- **CTA:** existing bundle presents action buttons within the hero.
- **Retain:** headline, strongest imagery, emotional warmth, two-column silhouette.
- **Expand/replace:** outcome-heavy clinical wording is replaced with reciprocal, non-clinical language and clearer actions.

## What is Sage And Seed?

- **Purpose:** mission introduction.
- **Visible text:** begins “We’re more than a platform. We’re a movement to restore connection, purpose, and joy across generations.”
- **Layout:** centered heading and supporting copy with spacious card-based content.
- **Retain:** optimistic, movement-oriented spirit.
- **Expand/replace:** explain initiative origins, reciprocal value, and the distinction between conversation supports and games.

## How It Works

- **Purpose:** show the session flow.
- **Visible steps:** Personalized Match; Gentle Video Call (30–45 minutes); Choose Activities; AI-Assisted Support.
- **Layout:** four-step sequence.
- **Retain:** clear sequence and personalization.
- **Expand/replace:** use Prepare, Connect, Engage, Build Forward; avoid suggesting unvalidated real-time AI and emphasize human review.

## Offerings

- **Purpose:** preview conversation/activity supports.
- **Layout:** rounded cards with icons and short descriptions.
- **Retain:** scannable categories and approachable presentation.
- **Expand/replace:** build a filterable library with 12 detailed guides, simplification, redirection, personalization, and follow-up.

## Benefits

- **Purpose:** describe value across generations.
- **Layout:** paired benefits and visual cards.
- **Retain:** intergenerational framing.
- **Expand/replace:** explicitly make value mutual; remove unsupported health-outcome promises and avoid casting the young person as a caregiver.

## Research

- **Purpose:** lend evidence context.
- **Layout:** research/news card treatment.
- **Retain:** commitment to research-informed practice.
- **Expand/replace:** separate peer-reviewed research, organizational practice guidance, and Sage & Seed development; include sources and uncertainty.

## News

- **Purpose:** announce research and expansion updates.
- **Visible examples in bundle:** “New Research Confirms Impact” and “Sage And Seed Expands to 50 New Schools,” both dated in late 2025 with placeholder `#` links.
- **Retain:** space for genuine future updates.
- **Expand/replace:** omitted from launch because claims and links are not substantiated. Add only verified program news later.

## Contact and footer

- **Purpose:** invite participation and provide contact.
- **Visible details:** Explore links, email `rayan.ashish@icloud.com`, copyright, Privacy and Terms buttons.
- **Retain:** direct email and dark navy footer.
- **Expand/replace:** add audience-specific contact options, functional mailto form, real Privacy and Safeguarding pages, and educational-not-medical disclaimer.

## Responsive behavior

- Desktop navigation collapses to a mobile menu below the medium breakpoint; grids move from four/three columns to fewer columns.
- The rebuild retains this responsive logic, enlarges controls, simplifies small-screen layouts, includes visible focus, and honors reduced motion.

## Public page inventory

- `/` — single public landing page containing all sections above.
- `/admin` and `/admin/login` — administrative application routes, excluded from the public-site recreation.
- No other public editorial routes were present in the compiled route map at audit time.
