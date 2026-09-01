# Review brief: shipfourteen.com

You are reviewing a live one-page marketing site. Read this brief before
reporting anything. Its purpose is to stop you spending findings on decisions
that are deliberate and on defects that are already known.

- **Live site:** https://shipfourteen.com
- **This deployment serves the same build at `/`**, so you can inspect the real
  page rather than screenshots. Screenshots in `/review/` are for convenience
  only; the page itself is the source of truth.
- **Source:** one self-contained `index.html`, no build step, no framework.
  Vanilla three.js for the moon, pinned to r169 and self-hosted.

## What the business is

ShipFourteen sells one thing: a complete website, designed and built in
fourteen days, fixed scope and fixed price. It is run by one person, Matúš
Kališ. There is no team. Buyers are small and mid-sized businesses.

## Why this version exists

A previous version of this page claimed *"Every one of these is live, open any
of them"* about six portfolio entries, when only one is a paying client's live
site. That sentence was false and it was the reason for the rewrite. The whole
page is now built around claims a sceptical reader can check.

## Ground truth about the portfolio

This is the fact base. If any label on the page overstates any of this, that is
a real finding and the most important kind.

| Entry | Linked from the page | The real official site | Correct label |
|---|---|---|---|
| Sentinel VI Foundation | sentinel-vi.org | same | Client launch |
| VALORtech.AI | valortech-ai.vercel.app | www.valortech.ai (different, older) | Unlaunched redesign |
| Tharseo IT | tharseo-it.vercel.app | tharseoit.com (different) | Unlaunched redesign |
| SPPK | sppk-redesign.vercel.app | sppk.sk (different, live) | Unlaunched redesign |
| Petržalská posilka | petrzalska-posilka.vercel.app | none | Concept, built speculatively |
| matuskalis.com | matuskalis.com | same | Personal project |

There are **no testimonials and no measured results**, because none exist.
Nothing on the page may imply otherwise. Each unlaunched redesign deliberately
links the incumbent site it would replace, so the reader can compare.

## Deliberate decisions — do not report these as defects

1. **Only one client launch is shown, and the page says so in its own words.**
   Volunteering that up front is the strategy, not an oversight.
2. **No per-project build durations.** The owner offered a blanket "14 days",
   but stamping one number on a large content site and a one-page gym site
   would repeat the exact error this rewrite exists to fix. The column is
   omitted until real per-project numbers exist.
3. **"From 300 EUR" sits in the Investment section, not the hero.** Publishing
   a floor price was the owner's explicit decision, taken against advice that
   it undercuts the positioning. Do not re-litigate whether to show a price;
   you may comment on how it is framed.
4. **The moon canvas is decorative**: `aria-hidden="true"`, no `tabindex`, not
   a tab stop. Its click interaction was removed, so a focus stop with no
   payoff would only waste a keyboard user's time.
5. **The page is long** — 10 199 px on desktop, 13 304 px on a phone. Eleven
   sections was the agreed scope. Comment on whether the middle earns its
   scroll, but length alone is not a bug.
6. **three.js is ~263 KB gzipped for a single lit sphere.** Known trade. It is
   loaded inside `requestIdleCallback` so it stays out of the first paint. A
   hand-rolled shader is filed as a follow-up, not an oversight.
7. **Michroma is used only on the wordmark.** Anywhere else is a regression.
8. **Radius is 2–3 px and there are no gradients or pill buttons.** This is a
   deliberate reversal of the previous design, not an unfinished state.

## Known open items — already logged, no need to report

- The booking CTA points at `cal.com/matuskalis/scoping-call`. The event is now
  titled *Website build — Scoping Call*, but its **description still mentions
  picking an AI feature**, left over from a previous offer. The owner has to
  fix that in Cal.com; it is not in this codebase.
- The footer email is a personal Gmail rather than a domain address.
- No per-project build durations, as above.

## Verification already performed — do not spend effort repeating

Run against production after deploy, walking the full page height at every
width rather than measuring only at scroll top:

| Check | Result |
|---|---|
| Horizontal overflow at 320 / 390 / 768 / 1440 | 0 px at every scroll position |
| Interactive elements under 40 px tall | 0 |
| Broken images | 0 |
| Console errors | 0 |
| Every outbound link | all 200 |
| Keyboard tab order | every stop has a visible 2 px focus ring |
| Canvas in tab order | no, by design |
| `prefers-reduced-motion` | schedule curve fully drawn, orbit animation off |
| Slovak diacritics (`ž č ť ľ š ú`) | resolve in Inter, not a fallback font |

## What is actually worth your attention

1. **Does any claim on the page overstate the ground truth above?** Read every
   sentence in the build log, the founder section and the FAQ against the table.
   This is the highest-value thing you can find.
2. **Does the honesty read as confidence or as apology?** The page leads with
   its weakest fact. Judge whether that lands as credible or as self-defeating,
   and quote the specific sentences that decide it.
3. **Is the fourteen-day promise consistent everywhere?** The schedule says the
   clock starts after the scoping call. Check nothing elsewhere contradicts
   that, including the manifest and the FAQ.
4. **Would a sceptical buyer's next question go unanswered?** Name the question
   and where it should have been answered.
5. **Correctness bugs** in the CSS or the three.js module that the checks above
   would not catch.

Report findings with a file and line where the defect is in code, or the exact
on-page sentence where it is in copy. A clean review with no findings is a
valid outcome.
