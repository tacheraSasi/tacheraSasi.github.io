---
title: "Why Most Engineers Shouldn\u2019t Build Distributed Systems (And Why I Did Anyway)"
date: 2026-03-05
summary: "Distributed systems are fascinating \u2014 and one of the fastest ways to create massive complexity. Why most engineers shouldn't build them, and why I did anyway."
draft: false
medium: "https://medium.com/@tacherasasi/why-most-engineers-shouldnt-build-distributed-systems-and-why-i-did-anyway-20e6ace3f18e?source=rss-9a41d7ec29fb------2"
---

![](https://cdn-images-1.medium.com/max/1024/1*JzWgtsxR_ozYKkQSqV6jVw.png)

Distributed systems are one of the most fascinating areas in software engineering.

They’re also one of the fastest ways to accidentally create massive complexity.

A lot of engineers jump straight into microservices, container orchestration, and distributed architectures because it sounds scalable and modern.

But in reality, distributed systems introduce an entirely new category of problems.

When your system runs on a single machine, many things are simple.

Function calls are instant.  
Memory access is predictable.  
Failures are easier to understand.

For example, a local function call might look like this:
```go


func processOrder(orderID string) error {  
    order := getOrder(orderID)  
    chargeCustomer(order)  
    updateInventory(order)  
    return nil  
}
```

Everything happens inside one process.  
No network. No timeouts. No partial failures.

But once your system becomes distributed, the same operation might involve multiple services communicating over the network.
```go


func processOrder(orderID string) error {  
    order, err := orderService.Get(orderID)  
    if err != nil {  
        return err  
    }


    err = paymentService.Charge(order.CustomerID, order.Total)  
    if err != nil {  
        return err  
    }


    err = inventoryService.Reserve(order.Items)  
    if err != nil {  
        return err  
    }


    return nil  
}
```

Now things become much more complicated.

What happens if the payment service succeeds but the inventory service fails?

What if the network times out but the request actually succeeded?

What if the service crashes halfway through the workflow?

These are common distributed system problems.

### Failures Become Normal

In distributed systems, failures are not exceptions.

They are expected behavior.

A simple HTTP call can fail in many ways:
```go


resp, err := http.Get("http://node-service/tasks")


if err != nil {  
    // network failure  
    retry()  
}
```

But what kind of failure is it?

  * The server might be down
  * The network might be slow
  * DNS might fail
  * The request might succeed but the response gets lost



Handling these cases correctly requires retries, timeouts, and idempotent operations.

### Scheduling Work Across Machines

One of the challenges I encountered while building a cloud orchestration system was scheduling workloads across multiple nodes.

A very simplified scheduler might look like this:
```ts


type Node struct {  
    ID       string  
    Capacity int  
    Used     int  
}


func schedule(nodes []Node, job Job) *Node {  
    for i := range nodes {  
        if nodes[i].Capacity-nodes[i].Used >= job.Resources {  
            return &nodes[i]  
        }  
    }  
    return nil  
}
```

This looks simple.

But real systems quickly introduce more challenges:

  * nodes going offline
  * jobs failing midway
  * resource fragmentation
  * network delays
  * distributed state



A production system requires heartbeat monitoring, leader election, failure recovery, and task rescheduling.

Suddenly the architecture grows significantly.

### Debugging Becomes Harder

Debugging distributed systems is also more complex.

In a monolith, you can follow logs sequentially.

In a distributed system, a single request might pass through several services:
```


API Gateway -> Auth Service -> Order Service -> Payment Service -> Inventory Service
```

To debug issues, you often need distributed tracing tools to reconstruct the path of a request.

Without observability, diagnosing issues becomes extremely difficult.

### Do Most Companies Need This?

In many cases, the answer is **no**.

A well designed monolith can scale surprisingly far.

Many successful products run on monolithic architectures much longer than engineers expect.

Distributed systems should only be introduced when they solve a clear scaling or reliability problem.

### But There Is Still Value in Learning Them

Even though most systems don’t need distributed architectures immediately, understanding them provides enormous value.

Once you understand how systems fail across networks and machines, you begin designing software differently.

You think more about:

  * fault tolerance
  * system boundaries
  * reliability
  * observability



Those lessons improve every backend system you build.

Distributed systems are powerful tools.

But like all powerful tools, they should be used carefully.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=20e6ace3f18e)

---

*Originally published on [Medium](https://medium.com/@tacherasasi/why-most-engineers-shouldnt-build-distributed-systems-and-why-i-did-anyway-20e6ace3f18e?source=rss-9a41d7ec29fb------2).*