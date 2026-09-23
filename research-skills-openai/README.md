# Research Skills

An OpenAI-oriented, skills-only research plugin for Codex. It contains 10 skills covering academic writing and editing, six research authoring workflows, methodology consultation, and unified research evaluation.

The main task develops and revises the work; fresh reviewers assess its scientific content. All research workflows and reviewers use the shared writing and editing skills for reader-facing material. General search, data access, and document handling use the tools available in the environment.

[Academic Writer](skills/academic-writer/SKILL.md) and [Academic Humanizer](skills/academic-humanizer/SKILL.md) also work independently across academic and educational tasks. Their instructions and reference explanations are written in Chinese for owner review; they support Chinese and English output according to the task and manuscript language.

[Research Evaluator](skills/research-evaluator/SKILL.md) replaces the six former evaluator skills and medical journal review. It provides explained assessments of research value, scientific support, proposal readiness, and analysis-plan executability, with publication consultation and editorial handling when needed. Its Chinese instructions load task guidance and scoring criteria as needed. It remains explicitly invoked. Reports use full names and reader-facing explanations; the proposed task scales await owner testing.

- [Skill catalog, migration, installation, and compatibility export](../README.md)
- [Development and manual testing](../docs/development.md)
- [Roadmap and manual validation status](../ROADMAP.md)
- [Plugin metadata](.codex-plugin/plugin.json)
- [License](LICENSE)

Skill behavior is tested manually by the owner. Automated tests cover auxiliary scripts only. This remains an experimental personal project; ChatGPT web installation and behavior have not been verified.
