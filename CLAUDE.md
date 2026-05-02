# 项目规则

> **Language note**: Please always use simple English. I am learning English.

## 1. 图像风格与生成协议（强制性）

- **视觉风格**：严格执行带有水彩质感的吉卜力工作室（Studio Ghibli）插画风格。严禁写实、3D 渲染或非吉卜力风格。
- **核心规格 (Consistency Protocol)**：
    1. **Master Specs (物理强锚定)**：必须在 Prompt 顶部明确定义一致性锚点。
        - **人物 (Character)**：发型（色/长/款）、上装（色/领/袖/饰）、下装、特定配饰。
        - **场景 (Scene)**：物理边界（如：严格在厨房内）、主色调、核心地标。
    2. **物理排他 (Negative Constraints)**：Prompt 必须包含 `Strictly in [A], NO [B]`。
    3. **生成方式**：通过 storyboard 脚本 + `export $(cat .env | grep -v '#' | xargs)` 注入 `GOOGLE_API_KEY` 后执行。
- **环境纯净度**：每帧 Prompt 必须包含 `NO text, NO subtitles, NO speech bubbles, NO letters`。
- **分镜规则**：
    1. **锚点引用 (Anchor Reference)**：`scene1.png` 作为全课"视觉标准图"。后续帧（Scene 2+）生成时，必须将 scene1 图片字节作为 `inlineData` 传入 Gemini API，让模型**看到**角色——这是防止人物漂移的核心机制。
    2. **STORYBOARD 顺序强制**：`STORYBOARD` 列表第一个元素必须是 `scene1`，scene1 先生成才能成为 anchor。
    3. **叙事剧透防护（教训：L13）**：写 storyboard 前必须先通读全课台词，识别"悬念"与"揭秘"节点。**scene1 不得提前展示故事中计划揭秘的道具**（如故事里要上楼才能看到裙子，scene1 绝不能出现裙子）。每帧的 desc 必须反映角色**此刻在故事里所处的位置和状态**，而非跳跃到后续剧情。
    4. **局部重生成时的 anchor**：当只重生成部分帧时，以**最新生成的视觉上最接近目标风格的帧**（而非原始 scene1）作为 anchor，确保重生成帧与已更新帧一致。
    5. **人物复制防护（教训：L81）**：两个同性别角色同帧时，必须在 `desc` 中加三层约束：① `STRICTLY N INDIVIDUALS ONLY. Do NOT duplicate any character.` ② 逐人指定位置与外貌。③ `These are DIFFERENT people with DIFFERENT hair and clothing.`
    6. **封面图同步**：`scene1.png` 同时用于 `curriculum.json` 和课程 JSON 的根 `image` 字段。

## 2. Storyboard 脚本规范

路径：`scripts/{book}/generate_l{N}_storyboard.py`，每课一个独立脚本。

```python
STYLE = "Studio Ghibli-inspired illustration style, ..."
SCENE = "Location: ..., Strictly in [...], NO [...]. "   # 每帧共用的场景锚点
# 若课程含多个物理场景，定义多个 SCENE_* 变量，在生成逻辑里按帧选用
CHAR_FOO = "Character FOO: [age], [hair], [clothing]. CRITICAL: MALE/FEMALE."
STORYBOARD = [
    {"id": "scene1", "desc": "建立场景宽镜头，角色外貌无需重复 ..."},
    {"id": "action_verb", "desc": "当前帧动作变化 ..."},
]
```

**规则**：
- 每课分镜**不少于 5 张**；每个 `desc` 只描述当前帧动作，外貌由 `CHAR_*` 覆盖。
- 若课程含多个物理场景，在各帧 desc 里必须用文字极度精确地复述场景锚点（多场景漂移教训）。
- **补图规则**：图片少于 5 张时，优先补剧情转折点/动作变化点/punchline；补完必须同步更新 JSON 的 `segments[].image` 映射，不得生成了但页面没引用。

## 3. 数据完整性与教材对齐

- **台词校验**：对照 `.lrc` 文件，确保对话片段 100% 完整。
- **角色映射**：查阅教材插图确认性别/年龄/人数，通过录音音色双重验证。
- **性别强锚（教训：L75）**：写 `CHAR_*` 前先听录音确认性别，不可凭情境猜测。必须在 `CHAR_*` 写 `CRITICAL: MALE/FEMALE`，并在每个含该角色的 `desc` 里重复 `is a MAN / is a WOMAN`。

## 4. 课程验收标准

1. **物理一致性**：Scene 2+ 与 Scene 1 的发型、服装、场景色调完全相同；严禁"变装"或"变脸"。
2. **叙事对齐**：每帧画面与该时间点台词的剧情位置一致，不提前剧透，不跳跃。
3. **语义匹配**：画面直观呈现 Segment 核心动词（摇头、递物、指向等）。
4. **环境纯净度**：画面无文字、字幕、对话气泡、漫画分栏。
5. **JSON 有效性**：中文翻译地道，JSON 结构合规（`jq .` 验证）。

## 5. 交付自检流程

生成完成后必须用 `Read` 工具逐帧查看每张 PNG，确认：
- [ ] 叙事节点正确：每帧画面与对应台词的故事进度一致，无剧透。
- [ ] 角色一致性：全课发型/服装/年龄无漂移，无重复人物。
- [ ] 场景正确：每帧位于正确的物理空间（客厅/卧室等）。
- [ ] 无文字污染：图面无任何字符。
- [ ] JSON 图片映射完整：`实际图片数 >= 5`，`实际图片数 = JSON 引用数`。
- [ ] `jq .` 语法校验通过。

**若发现问题**：修改 desc 加强约束 → 重新生成 → 再次查看，直到合格。禁止带已知错误交付。

## 6. 图片继承机制（LessonView）

- **无 `image` 字段的 segment**：回溯最近一个有图的 segment 继续显示，不跳回根图。
- **根图**：仅在音轨开始、尚未到达第一个有图 segment 之前作为默认背景。
- **验收核查**：统计每张图实际显示时长，单张超过 30% 说明有段落未映射，需补 `image` 字段。

## 7. Git 规则

- 始终在 `main` 分支直接工作，及时提交。
