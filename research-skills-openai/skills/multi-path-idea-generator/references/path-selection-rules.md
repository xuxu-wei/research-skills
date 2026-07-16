# Path Selection Rules

The orchestrator assigns `focused_optimization` or `bounded_exploration` first.
Generation paths refine how to write a supported direction; they do not decide
the route or candidate count.

- Focused work uses the path closest to the current identity plus any targeted
  repair path needed for evidence-chain or claim support.
- Bounded exploration assigns one primary path per evidence-supported direction
  and keeps only substantively different research identities.
- Base path recommendations on opportunity type, user goal, available data and
  methods, constraints, and known repair needs.
- Do not create an additional direction merely to represent a title, audience,
  or editorial framing alternative; write it as a new version of the same node.
- If the orchestrator has assigned paths, do not expand them. If none is
  defensible, return a failure rather than inventing one.
