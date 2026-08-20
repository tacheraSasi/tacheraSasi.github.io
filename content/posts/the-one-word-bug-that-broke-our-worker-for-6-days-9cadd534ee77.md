---
title: "The One-Word Bug That Broke Our Worker for 6 Days"
date: 2026-04-28
summary: "For six days, our system was lying to us \u2014 not crashing, just quietly doing nothing. The cause? One wrong word in a shell script."
draft: false
medium: "https://medium.com/@tacherasasi/the-one-word-bug-that-broke-our-worker-for-6-days-9cadd534ee77?source=rss-9a41d7ec29fb------2"
tags: ["devops", "docker", "golang"]
---

![](https://cdn-images-1.medium.com/max/1024/1*CtVFn53iNGx3lQ2MEe3JKw.png)

### For six days, our system was lying to us

Not crashing. Not failing loudly. Just quietly pretending everything was fine while doing absolutely nothing.

And the cause?

One wrong word in a shell script.

### Everything Looked Fine

We run a pretty standard setup:

* A Go API (core)
* A background worker (minion)
* Redis for queues
* Docker Compose holding it all together

We recently moved bulk SMS processing into the worker using Asynq. Clean separation, better scalability, the usual win.

We deployed.

The API responded perfectly:

```
200 OK  
"bulk SMS queued successfully
```

Except… no SMS was ever sent.

### The Worker Was Dead Silent

First instinct: check the worker logs.

Nothing.

No errors. No panics. No trace of the task ever being picked up.

Just one quiet warning after retries were exhausted.

Meanwhile, everything else worked:

* login alerts ✅
* email notifications ✅
* scheduled jobs ✅

Only bulk SMS failed.

At this point, we did what engineers always do when the signal is weak:

We guessed.

### We Investigated the Wrong Things

We went deep into the stack:

* Suspected Redis corruption
* Questioned queue priorities
* Looked for serialization bugs
* Added panic recovery middleware
* Logged full payloads
* Added startup diagnostics

We deployed again.

Still nothing.

And this is where most people waste days. We almost did.

Because we were debugging behavior… not reality.

### The Subtle Clue

There was one tiny inconsistency.

Our worker used to log:

```
Worker started
```

We had changed it to:

```
Worker started (server + scheduler running)
```

After deploy, the logs still showed the old message.

That should have been the end of the investigation right there.

Our code wasn’t running.

### The Real Problem

The issue wasn’t in Go.  
It wasn’t in Redis.  
It wasn’t in queues.

It was in this script:

```yaml
docker compose build --no-cache api  
docker compose up -d --remove-orphans
```

And this config:

```yaml
services:  
  core:  
  minion:  
  db:  
  redis:
```

Look closely.

We were building api.

There is no api.

Docker didn’t complain. It didn’t warn. It didn’t fail.

It just did nothing.

And then docker compose up happily started containers using old cached images.

So for six days:

* The API sometimes rebuilt
* The worker never rebuilt
* The system kept deploying successfully
* Our fixes never actually shipped

We were debugging code that wasn’t even running.

### The Fix Was Embarrassing

```
- docker compose build --no-cache api  
+ docker compose build --no-cache core minion
```

That’s it.

Two words instead of one.

We deployed again.

Immediately:

* New startup logs appeared
* Bulk SMS tasks were picked up
* Jobs executed in milliseconds

System fixed.

### What This Actually Teaches

### 1\. If your fix doesn’t change behavior, assume it never deployed

Stop overthinking.

Before touching Redis, queues, or concurrency… ask:

**“Is my new binary even running?”**

If you skip this, you deserve the hours you’re about to lose.

### 2\. Silent failures are worse than crashes

Crashes force action.

Silent no-ops pass CI, pass deploys, and waste days.

docker compose build should not succeed when the service doesn’t exist.

But it does.

So you have to defend against that yourself.

### 3\. Your deployment pipeline is part of your codebase

People treat scripts like they’re disposable.

They’re not.

That one-line deploy.sh caused more damage than any bug in the Go code.

Review it. Test it. Break it intentionally.

### 4\. Logging is not optional for workers

If your worker can fail quietly, it will.

You need:

* startup fingerprints (commit hash, build time)
* task-level logs
* explicit success/failure visibility

Otherwise, you’re blind.

### 5\. Rename things properly or don’t rename them at all

api became core.

The script didn’t.

That mismatch cost six days.

Refactors don’t end when the code compiles.

### The Real Lesson

This wasn’t a debugging failure.

It was a discipline failure.

We trusted the pipeline without verifying it.  
We chased complex explanations before ruling out simple ones.  
We debugged symptoms instead of checking fundamentals.

And that’s how a one-word mistake beats experienced engineers.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=9cadd534ee77)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/the-one-word-bug-that-broke-our-worker-for-6-days-9cadd534ee77?source=rss-9a41d7ec29fb------2).*
