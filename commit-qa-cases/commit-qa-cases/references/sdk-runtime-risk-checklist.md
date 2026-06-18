# SDK Runtime Risk Checklist

Use this checklist when changes affect SDK runtime behavior, exported APIs, initialization, login, payment, callbacks, event reporting, UI, networking, storage, registry, system APIs, threads, timers, or global state.

For each external or shared resource, answer:

- Does the caller wait for it?
- Can it block, hang, or slow a critical path?
- Is there a timeout or bounded wait?
- What happens on failure, partial failure, malformed data, repeated calls, or concurrent calls?
- Is there cancellation or lifecycle cleanup?
- Are callbacks emitted exactly once and on the expected thread/context?
- Are stale async results ignored after replacement, uninit, or destruction?
- Are logs emitted for both success and failure paths?
- Can QA reproduce and search the failure?

Convert important risks into test cases or explicit residual-risk notes.
