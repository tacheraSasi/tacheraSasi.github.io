---
title: "BeamDrop, Self-Hosted File Sharing in Go"
slug: "beamdrop"
date: 2026-02-20
draft: false
author: "Tachera W Sasi"
description: "BeamDrop is a self-hosted file sharing server in Go: single binary, embedded React UI, S3-compatible API, shareable links, Prometheus metrics and Docker support."
keywords: ["beamdrop", "self-hosted file sharing", "go file server", "s3 compatible api", "open source dropbox alternative"]
images: ["/images/beamdrop.png"]
subtitle: "Single-binary file sharing with an S3-compatible API, shareable links and real-time stats."
stack: ["Go", "React", "SQLite", "Docker"]
liveUrl: "https://github.com/ekilie/beamdrop"
repoUrl: "https://github.com/ekilie/beamdrop"
image: "/images/beamdrop.png"
---

BeamDrop started with a simple problem: sharing files between my own devices without handing them to a cloud provider. One afternoon project later, it had become a full-stack system: a Go HTTP server, an embedded React frontend, SQLite storage, JWT auth, WebSockets and an S3-compatible API, all shipping as a single binary. I wrote up how that happened in [I Think I Accidentally Built a Full-Stack Framework](/posts/i-think-i-accidentally-built-a-full-stack-framework/).

## What it does

- Upload, download, move, copy, rename and search files from a fast web UI
- Password protection plus shareable links with expiry
- S3-compatible API (buckets, objects, presigned URLs) so CI/CD and scripts can talk to it
- Real-time stats over WebSockets and Prometheus metrics for observability
- QR code in the terminal so your phone connects in seconds

## Why it is built this way

No web framework: just Go's `net/http` and `ServeMux`. No CGO: a pure-Go SQLite driver keeps cross-compilation (`GOOS`/`GOARCH`) trivial. No sidecars: the React build is baked into the binary with `embed.FS`, so deployment is one file. These are the same boring-reliability choices behind [ekilie.cloud](/projects/ekilie-cloud/).

## Run it

```bash
beamdrop -dir ~/Documents -p secretpassword
```

BeamDrop is open source at [github.com/ekilie/beamdrop](https://github.com/ekilie/beamdrop) and there is a mobile client ([BeamDrop Mobile](https://github.com/tachRoutine/beamdrop-react-native.git)) plus a SaaS control plane in the same repo.
