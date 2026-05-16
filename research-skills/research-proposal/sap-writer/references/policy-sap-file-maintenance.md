# SAP File Maintenance Policy

## Purpose
Ensure SAP drafting and revision remain file-centered and auditable.

## Required tracking
Each SAP drafting or revision task must maintain:
- `sap_file_path`
- `sap_version`
- linked `proposal_file_path`, if available
- source context or preflight report reference
- change summary
- unresolved SAP issues

## Initial draft
The initial draft should create a new SAP file and return its path and version.

## Revision
A revision should either update the existing SAP file while preserving version history, or create a clearly versioned new file. It must not create an unrelated SAP without lineage.

## Change summary
Each revision should identify:
- What changed
- Which evaluator concerns were addressed
- Which issues remain unresolved
- Whether any new assumptions were introduced

## Prohibited behavior
- Overwriting prior SAP without traceable version information
- Losing unresolved issues
- Treating formatting edits as substantive statistical revision
- Creating SAP content that conflicts with the proposal or preflight report
