---
title: "What Building malloc Taught Me About Memory"
date: 2026-03-13
summary: "I implemented a tiny version of malloc to understand what really happens under the hood. The result was surprisingly simple and incredibly educational."
draft: false
medium: "https://medium.com/@tacherasasi/what-building-malloc-taught-me-about-memory-57eae5b35166?source=rss-9a41d7ec29fb------2"
tags: ["clang"]
---

![](https://cdn-images-1.medium.com/max/1024/1*2dOqSEchtIkDv2Fma09rOA.png)

Modern developers rarely think about memory.

We call malloc, new, or let a garbage collector handle everything. Most of the time that’s perfectly fine. But recently I decided to dig deeper and implement a very small version of malloc myself.

Not to replace real allocators. Just to understand what actually happens under the hood.

The result was surprisingly simple and incredibly educational.

This post walks through the core ideas.

### Why Understanding Memory Still Matters

Most software today runs on layers of abstraction.

Frameworks → languages → runtimes → operating systems.

That’s powerful, but it also means many developers never see the **foundations** those layers are built on.

Understanding memory allocation helps with:

• writing faster software  
• debugging memory issues  
• understanding how runtimes work  
• building systems tools  
• designing better APIs

Even if you work in higher level languages like **Go** , these concepts still power everything underneath.

### Step 1: Where malloc Gets Memory

When a program runs, memory roughly looks like this:
```


Code  
Globals  
Heap  ← grows upward  
Stack ← grows downward
```

malloc allocates from the **heap**.

Under the hood, the allocator asks the OS for more heap space using a system call like sbrk().

Example:
```


void *ptr = sbrk(1024);
```

This moves the **program break** forward by 1024 bytes and returns a pointer to the new memory.

Think of it like extending the end of your program’s heap.

### Step 2: The Naive Allocator

The simplest possible allocator would just call sbrk.
```


void *my_malloc(size_t size) {  
    return sbrk(size);  
}
```

But this immediately creates a problem.

If you later call free, the allocator has **no idea** :

• how big the allocation was  
• where the next block starts  
• whether a block can be reused

So real allocators store **metadata**.

### Step 3: The Hidden Header Trick

Every allocation secretly stores a small header before the memory returned to the user.

Memory layout:
```


[ HEADER ][ USER MEMORY ]
```

The header might contain:
```


size  
is_free  
next_block
```

Example structure:
```rust


typedef struct block_header {  
    size_t size;  
    int is_free;  
    struct block_header *next;  
} block_header_t;
```

When the allocator returns memory, it actually returns a pointer **after the header**.
```


return (void *)(block + 1);
```

Which means the user sees:
```


ptr → usable memory
```

While the allocator still has its metadata.

### Step 4: Tracking Allocations

Blocks are usually tracked using a linked list.
```


heap_start  
   ↓  
[block A] → [block B] → [block C]
```

When malloc runs:

  1. search for a free block big enough
  2. reuse it if possible
  3. otherwise request more memory from the OS



This keeps allocations fast and avoids unnecessary system calls.

### Step 5: What free Actually Does

One surprising thing: free usually does **not return memory to the OS**.

Instead it just marks the block as reusable.
```


[HEADER free=1][memory]
```

Future allocations can reuse that block instead of requesting more memory.

### What Real Allocators Do Differently

Real allocators (like the ones used by **glibc**) add several optimizations:

**Block splitting**
```


Free block: 100 bytes  
Need: 20
```

Split into:
```


20 used  
80 still free
```

**Block coalescing**

Adjacent free blocks merge together to reduce fragmentation.

**Large allocation handling**

Large allocations often use mmap instead of the heap.

**Thread safety**

Modern allocators maintain thread local arenas for performance.

### What I Learned From This

Building even a tiny allocator reinforced a few important lessons.

### Abstractions hide complexity, but the fundamentals still matter

Languages like **Go** make memory management easier, but the underlying principles are still there.

### Performance often comes from understanding the layers below you

Understanding memory layout and allocation patterns helps explain why some code performs better than others.

### Systems knowledge compounds

Once you understand memory allocators, many other topics suddenly make more sense:

• garbage collectors  
• runtime design  
• kernel memory management  
• high performance servers

### Final Thoughts

You don’t need to write your own allocator for production software.

But building one, even a small version, forces you to think like the runtime.

And that perspective is valuable.

The more you understand the layers beneath your tools, the better engineer you become.

GITHUB => <https://github.com/tacheraSasi/malloc.git>

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=57eae5b35166)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/what-building-malloc-taught-me-about-memory-57eae5b35166?source=rss-9a41d7ec29fb------2).*