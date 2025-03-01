# Zenith Architecture Specification

## Overview
Zenith Engine is architected around a non-blocking asynchronous event loop with cooperative priority task scheduling.

```
[Inbound Requests] ---> [Event Dispatcher] ---> [Priority Queue] ---> [Worker Pool]
                              |                        |
                              v                        v
                      [Two-Tier Cache]         [Prometheus Exporter]
```
