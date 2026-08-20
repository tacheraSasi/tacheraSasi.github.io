---
title: "How TypeScript Enums Compile to JavaScript (And Why It Matters)"
date: 2025-08-31
summary: "TypeScript enums compile to JavaScript in surprising ways. Understanding the output helps you use them wisely."
draft: false
medium: "https://medium.com/@tacherasasi/how-typescript-enums-compile-to-javascript-and-why-it-matters-8766881c1728?source=rss-9a41d7ec29fb------2"
tags: ["typescript", "javascript", "enums-in-typescript"]
---

When you’re learning TypeScript, it’s easy to overlook that it all boils down to plain JavaScript in the end. Most TypeScript goodies like types, interfaces, and unions vanish after compilation, living only to help catch errors during development. But there’s one feature that sticks around: **enums**. They’re a bit special, and here’s why.

### What Happens with Numeric Enums

Let’s say you create a simple enum like this:
```


enum Direction {  
  Up,  
  Down,  
  Left,  
  Right  
}
```

When TypeScript compiles this, it doesn’t just disappear. Instead, it turns into this JavaScript:
```js


var Direction;  
(function (Direction) {  
Direction[Direction["Up"] = 0] = "Up";  
Direction[Direction["Down"] = 1] = "Down";  
Direction[Direction["Left"] = 2] = "Left";  
Direction[Direction["Right"] = 3] = "Right";  
})(Direction || (Direction = {}));
```

This code creates a **two-way street** : you can look up values both ways. For example:
```


Direction.Up === 0;      // true  
Direction[0] === "Up";   // true
```

So, unlike most TypeScript features, enums don’t just exist for type-checking they become **real objects** in your JavaScript code.

### Why This Is a Big Deal

Here’s why you should care:

  * **Bundle Size:** Enums generate actual JavaScript code, which can make your final bundle heavier. If you’re not careful, this can add up.
  * **Unexpected Perks:** Enums let you do cool things like reverse lookups (e.g., getting “Up” from 0). Handy, but it might catch you off guard if you’re not expecting it.
  * **Lighter Options:** If you just need simple constants, you might want to use const enum or plain string literals instead. They’re leaner and don’t add extra code to your JavaScript.



### The Bottom Line

Understanding how enums work under the hood helps you write **smarter, cleaner code**. Every time you use an enum, keep in mind: you’re not just writing TypeScript you’re creating real JavaScript objects that live in your final app. Use them wisely!

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=8766881c1728)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/how-typescript-enums-compile-to-javascript-and-why-it-matters-8766881c1728?source=rss-9a41d7ec29fb------2).*