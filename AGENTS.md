# 项目规则

## 1. 图像风格与生成协议（强制性）

- **视觉风格**：严格执行带有水彩质感的吉卜力工作室（Studio Ghibli）插画风格。严禁写实、3D 渲染或非吉卜力风格。
- **核心规格 (Consistency Protocol)**：
    1. **Master Specs (物理强锚定)**：必须在 Prompt 顶部明确定义一致性锚点。
        - **人物 (Character)**：发型（色/长/款）、上装（色/领/袖/饰）、下装、特定配饰（如：黑框眼镜、红色碎花手提包）。
        - **场景 (Scene)**：物理边界（如：严格在厨房内）、主色调（如：午后暖阳）、核心地标。
    2. **物理排他 (Negative Constraints)**：Prompt 必须包含 `Strictly in [A], NO [B]`。例如："Strictly in a bedroom, NO outdoor elements, NO cars"。
    3. **官方工具**：必须使用 `scripts/generate_images.py`。
- **核心模型**：`gemini-3.1-flash-image-preview`。
- **环境纯净度 (Artistic Purity)**：
    - **禁止文字**：Prompt 必须包含 `NO text, NO subtitles, NO speech bubbles, NO characters, NO letters`。
    - **追求意境**：画面应呈现出"意境窗"的纯净感，严禁出现任何破坏美感的现代 UI 元素或字符污染。
- **分镜规则**：
    1. **锚点引用 (Anchor Reference)**：`scene1.png` 作为全课"视觉标准图"。后续帧（Scene 2+）生成时，必须将 scene1 的图片字节作为 `inlineData` 传入 Gemini API（多模态输入），让模型**看到**角色而非靠文字猜测——这是防止人物漂移的核心机制，已在 `generate_images.py` 中实现，禁止绕过。
    2. **STORYBOARD 顺序强制**：storyboard 脚本中 `STORYBOARD` 列表的**第一个元素必须是 `scene1`**。`generate_images.py` 按列表顺序执行，scene1 先生成才能成为后续帧的 anchor；若顺序错误，anchor 机制失效。
    3. **视觉对齐**：高度强调不同帧之间的服装和物件保持像素级连续性。
    4. **封面图同步**：`scene1.png` 同时用于 `curriculum.json` 和课程 JSON 的根 `image` 字段。
    5. **稳定开场**：非对话片段不设置独立 `image` 字段，以维持默认背景。
    6. **语义命名**：分镜帧使用语义化名称（如 `man_waves.png`），禁止随意编号。
    7. **人物复制防护（教训：L81）**：仅写 `EXACTLY N people` 不足以防止 AI 复制角色——尤其当同一帧内有**两个同性别角色**时，AI 会把其中一人复制到空位。必须在 `desc` 中加三层约束：
        - ① `STRICTLY N INDIVIDUALS ONLY. Do NOT duplicate any character. Do NOT add extra people.`
        - ② 逐人指定位置与外貌：`The person on the LEFT is X (浅棕发+V领毛衣). The person on the RIGHT is Y (深发+灰夹克).`
        - ③ `These are DIFFERENT people with DIFFERENT hair and clothing — do NOT make them look alike.`
- **重置与覆盖**：更新或修复图片时，**必须强制覆盖**旧文件（`--force`），消除过时 AI 幻觉图。

## 2. Storyboard 脚本规范

每门课程必须有一个独立的 storyboard 脚本，路径为 `scripts/{book}/generate_l{N}_storyboard.py`。脚本通过以下模块变量定义分镜，由 `generate_images.py` 的 `parse_storyboard_script` 自动解析拼接：

```python
# 全局吉卜力画风描述（所有帧共用）
STYLE = "Studio Ghibli-inspired illustration style, ..."

# 场景物理空间定义（保持跨帧一致）
SCENE = "Location: ..., Keep [...] consistent across ALL frames. NO captions, ..."

# 角色外貌定义（每个角色一个变量，变量名以 CHAR_ 开头）
CHAR_FOO = "Character FOO: [age], [hair], [clothing details]. CRITICAL: [key items] NEVER change."
CHAR_BAR = "Character BAR: ..."

# 分镜列表（第一个必须是 scene1，这决定了 anchor 帧）
STORYBOARD = [
    {"id": "scene1",      "desc": "建立场景的宽镜头 ..."},
    {"id": "action_verb", "desc": "对应台词动作的描述 ..."},
    ...
]
```

**规则**：
- `STYLE`、`SCENE`、`CHAR_*` 自动拼接为 `master_prompt`，前缀到每张图的 Prompt。
- `STORYBOARD[0]` 的 `id` 通常为 `scene1`，生成后自动成为该课 anchor。
- 每个 `desc` 只描述**当前帧的动作变化**，角色外貌无需重复（已在 `CHAR_*` 中定义）。
- 每课分镜数量**不少于 5 张**。
- **补图规则（低帧课程强制）**：
    - 若现有课程图片少于 5 张，必须先补 storyboard，再补课程 JSON 的图片映射；禁止只生成图片不更新 JSON。
    - 新增帧必须优先补**剧情转折点、动作变化点、诊断/结论点、笑点/收束点**，不得用语义重复的静态同景图凑数。
    - `segments[].image` 必须按叙事顺序映射到这些新增帧，确保台词与画面语义一一对应；优先采用“发现问题 -> 商量处理 -> 动作检查 -> 诊断结果 -> punchline/收束”的切分方式。
    - 补图完成后，必须复核该课满足：`实际图片数 >= 5`、`实际图片数 = JSON 实际引用数`、`不存在生成了但页面没引用的 PNG`。

## 3. 数据完整性与教材对齐

- **台词校验**：对照 `.lrc` 文件，确保对话片段（Segments）100% 完整。
- **角色映射 (Role Mapping)**：
    - **教材验证**：查阅标准教材插图，确认角色性别、年龄段、外貌特征及人数。
    - **双重校验**：通过录音音色（判断说话人）和教材插图双重验证。如果录音是两个男性，Prompt 必须强调"TWO MEN, NO WOMEN"，且年龄段需明确定义（如：30s Young Man），严禁出现 Age Drift（忽老忽少）。
    - **性别强锚（教训：L75）**：**写 `CHAR_*` 前必须先听录音确认每个角色的性别**，不可凭故事情境猜测（如"鞋店店员应该是女的"）。一旦确认性别，必须在 `CHAR_*` 里加 `CRITICAL: MALE` 或 `CRITICAL: FEMALE`，并在该角色出现的每个 `desc` 里重复一句 `is a MAN / is a WOMAN`，防止 AI 自行篡改。
- **视觉线索补完**：分镜必须包含关键视觉细节（如：领口牌子 label、胸前徽章 badge），即便音频未提及。

## 4. 课程验收标准 (Acceptance Criteria)

1. **物理一致性 (Visual Consistency)**：
    - 检查 Scene 2+ 与 Scene 1 的发型、服装、场景色调是否完全相同。
    - 严禁出现角色在同一课程中"变装"或"变脸"。
2. **语义动效匹配 (Semantic Alignment)**：
    - 画面必须直观解释 Segment 中的核心动词（如：摇头、递物、生气、微笑、指向）。
3. **音画同步性 (Sync Accuracy)**：
    - `startTime` 和 `endTime` 精确匹配音频；切换点位于动作起始点。
4. **环境纯净度 (No Noise)**：
    - 画面严禁出现文字、字幕、对话气泡、漫画分栏或错误文化符号。
5. **语法与翻译 (JSON Validity)**：
    - 中文翻译必须地道无病句；JSON 结构符合规范。

## 5. 交付与自检流程（每次必须执行）

- **JSON 有效性检查**：执行 `jq . <path_to_json>`。大规模修改优先使用 Python 脚本全量重写。
- **视觉图像审查 (Visual Image Review — MANDATORY)**：生成完成后必须用 `Read` 工具实际查看每张生成的 PNG 图像，逐帧确认以下内容：
    - **人物一致性**：同一课程内所有帧的角色发型、服装、体型是否完全相同，无"换装"、无"变脸"、无"忽老忽少"。
    - **空间关系**：场景中角色的位置关系是否符合 storyboard desc 的描述（如剧院排座前后关系）。
    - **人物数量**：每帧出现的角色数量是否正确，无重复人物、无幽灵角色。
    - **无文字污染**：图面中无任何文字、字幕、标注、标志文字。
    - **语义匹配**：画面动作是否与对应台词/desc 描述相符。
    - **若发现问题**：必须修改对应 storyboard desc（加强约束），删除错误图片，重新生成，再次查看确认——直到所有帧合格为止。禁止带着已知错误交付。
- **多维自检记录 (Self-Check Log)**：交付时需显式汇报以下项：
    - [ ] 已核对教材插图/角色性别人数。
    - [ ] 已核对 STORYBOARD 第一个元素为 `scene1`（anchor 顺序正确）。
    - [ ] 已核对 Scene 2+ 与 Scene 1 的物理一致性（anchor 机制已生效）。
    - [ ] 已实际查看全部生成图像，逐帧完成视觉审查。
    - [ ] 确认跨帧人物一致性（服装/发型/年龄无漂移）。
    - [ ] 确认画面无任何文字/气泡/字符污染。
    - [ ] 已执行 jq 语法校验。
    - [ ] 已跑 build 验证。

## 6. Git 规则

- 始终直接在 `main` 分支上工作。
- 及时合并，确保代码库状态最新。
