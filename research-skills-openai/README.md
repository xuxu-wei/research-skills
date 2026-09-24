# Research Skills

An OpenAI-oriented, skills-only research plugin for Codex. It contains 8 skills covering academic writing and editing, five research authoring workflows, and unified research evaluation, including methodology consultation and study improvement advice.

The main task develops and revises the work; fresh reviewers assess its scientific content. All research workflows and reviewers use the shared writing and editing skills for reader-facing material. General search, data access, and document handling use the tools available in the environment.

All 8 skills allow automatic matching to a relevant task and remain available by explicit name. Discovery descriptions lead with their core use cases. Matching in everyday tasks still requires owner validation.

[Academic Writer](skills/academic-writer/SKILL.md) and [Academic Humanizer](skills/academic-humanizer/SKILL.md) also work independently across academic and educational tasks. Their instructions and reference explanations are written in Chinese for owner review; they support Chinese and English output according to the task and manuscript language.

[Research Evaluator](skills/research-evaluator/SKILL.md) replaces the former evaluator, medical journal review, research improvement planning, and methodology preflight entries. It provides explained assessments of research value, scientific support, proposal readiness, and analysis-plan executability, with publication consultation and editorial handling when needed. Its Chinese instructions load task guidance and scoring criteria as needed. Automatic matching preserves the same independent-review requirements. Reports use full names and reader-facing explanations; the proposed task scales await owner testing.

[SAP Writer](skills/sap-writer/SKILL.md) connects research questions, shared definitions, analysis methods, uncertainty, and reporting in a plan suited to the study. Its Chinese instructions link to separate references for document organization and analysis decisions. Detailed models and calculations can be placed in appendices; the plan's language and format follow the task.

- [Skill catalog, migration, installation, and compatibility export](../README.md)
- [Development and manual testing](../docs/development.md)
- [Roadmap and manual validation status](../ROADMAP.md)
- [Plugin metadata](.codex-plugin/plugin.json)
- [License](LICENSE)

Skill behavior is tested manually by the owner. Automated tests cover auxiliary scripts only. This remains an experimental personal project; ChatGPT web installation and behavior have not been verified.
