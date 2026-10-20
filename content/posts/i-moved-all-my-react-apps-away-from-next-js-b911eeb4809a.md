---
title: "I Moved All My React Apps Away From Next.js"
date: 2026-10-19
lastmod: 2026-10-19
draft: false
author: "Tachera W Sasi"
description: "Next.js was my favorite framework for two years. Then one awkward question ended it: what was I actually using it for? The answer: mostly just routing."
summary: "Next.js was my favorite framework for two years. Then one awkward question ended it: what was I actually using it for? The answer: mostly just routing."
tags: ["react", "nextjs", "tanstack-router", "vite"]
categories: ["Web Development"]
keywords: ["next.js alternative", "react without next.js", "tanstack router vs next.js", "vite react spa routing"]
images: ["https://cdn-images-1.medium.com/max/1200/1*weStifDcGA1TP8qTCCpA6g.png"]
medium: "https://medium.com/@tacherasasi/i-moved-all-my-react-apps-away-from-next-js-b911eeb4809a?source=rss-9a41d7ec29fb------2"
---

![A React app architecture split between a plain Vite frontend and an independent backend](https://cdn-images-1.medium.com/max/1024/1*weStifDcGA1TP8qTCCpA6g.png)

For a while, Next.js was *the* framework for me.

I started using it seriously toward the end of 2023. By 2024, I was deep into it. Almost every project I started was going to use Next.js, and if you asked me what framework to use for a React application, you probably already knew my answer.

I really liked the App Router. I liked the file-based routing. I liked how everything fit together. Next.js was popular, the ecosystem was growing, and I was having a good time building with it.

Then, somewhere after a year and a half of using it, I asked myself a question that made the whole thing a little awkward:

**What am I actually using Next.js for?**

The answer was mostly routing.

And that was the beginning of the end.

### I was using a whole framework for one feature

Let me be clear. I wasn’t struggling with Next.js. I wasn’t rage-quitting because of some mysterious hydration error at 2 AM. I genuinely enjoyed using it.

But when I looked at the applications I was building, I noticed a pattern.

Most of them had a React frontend and a separate backend. Sometimes the backend was written in Go. Sometimes NestJS. Sometimes something else entirely. I wanted my backend to be its own application, with its own architecture, deployment, and responsibilities.

I wasn’t trying to build everything inside Next.js.

I was building a frontend that talked to an API.

And yet I was bringing in a framework with a whole collection of server-side features, rendering strategies, conventions, and abstractions when I wasn’t using much of them.

Did I use SSR sometimes? Yes. But it wasn’t central to most of my applications.

What I consistently wanted was much simpler:

  * React for building the UI.
  * File-based routing so my routes were easy to organize.
  * A production build I could deploy as static assets.
  * A clean way to communicate with my backend.

That was pretty much the list.

I had been choosing the entire restaurant because I liked one item on the menu.

### Enter TanStack Router

Around the middle of 2025, I started experimenting with TanStack Router.

My first serious use of it was [BeamDrop](https://github.com/ekilie/beamdrop), my self-hosted file storage project built around Go and React.

The frontend lives in [static/frontend](https://github.com/ekilie/beamdrop/tree/main/static/frontend). That is the actual project setup, rather than some imaginary example I made for this blog.

I wanted a frontend that could stay focused on the UI while the Go backend handled the application logic. TanStack Router gave me the routing experience I liked from Next.js without requiring me to adopt its entire application model.

The part that immediately clicked was file-based routing.

I could keep my routes organized as files, work with nested routes, and get type-safe navigation. The router plugin could generate the route tree, and automatic code splitting was available when I wanted it.

All of this worked with React and Vite.

The setup felt familiar, but there was less framework between me and the application I was building.

And I liked that a lot.

### I wanted the routing, not the whole universe haha.

Here is a simplified example of the kind of route I wanted to write:

```ts
// src/routes/files.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/files')({
  component: FilesPage,
})
function FilesPage() {
  return <h1>My files</h1>
}
```

The file represents a route. The route renders a React component. Type information flows through the router, and I don’t have to maintain a massive collection of handwritten route definitions.

For file-based routing, the Vite plugin handles generating the route tree:

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { tanstackRouter } from '@tanstack/router-plugin/vite'

export default defineConfig({
  plugins: [
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }),
    react(),
  ],
})
```

This is a minimal illustration of the setup, not a copy of BeamDrop’s complete configuration. The important part is that I get file-based routing and optional automatic code splitting without adopting a full-stack framework.

TanStack Router also supports code-based routing, but file-based routing was the feature that initially attracted me. Its [official routing documentation](https://tanstack.com/router/latest/docs/routing/file-based-routing) explains the approach in more detail.

I wasn’t giving up structure. I was choosing a smaller set of tools to provide it.

### Static builds are a feature, not a compromise

One of my favorite parts of this setup is being able to build the frontend into static assets.

For applications like BeamDrop, I don’t need the frontend to run a server-side React rendering process every time someone opens a page. I need the browser to load the application, display the interface, and communicate with the backend.

Vite produces a build that can be served as ordinary HTML, CSS, and JavaScript files. Those assets can sit behind Nginx, a CDN, object storage, or whatever deployment arrangement makes sense for the project.

My Go backend remains responsible for the actual application logic.

That separation is useful to me. The frontend can be deployed independently, and I don’t have to run a Next.js server just to deliver a client-side application.

There’s also less infrastructure to think about. I can build the frontend, serve the resulting files, and let the backend do its job.

**A frontend doesn’t automatically need a frontend server. Sometimes it just needs to be a folder of files.**

Of course, a static build doesn’t mean the entire application is static. BeamDrop still needs its backend for things like authentication, file operations, and API requests. Static delivery simply means the frontend itself doesn’t need a runtime server to render its pages.

### Then I stopped using Next.js altogether

After using TanStack Router on BeamDrop, I liked the experience enough that I started using the same approach on my other projects.

Eventually, I stopped reaching for Next.js.

Not for a week. Not for a small experiment. I haven’t used it for a project since I made that switch.

Haha.

I found that plain React, Vite, and TanStack Router covered what I actually needed. I could organize routes the way I wanted, keep the frontend separate from the backend, and deploy static builds without dragging along a server runtime that my applications didn’t require.

My frontend development felt lighter. My applications felt responsive, and I spent less time thinking about framework-specific behavior and more time building the product.

I haven’t conducted a controlled benchmark across all my projects, so I’m not going to claim that TanStack Router magically makes every application faster or uses a fixed percentage less RAM. That’s not the point.

The point is that **the simpler setup fits my applications better**, and the performance and resource usage I’ve observed have reinforced that choice.

### Apparently, other people have been asking the same question

I thought this was mostly a personal preference until I came across other teams making similar decisions.

In April 2026, Railway published [a detailed account of moving its production frontend off Next.js](https://blog.railway.com/p/moving-railways-frontend-off-nextjs). Its dashboard, canvas, and website moved to Vite and TanStack Router.

Their reasons weren’t identical to mine. Railway had a much larger application, build times exceeding ten minutes, and a frontend dominated by client-side interactions and real-time features. They wanted a faster development loop and a framework that better matched the architecture of their product.

They reported that builds that had taken more than ten minutes were finishing in under two minutes after the migration.

That doesn’t mean every Next.js project has slow builds. It means Railway’s team found that the costs of their particular setup had stopped making sense.

[Appwrite also discussed the growing interest in TanStack Start](https://appwrite.io/blog/post/why-developers-leaving-nextjs-tanstack-start), including the desire for a lighter, more explicit development experience.

These are different projects with different requirements, and Railway’s migration to TanStack Router should not be confused with Appwrite’s discussion of TanStack Start. But the broader question is familiar: are we choosing a framework because its features solve our problems, or because it has become the default answer?

I don’t think Next.js is suddenly bad. I think developers are getting more comfortable questioning whether they need everything it provides.

I know I did.

### I don’t hate Next.js

I want to make this distinction because framework discussions can become unnecessarily religious.

Next.js is a good framework. It has a large ecosystem, strong rendering capabilities, and useful conventions. If I’m building a content-heavy website that benefits from server rendering, or an application where I genuinely want React rendering and backend-for-frontend logic in one framework, Next.js can make a lot of sense.

It also supports static exports, so even the idea that Next.js always requires a runtime server would be wrong. The framework offers more than one deployment model.

But that doesn’t mean I need to choose it for every React application.

My backend is often a separate service. My frontend is often a client-side application. My data comes from APIs, and I want to control how those APIs are designed and deployed.

I don’t need to put my Go backend inside a React framework just because the framework can handle server-side work.

And I don’t need to use a full-stack framework just because I want file-based routing.

Those are two separate decisions.

For my projects, I prefer to make them separately.

### My stack is boring now, and I like it

These days, the frontend stack I reach for is straightforward:

  * **React** for the UI.
  * **Vite** for development and production builds.
  * **TanStack Router** for routing, navigation, and type safety.
  * **TanStack Query**, when I need dedicated server-state and data-fetching management.
  * **Go, NestJS, or whatever backend fits the project.**

Not every project needs every item on that list. That’s the point.

I can add tools when I need them instead of adopting a larger framework first and figuring out how much of it I will actually use later.

There is a certain satisfaction in a stack where every dependency has a clear reason to exist. I know what handles routing. I know what builds the frontend. I know where the backend begins. When something goes wrong, I have fewer layers to investigate.

It feels like I’m building an application rather than learning the rules of an application framework.

And after years of building things, that feeling matters to me.

### Maybe React is enough

The React ecosystem has spent years making it easier to build increasingly sophisticated applications. Frameworks are useful. Abstractions are useful. Server rendering, server components, and full-stack capabilities solve real problems.

But sometimes we get so used to the most feature-rich option that we forget we can start smaller.

If all you need is a client-side application, React and a router might be enough. Add a data-fetching library if the application needs one. Add server rendering if the requirements justify it. Use a full-stack framework when its full-stack features are actually useful to you.

You don’t have to start with the biggest abstraction available.

I spent more than a year deeply invested in Next.js. It helped me build projects, and I’m glad I learned it. Moving away from it wasn’t an admission that I had chosen badly. It was a consequence of understanding my own requirements better.

BeamDrop was the project that made the difference for me. I tried a different setup, liked how it felt, and kept using it.

That’s really all that happened.

I didn’t discover the one true React stack. I just stopped using a framework for features I barely needed.

**Next.js didn’t lose me because it couldn’t do the job. TanStack Router won me over because it gave me what I actually wanted.**

And so far, I haven’t had a reason to go back.

Yours truly, Tach

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=b911eeb4809a)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/i-moved-all-my-react-apps-away-from-next-js-b911eeb4809a?source=rss-9a41d7ec29fb------2).*
