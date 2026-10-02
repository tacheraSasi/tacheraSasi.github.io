---
title: "I Want to Understand Computers, Not Just Use Them"
date: 2026-10-02
summary: "After years of building abstractions, I want to understand the machine underneath them: the processes, memory, networking, and failure modes that frameworks hide."
draft: false
medium: "https://medium.com/@tacherasasi/i-want-to-understand-computers-not-just-use-them-b94385de2ffb?source=rss-9a41d7ec29fb------2"
tags: ["tachera", "software-engineering", "systems-programming"]
---

![](https://cdn-images-1.medium.com/max/1024/1*Z-4jE3q_hWwAJq4NPpkbrw.png)

I’ve spent a lot of time writing software.

Web applications. Mobile apps. APIs. Backends. Databases. Deployment systems. Developer tools. And lately, more and more infrastructure and very, very low-level stuff, mostly in Zig.

And honestly, I’m starting to suspect that I have a problem.

At some point, I realized something had changed.

I don’t just want to build software anymore.

I want to understand the computer underneath it.

I want to know what happens when a process starts, how memory actually gets used, why a network connection fails, what the operating system is doing, how filesystems work, what happens when a server runs out of resources, and why a distributed system behaves differently from the beautiful little diagram I drew on a whiteboard.

The diagram, of course, assumes everything works.

The real system apparently did not receive the memo.

I want to understand the machine, not just the framework sitting on top of it.

### The abstraction is useful until it isn’t

Modern software development is incredibly good at hiding complexity.

That’s one of its greatest strengths.

I can create an HTTP server without thinking about TCP. I can use a database without thinking about disk pages. I can deploy an application without manually configuring a server. I can create a mobile interface without thinking about how pixels eventually reach a display.

That’s great.

Abstraction exists for a reason.

I don’t want to manually implement TCP every time I build a todo app. That sounds like a terrible Tuesday.

But there is a point where abstraction becomes a ceiling.

You can spend years knowing React, Laravel, Next.js, Docker, Kubernetes, or whatever the industry is excited about this month without understanding much about what actually happens underneath them.

And then something breaks.

A connection starts timing out.

A process consumes all the memory.

A deployment works on one machine but not another.

A filesystem fills up.

A request occasionally takes five seconds instead of fifty milliseconds.

A queue gets backed up.

Your logs say absolutely nothing useful.

You stare at the terminal.

The terminal stares back.

Suddenly the abstraction isn’t enough anymore.

You have to go one layer deeper.

And I want to be comfortable there.

### I started caring about the layers underneath

This is probably why I’ve become increasingly interested in Go, Zig, Rust, Linux, networking, distributed systems, infrastructure, and developer tooling.

They force me to think differently.

When I’m building something in Go, I find myself thinking about processes, concurrency, memory, networking, files, system calls, binaries, and failure modes.

When I’m writing Zig, I have considerably fewer layers between me and the machine.

Sometimes that’s beautiful.

Sometimes it feels like the computer has finally decided to stop protecting me from my own decisions.

Either way, I’m learning.

When I’m working with Linux, I can’t pretend the operating system doesn’t exist.

When I’m building infrastructure, I have to think about what happens when something goes wrong.

And that’s exactly what I want.

I don’t want software to feel like magic.

I want to understand the magic trick.

Preferably before production catches fire.

### This is also why I build things from scratch

I’ve always had a tendency to build things I probably could have just downloaded.

Sometimes that’s objectively inefficient.

If I need file storage, there are dozens of existing products.

If I need deployment infrastructure, there are already massive platforms.

If I need a programming language, there are hundreds of them.

And yet I keep building.

VintLang started because I wanted to understand what it actually means to build a programming language.

BeamDrop exists because I wanted to build a self-hosted storage system.

Ekilie exists because I wanted to understand the infrastructure behind deploying and managing software.

At this point, I should probably learn to leave perfectly good software alone.

But there is something different about building a thing yourself.

You don’t just read about the problem.

You run directly into it.

You discover why the boring decisions matter.

You discover where systems become complicated.

You discover what breaks.

You discover that your beautiful architecture diagram did not account for the disk being full.

And, most importantly, you develop an intuition that you can’t get from reading API documentation alone.

I don’t necessarily expect every project to become a massive company.

Sometimes the project itself is the education.

Sometimes you spend three days building something that already exists because you wanted to know how it works.

That’s not always good engineering.

But it’s excellent curiosity.

### I don’t want to memorize more APIs

There is a strange trap in software engineering where becoming more experienced can sometimes mean becoming better at remembering abstractions.

You learn another framework.

Another library.

Another cloud service.

Another ORM.

Another deployment platform.

Another programming language.

Another JavaScript build tool whose name you will forget in approximately six months.

And suddenly your definition of progress becomes:

> *How many technologies do I know?*

I’m becoming less interested in that question.

I’d rather ask:

> *How much of the system do I actually understand?*

If I know five frameworks but don’t understand networking, that’s a problem.

If I know three cloud platforms but can’t explain what happens when a Linux process runs out of memory, that’s a problem.

If I can deploy a Kubernetes cluster but don’t understand why I needed one in the first place, that’s a particularly interesting problem.

Tools are useful.

Understanding is more valuable.

### The deeper I go, the more interesting software becomes

The funny thing is that learning the lower layers hasn’t made higher-level development less interesting.

It has made it more interesting.

When I write an API now, I think differently about it.

When I deploy an application, I think about the machine running it.

When I write concurrent code, I think about what the runtime and operating system are actually doing.

When I design a system, I think more about failure instead of just the happy path.

The layers aren’t separate.

They’re connected.

A web request eventually becomes bytes.

Those bytes travel through networks.

Processes consume resources.

Data ends up somewhere on storage.

The operating system manages all of it.

And underneath all of that is hardware executing instructions.

Which is slightly insane when you think about it.

You can write:

fetch("/users")

and somehow that eventually involves electricity moving around inside a machine, packets travelling through networks, operating systems scheduling work, and hardware executing instructions.

And I used to think the interesting part was the React component.

The React component is still pretty cool, though.

### I’m not trying to become a “10x engineer”

I’ve never been particularly interested in that idea.

I don’t want to optimize myself into a machine that produces pull requests.

I want to become the kind of engineer who can sit in front of an unfamiliar system and eventually figure it out.

Give me a strange codebase.

Give me a broken server.

Give me an unfamiliar protocol.

Give me a performance problem.

Give me a system with terrible documentation.

I want my first reaction to be curiosity instead of panic.

Although some panic is probably acceptable.

That’s the skill I’m actually chasing.

Not knowing everything.

Knowing how to find out.

### Maybe that’s what engineering really is

The older I get as a developer, the less impressive syntax feels.

Writing code is important, but code is only one part of the job.

The interesting part is understanding why the system behaves the way it does.

Understanding constraints.

Understanding trade-offs.

Understanding failure.

Understanding the environment your software lives in.

And understanding enough of the underlying machine that you aren’t completely helpless when an abstraction breaks.

That’s where I want to go.

I still love building web applications.

I still enjoy React.

I still write APIs.

I still use frameworks.

I’m not abandoning abstraction.

I’m just becoming more interested in what exists underneath it.

Because eventually, I don’t want to just be someone who knows how to use computers.

I want to be someone who understands them.

Even if that means occasionally spending six hours debugging something that turns out to be a typo.

And I think that’s a much more interesting journey.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=b94385de2ffb)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/i-want-to-understand-computers-not-just-use-them-b94385de2ffb?source=rss-9a41d7ec29fb------2).*
