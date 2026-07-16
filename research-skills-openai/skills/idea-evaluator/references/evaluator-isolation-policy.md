# Evaluator Isolation Policy

Valid evaluation requires a fresh delegated instance, one frozen dossier as the
only project read, read-only source handling, and one review output.

Invalidate and reassign if the evaluator generated/revised the Idea, edits a
source, reads any other project artifact or URL, sees history/scores/decisions,
evaluates a partial dossier, cannot bind the digest, omits required chain/claim
checks, or rewrites the Idea. If delegation is unavailable, return
`independent_review_pending`; never fall back inline.
