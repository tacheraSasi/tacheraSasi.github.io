---
title: "VintLang — A Programming Language Built in Go"
slug: "vintlang"
date: 2025-06-01
draft: false
author: "Tachera W Sasi"
description: "VintLang is a programming language built in Go: interpreter, standard library, packaging with movebin, docs and a growing community ecosystem."
keywords: ["vintlang", "programming language go", "interpreter in go", "new programming language"]
images: ["/images/vintlang-dark.png"]
subtitle: "A practical language for scripting and learning, with an interpreter written from scratch in Go."
stack: ["Go", "Vint"]
liveUrl: "https://vintlang.ekilie.com"
repoUrl: "https://github.com/tacheraSasi"
image: "/images/vintlang-dark.png"
---

VintLang is a programming language I designed and implemented in Go: lexer, parser, tree-walking interpreter, standard library and tooling. It is the project that taught me the most about computers, which is a journey I wrote about in [I Want to Understand Computers, Not Just Use Them](/posts/i-want-to-understand-computers-not-just-use-them-b94385de2ffb/).

## What it includes

- Full interpreter pipeline: lexing, parsing, evaluation
- Standard library for everyday scripting tasks
- [movebin](https://github.com/vintlang/movebin-vint.git): install Vint binaries globally from the CLI
- Live playground and docs at [vintlang.ekilie.com](https://vintlang.ekilie.com)
- Vint is one of the languages [ekilie.cloud](/projects/ekilie-cloud/) runs

## Why build a language

Writing an interpreter forces you through every layer: memory layout, scoping, error handling, performance trade-offs. Lessons from VintLang feed directly into my backend work, including [GooferORM](/projects/gooferorm/) and [BeamDrop](/projects/beamdrop/).

VintLang is open source under the [vintlang](https://github.com/vintlang/movebin-vint.git) organization. Try the playground, read the docs, and file issues: language design is a conversation.
