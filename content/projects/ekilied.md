---
title: "ekilied, Platform Agent Daemon for Ekilie Cloud"
slug: "ekilied"
date: 2026-01-15
draft: false
author: "Tachera W Sasi"
description: "ekilied is the lightweight Go agent that runs on your VPS for Ekilie Cloud: manages sites, deployments, SSL certificates and services."
keywords: ["ekilied", "vps agent", "deployment agent go", "ekilie cloud"]
images: ["/images/go-2.png"]
subtitle: "A tiny Go binary on your VPS that manages sites, deployments, SSL and services."
stack: ["Go"]
liveUrl: "https://github.com/ekilie/ekilied"
repoUrl: "https://github.com/ekilie/ekilied"
image: "/images/go-2.png"
---

ekilied is the on-box half of [Ekilie Cloud](/projects/ekilie-cloud/): a lightweight Go daemon that runs on your VPS and converges it toward the control plane's desired state. Small binary, no runtime dependencies, boring and reliable on purpose.

## What it does

- Provisions and supervises sites and services on the machine
- Issues and renews SSL certificates automatically
- Applies deployments: pull, build, restart, health-check
- Reports status and logs back to the control plane

It pairs with the [Ekilie Cloud](/projects/ekilie-cloud/) control plane and shares design DNA with [BeamDrop](/projects/beamdrop/): single static binary, standard-library HTTP, observable by default.

Open source at [github.com/ekilie/ekilied](https://github.com/ekilie/ekilied).
