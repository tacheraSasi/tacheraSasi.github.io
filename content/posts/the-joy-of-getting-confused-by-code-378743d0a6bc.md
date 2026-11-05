---
title: "The Joy of Getting Confused by Code"
date: 2026-11-05
lastmod: 2026-11-05
draft: false
author: "Tachera W Sasi"
description: "I’ve been writing Zig for about a year now."
summary: "I’ve been writing Zig for about a year now."
tags: ["zig", "systems-programming", "programming"]
categories: []
keywords: []
images: ["/images/me.jpg"]
medium: "https://medium.com/@tacherasasi/the-joy-of-getting-confused-by-code-378743d0a6bc?source=rss-9a41d7ec29fb------2"
---

![](https://cdn-images-1.medium.com/max/1024/1*yimGt7leNQsqkRCMRDGTng.png)

I’ve been writing Zig for about a year now.

I’ve been practicing it almost daily, building things, reading other people’s code, and slowly getting more comfortable with the language.

At this point, the syntax itself isn’t really the problem anymore. I can read structs, functions, pointers, allocators, error handling, and most of the things I encounter in everyday Zig code.

Of course, there are still concepts that make me stop and think.

And honestly, those moments are probably my favorite part of programming.

Recently, I had one of those moments while reading a small piece of code I found on the internet.

It was a simple Wget clone written in Zig. The entire thing was less than 200 lines of code. It could download files from the internet, split downloads into chunks, and write the downloaded data to a file.

Nothing particularly crazy.

I was just tracing the code, trying to understand how everything worked.

Then I saw something that made me stop.

### The first thing that confused me

Before I get to what I saw, there’s something about Zig that had bothered me before.

Imagine you have a User struct with a function called init that creates a new user.

In Zig, you can explicitly call the initialization function through the type.

For example:

```zig
const User = struct {
    name: []const u8,
    age: u8,
    fn init(name: []const u8, age: u8) User {
        return .{
            .name = name,
            .age = age,
        };
    }
};
const user = User.init("Tach", 25);
```

Here, everything is explicit. I’m calling init through User, and the function returns an instance of User.

But you can also do something like this:

```
const user: User = .init("Tach", 25);
```

Wait. What?

There’s no User before .init() anymore.

Instead, I’m declaring the variable as a User, and the compiler figures out what .init() means from that context.

The second form initially felt weird to me.

How does the compiler know what .init() is when there's no type name before it?

I eventually looked it up and learned about contextual type inference.

Basically, the compiler can use information from the surrounding context to figure out how to interpret an expression.

That little discovery stuck with me.

I had encountered it before, understood it, and moved on.

Until recently.

### Wait, where does this value come from?

I was tracing the downloader’s main function when I came across this:

```
const bytes_written = download(
    &client,
    .cwd(),
    uri,
    destination,
) catch |err| {
    std.debug.print("{t}\n", .{err});
    return 1;
};
```

I understood most of what was happening here.

The program was calling a function named download, passing in the HTTP client, the URL, and the destination filename.

But then there was this:

.cwd()

Wait.

What the fuck is that?

I knew the function was expecting a directory value. So I went to the function definition to see what the parameter actually was.

```zig
fn download(
    client: *std.http.Client,
    destination_dir: Io.Dir,
    uri: std.Uri,
    destination: []const u8,
) !u64 {
    // ...
}
```

There it was.

destination_dir was of type Io.Dir, a type from Zig's standard library that represents a directory handle.

And the function was receiving .cwd().

Where was that coming from?

I know that function arguments have to be actual values.

If a function expects a string, I need to pass it a string. If it expects a struct, I need to pass it an instance of that struct.

But here I was looking at a dot followed by a function call.

For a few minutes, I just stared at it.

Then I started thinking about that earlier discovery.

### Could the compiler be doing the same thing?

I remembered how Zig could infer the type of .init() when the expected type was already known.

So I started wondering:

Could the compiler also be using the expected argument type to figure out what .cwd() means?

The function expects an Io.Dir.

And .cwd() is a function associated with Io.Dir that returns a directory value representing the current working directory.

Maybe Zig was using the expected type to resolve the function call.

That was my first thought.

And then I started making another connection.

If I had a User struct with an init function that returned a User, could I pass .init() directly to a function expecting a User?

Could I do the same thing with other types?

That was the part that really intrigued me.

I wasn’t just trying to understand one line of code anymore.

I was trying to understand whether I had discovered a general pattern in the language.

### The compiler isn’t doing magic

What I was connecting was contextual type inference.

In Zig, the expected type can help the compiler resolve a leading-dot expression.

In this case, the parameter is explicitly declared as Io.Dir, so Zig can use that type to resolve .cwd() to the appropriate declaration.

The function still exists.

The value is still real.

The compiler isn’t creating a directory out of thin air.

It’s simply using information that’s already available to figure out what the expression means.

And that was the part I found interesting.

I had always thought about function arguments as values that needed to be explicitly named or qualified.

But Zig was showing me that sometimes the context already tells the compiler enough.

### A little more context about the downloader

The more I traced the code, the more I appreciated how the pieces fit together.

Before downloading the file, the program creates an I/O environment:

```go
var threaded: Io.Threaded = .init(init.gpa, .{
    .async_limit = .limited(parallel_requests),
    .concurrent_limit = .limited(worker_limit),
});

defer threaded.deinit();
const io = threaded.io();
```

Here, I already understood what was happening.

The program was setting up a threaded I/O implementation with limits for asynchronous and concurrent operations.

Then it created an HTTP client:

```go
var client: std.http.Client = .{
    .allocator = init.gpa,
    .io = io,
};

defer client.deinit();
```

This was another example of the same kind of syntax I had learned before.

The compiler knows the type of client, so it can infer the type of the struct literal on the right side.

Nothing surprising there.

But the .cwd() call was different enough to make me stop.

It wasn’t just initializing a struct.

It was using the expected argument type to resolve a function call, right there in a function argument.

And seeing it in actual code made the concept click in a way that reading about it hadn’t.

### Why I love getting confused by code

The interesting thing is that I wasn’t struggling with Zig syntax.

I’ve been writing Zig for a year. The syntax itself is familiar.

What caught me off guard was the concept behind it.

And I think that’s something I’ve started appreciating more as I spend time reading code written by other people.

Sometimes you encounter a feature that seems completely ordinary to the person who wrote the code, but it makes you stop and rethink something you thought you understood.

Those moments are incredibly satisfying.

Not because you suddenly become an expert, but because a small piece of the language becomes clearer than it was before.

I didn’t learn an entirely new programming language today.

I just understood one more thing about a language I’ve already been using.

And somehow, that felt exciting enough to write about.

Maybe that’s the best part of learning programming.

Sometimes, you don’t need to build something impressive or solve a massive problem.

Sometimes, all it takes is a tiny piece of code that makes you go:

“Wait, what the fuck is this?”

And then spending a few minutes figuring it out.

That’s the joy of getting confused by code.

**The code that started this whole thing:** [A tiny Wget clone written in Zig](https://gist.github.com/nubskr/c2b4a4ce3c16214c18718e24471520c6)

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=378743d0a6bc)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/the-joy-of-getting-confused-by-code-378743d0a6bc?source=rss-9a41d7ec29fb------2).*
