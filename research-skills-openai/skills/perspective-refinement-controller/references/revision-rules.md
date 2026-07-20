# Revision Rules

Every revision item must trace to an evaluator or panel issue ID.

Allowed strategies:
- add: add a targeted sentence or paragraph
- replace: replace unsupported or unclear wording
- condense: reduce background or caveats
- delete: remove orphan or unsupported material
- clarify: make thesis, boundary, or evidence relation explicit
- reorder: move material to restore argument flow

Body-integration choices:
- in_body
- response_only
- not_addressed_with_reason

Substantive changes that alter claim strength, add evidence, or introduce a new claim require a claim change request and curator merge before drafting.

For editorial repair:

- accept only the single normalized YAML brief, current frozen Perspective, and protected-content register;
- require the current scientific version's exact `writer_instance_id`;
- preserve every Claim ID, source Binding ID, evidence status, terminology meaning, and counterargument/boundary family authority;
- keep one authoritative exposition per family and do not replace omitted repetitions with pointers;
- route any scientifically meaningful change back to scientific revision before prose changes;
- do not expose raw narrative/language assessments or prior evaluator material to the writer.
