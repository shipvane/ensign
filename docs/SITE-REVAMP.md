# Landing page — full revamp plan

Written 2026-08-08, after the medium-effort pass that added the Fleet section,
removed the redundant `#products` section, and gave the TideLog proof its own
beat. This is the *next* pass — a narrative rework, not a tidy-up. Nothing here
is started.

## Where the page stands now

Seven sections before the footer:

| # | id | Beat |
|---|---|---|
| 1 | *(hero)* | Ship your code, just point the way |
| 2 | `why` | Your code, your cloud, your call — black-box SaaS vs Shipvane |
| 3 | `how` | The ADLC — an eight-step grid of the whole lifecycle |
| 4 | `fleet` | One ship, every station crewed — labelled diagram + six cards |
| 5 | `proof` | Watch it build a real app — TideLog, four-step evidence, real PR |
| 6 | `clients` | One Engine, many front doors |
| 7 | `waitlist` | Be first aboard |

The medium pass fixed the duplication (`#products` restated what `#fleet`
covers) and promoted proof from a footnote to a section. What's left is
structural.

## What a full revamp should address

**1. The page has no picture of the product.** The Fleet diagram shows the
*architecture*; nothing shows the *experience*. A visitor never sees a terminal
running `shipvane connect`, a PR Engine opened, or the Bridge dashboard. For a
developer tool that's the single biggest gap — most buyers decide on "what does
using it look like". Blocked on Connect and Bridge being demoable; TideLog going
live at demo.shipvane.com unblocks part of it.

**2. The ADLC step-grid is doing too much work.** Eight equally-weighted cards
is a lot of reading for what is really one loop with a gate in it. A single
animated or annotated diagram — ticket in, loop, green gate, PR out — would land
faster and pairs naturally with the Fleet diagram's visual language.

**3. Two sections argue the same point.** `why` (black-box vs owned) and the
safety-contract band (nothing ships off-course) are both trust arguments.
They're separated by four sections, so it doesn't read as repetition today, but
in a rework they should probably merge into one strong trust beat.

**4. Nothing is dated or versioned.** "In development" has no timeline. A
roadmap strip — even coarse, like "Engine private beta → Connect → Bridge" —
would convert better than six identical status chips, and gives repeat visitors
a reason to come back.

**5. The waitlist is the only conversion.** No docs, no GitHub-star ask, no
newsletter. Once Engine is installable the CTA hierarchy needs rethinking.

## Sequencing when it happens

Do it in this order, because each step unblocks the next:

1. Get TideLog live at demo.shipvane.com (blocked on the App Runner GitHub
   handshake — connection `shipvane-github` is `PENDING_HANDSHAKE`).
2. Capture real product visuals: TideLog running, a PR Engine opened, a Bridge
   screenshot once it's past scaffold.
3. Mock the new narrative before touching `index.html` — this is a design pass
   and the current page is good enough that a half-finished rework is worse.
4. Rebuild, keeping the hero. It works; nothing in this plan argues otherwise.

## Constraints to preserve

- **Light-only.** The page has no dark mode; don't half-introduce one.
- **Single file, inline CSS/SVG.** No build step, no dependencies — GitHub Pages
  serves `site/` directly. Keep it that way unless there's a real reason.
- **Honest status.** Helm is marked *Planned* and Ensign *Not a product* on
  purpose. The pitch is "no black box, proven not just generated" — implying a
  component exists that doesn't would undercut it.
- **Verify claims before publishing.** TideLog's PRs are open, not merged; the
  copy says "pull requests" for that reason. Check before strengthening it.
