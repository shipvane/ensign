<p align="center">
  <img src="brand/lockup-horizontal.png" alt="Shipvane — Ship your code, just point the way." width="440" />
</p>

<p align="center"><em>Your code, your cloud, your call.</em></p>

Shipvane runs autonomous coding agents inside **your own cloud** — not a black box.
You point it at a ticket; it works in a real checkout, proves the change against a
**real CI build** (it's not done until the build is green), and lands a merge-ready
PR for **your approval**. Your code never leaves your environment, and nothing
merges without your say.

> 🚧 **Early development.** This repository reserves the `shipvane` name across
> npm, PyPI, and GitHub while the product is built. Docs and the CLI are coming
> soon — https://shipvane.com

## Why Shipvane

Black-box SaaS coding agents run your codebase in someone else's opaque
environment and hand back code they can't truly verify. Shipvane is the opposite:

- **Your cloud, not a black box.** The agent runtime deploys into your own AWS
  account, so you own the environment, the logs, and the keys. (AWS today; more
  to come.)
- **Proven, not just generated.** Every change runs your real build and tests and
  iterates until the gate is green.
- **You hold the final say.** Code only moves forward with your approval — runs
  are ephemeral and scoped per ticket.

## The fleet

Every part is named for the job it actually does on a ship — learn the vessel
and you've learned the product.

| | Role | Status |
|---|---|---|
| **Engine** | Drives the work — the agentic runtime, deployed into your own cloud | In development |
| **Connect** | Gets you aboard — the tender: a CLI that carries your orders out to the Engine | In development |
| **Bridge** | Sees everything — run history, live logs, and run controls from browser or phone | In development |
| **Capstan** | Hauls the backlog — the autonomous loop, one reviewable PR at a time | In development |
| **Helm** | Sets the course — the dispatcher: what runs, in what order, under what spend cap | Planned, not yet built |
| **Ensign** | Flies the flag — **this repo**: shipvane.com plus the brand and social assets | — |

**[TideLog](https://github.com/shipvane/tidelog)** isn't part of the fleet. It's
a real app — a harbor operations logbook — that we build entirely with Shipvane,
in the open, so anyone can read the pull requests Engine wrote.

Engine speaks the **Model Context Protocol** and signs in over **OAuth**, so the
Connect CLI is just one way in — you can also drive it straight from the AI
client you already use. Working today in **Claude Code**, **Claude Desktop**, and
**Claude mobile**; ChatGPT and other MCP clients coming.

## Where to find it
- **Web:** https://shipvane.com
- **npm:** `npm i shipvane` *(reserved)*
- **PyPI:** `pip install shipvane` *(reserved)*

---

© Shipvane. Name-reservation placeholder — not the licensed product.
