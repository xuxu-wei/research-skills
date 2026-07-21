# OpenAI 插件开发、测试与版本更新流程

本文档是 `research-skills-openai` 本地开发、测试、任务监控、发布和回滚的唯一权威流程。`AGENTS.md` 只保留不可变约束，`README.md` 只提供快速入口；流程发生变化时，应在同一提交中更新本文档及直接相关的确定性测试，不再维护第二套完整说明。

本文档仅适用于 OpenAI 插件。Hermes 同步按单独排期处理，不得复制 OpenAI 专属的插件元数据、Marketplace 配置或 Codex 运行时命令。

## 1. 身份与通道

始终区分以下三种身份：

1. **源码身份**：`.codex-plugin/plugin.json` 与 `workflow-registry.yaml` 使用相同的纯 SemVer，不包含本地 cachebuster。
2. **Local 安装身份**：个人插件副本保留源码版本前缀，仅在安装副本中使用 `+codex.local-*`；不得把该版本写回或提交到仓库。
3. **GitHub 安装身份**：来自已提交、已推送和已发布源码的纯发布版本，不读取未推送的工作树修改。

Local 和 GitHub 通道任何时候只能启用一个。开发阶段使用 Local；发布验收阶段切换到 GitHub。不得通过手工编辑 `marketplace.json`、`config.toml` 或缓存目录绕过通道管理。

## 2. 建立开发环境

使用 Python 3.11 或更高版本。在仓库根目录建立一次隔离环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8 = "1"
python -m pip install -r requirements-dev.txt
python scripts/openai_plugin_dev.py status
```

Windows 验证终端保持 `PYTHONUTF8=1`，使 Skill 和测试文件按 UTF-8 读取，不依赖系统区域设置。开发应在独立功能分支或 worktree 中进行；开始前检查 `git status --short`，不得重置、覆盖或混入无关用户修改。

后续命令从 manifest 动态读取源码版本，避免在流程文档中硬编码版本号：

```powershell
$sourceVersion = (Get-Content -Raw -Encoding utf8 research-skills-openai/.codex-plugin/plugin.json | ConvertFrom-Json).version
```

### 首次 Local 设置

`install-local` 要求个人 Marketplace 条目已指向 `./plugins/research-skills-openai`。仅当该条目和个人 Local 副本都不存在时，使用 `plugin-creator` 建立它们：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\create_basic_plugin.py" research-skills-openai --with-marketplace --category Research
```

如果 `status --json` 显示已有但不匹配的条目，应停止并通过 `plugin-creator` 修复；不得手工改 Marketplace 文件。默认个人 Marketplace 会被 Codex 自动发现，不需要执行 `codex plugin marketplace add`。

## 3. 本地修改即时生效循环

每轮修改执行以下步骤：

1. 运行 `python scripts/openai_plugin_dev.py status`，确认源码、个人副本、已安装版本和启用通道。
2. 修改前读取最近的 `AGENTS.md`、目标 `SKILL.md` 及其实际需要的直接引用。
3. 修改后对受影响 Skill 运行 `quick_validate.py`，并运行最小相关单元测试或合同测试。
4. 临时禁用 GitHub 通道，使 Local 成为唯一启用通道。可在 Codex App 中禁用；等价 CLI 操作为：

   ```powershell
   $codexCli = (python scripts/openai_plugin_dev.py status --json | ConvertFrom-Json).codex_cli
   & $codexCli plugin remove research-skills-openai@xuxu-research-preview --json
   ```

5. 安装并验证当前工作树的隔离副本：

   ```powershell
   python scripts/openai_plugin_dev.py install-local
   python scripts/openai_plugin_dev.py verify --channel local --expected-version $sourceVersion
   ```

`install-local` 验证现有 Marketplace 条目和源码，将源码复制到个人插件目录，只在副本的 manifest 与 Registry 中写入 cachebuster，并在失败时恢复原 Local 副本。它不会修改受跟踪源码或 Marketplace JSON，也不会要求删除插件缓存。

`verify --channel local` 比较工作树与已安装副本的完整文件清单和文件内容，只允许两个本地版本字段不同。该检查不保存哈希。

Codex 不热加载 Skill。每次重新安装后必须新建测试任务；旧任务只能代表其启动时加载的缓存，不能验收新修改。如果 Windows 正在占用插件副本，可关闭 Codex App 后重装，验证完成再重新打开。

## 4. 测试分层与隔离

按以下层次测试，只扩展到受影响范围：

1. **局部静态验证**：受影响 Skill 的 `quick_validate.py`、只读 lint 或 schema 检查。
2. **插件级验证**：相关合同测试、仓库审计、转换器和插件验证器。
3. **Fresh discovery smoke**：在重装后的新任务中确认目标 Skill、插件基本版本和入口可发现。
4. **Fresh-agent forward test**：使用原始 fixture 和新的输出目录运行真实工作流，不向测试任务泄漏预期缺陷或修复答案。

测试 fixture 保持只读，不得为了让测试通过而修改原始输入。每轮输出写入新的、带插件版本与工作流名称的目录。Writer 可由同一实例完成一次有界修订，但必须保持完整文档身份并交付完整新版本；实质性修改后的 assessor、evaluator 和 reviewer 必须在 fresh task 中读取冻结输入重新评估。

ROADMAP 中已完成的 Phase 是历史快照，不因后续版本更新而自动复跑。只运行当前变更直接影响的回归测试，除非所有者明确重新开启历史 Phase。

### 测试运行元数据

每个测试输出根目录维护 `run-metadata.yaml`，并将其登记到该轮产物索引。至少记录：

```yaml
plugin:
  channel: local | github
  source_version: <pure-semver>
  installed_version: <resolved-installed-version>
  installed_cache_root: <exact-path>
  skill_count: <integer>
  reviewer_count: <integer>
run:
  workflow: <workflow-name>
  evidence_mode: <mode-or-not-applicable>
  fixture_path: <exact-read-only-input-path>
  output_root: <exact-output-path>
  task_id: <task-identity>
  started_at: <timestamp>
  ended_at: <timestamp-or-null>
  terminal_status: running | completed | failed | interrupted | invalid
```

不得把 SHA256 或其他 Digest 持久化到 LLM-facing 接口或人工审阅记录。插件一致性由确定性工具在内存中完成清单和内容比较；产物完整性由 `{artifact_id, version, exact_path}`、完整索引和唯一当前指针维护。

## 5. 监控与故障分类

任务状态与终态报告是主要依据，文件更新时间和进程活动仅作辅助。终端显示乱码不能证明 UTF-8 文件损坏；必要时用严格 UTF-8 解码或码点检查验证源文件。

长任务应由启动它的 Codex CLI 或 App 任务持续监视：

- 连续约 10 分钟没有状态或产物变化时，先查询任务状态，不立即中断。
- 再经过约 10 分钟仍无任务响应、文件变化或进程活动时，才标记为疑似停滞并决定是否中断。
- 完成、失败或中止后报告终态，关闭应关闭的 CLI 进程或辅助测试任务，并保留有诊断价值的部分产物。

按影响分类处理失败：

- **Critical/Major**：定位最小根因，实施最小修复，重新安装 Local，并用 fresh task 重测。
- **Minor**：若只是局部漏执行或指令偏离，且未改变科学内容、内容保真、readiness、决策或大范围输出，仅记录到 `tests/readability-workflow-test-report.md`。记录插件版本、问题现象、推测诊断和拟议方案；不主动复现，不启动新的修复—测试循环。
- **Harness/environment**：测试工具、权限、编码、联网或任务调度故障使本轮无效。先修复测试环境并重新运行，不因此修改 Skill。

## 6. 发布与回滚

只有 Local 验收通过后才能发布：

1. 确认安装型行为变更已使用合适的新 SemVer，并同步当前 manifest、Registry 和版本声明；纯文档变更不需要版本升级。
2. 运行当前改动适用的验证，修复全部错误并报告剩余警告。
3. 精确暂存本次变更；不得提交本地 cachebuster、机密 fixture、生成的测试输出或无关用户工作。
4. 在功能分支提交并推送，等待 CI，通过审阅后合并到主分支并创建不可移动的版本 tag。
5. 发布后切换通道：

   ```powershell
   $sourceVersion = (Get-Content -Raw -Encoding utf8 research-skills-openai/.codex-plugin/plugin.json | ConvertFrom-Json).version
   $codexCli = (python scripts/openai_plugin_dev.py status --json | ConvertFrom-Json).codex_cli
   & $codexCli plugin remove research-skills-openai@local --json
   & $codexCli plugin marketplace upgrade xuxu-research-preview
   & $codexCli plugin add research-skills-openai@xuxu-research-preview --json
   python scripts/openai_plugin_dev.py verify --channel github --expected-version $sourceVersion
   ```

6. GitHub 通道验证后新建任务运行 discovery smoke。只有该任务确认正式安装版本和入口正确，才能宣布发布完成。

发布失败时不得移动或复用既有 tag。需要继续工作时，禁用 GitHub 通道，从最后一个良好 tag 的干净 worktree 安装 Local 副本；正式修复使用新的版本号重新发布。

## 7. 每次交付检查表

- 当前只有一个插件通道启用。
- 源码版本是纯 SemVer，Local cachebuster 未进入工作树。
- `verify` 绑定正确通道和源码版本。
- 行为测试来自重装后的 fresh task，fixture 未被修改。
- `run-metadata.yaml` 和产物索引完整，不包含持久化 Digest。
- 只运行受影响验证；未自动重跑已完成的 ROADMAP Phase。
- Minor 偏离只记入维护报告，Critical/Major 与环境故障按不同路径处理。
- 发布提交不包含机密输入、生成输出或无关用户修改。
- GitHub 通道 smoke 通过后才宣布发布，失败时不移动 tag。
