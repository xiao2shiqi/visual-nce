# 项目规则

> **Language note**: Please always use simple English. I am learning English.

## 1. 生图管线（Antigravity 编辑模式，2026-07-04 定稿）

### 1.1 通道

生图统一走 **Antigravity CLI（`agy`）**：Google 账号 OAuth + AI Pro 会员额度，无需 API key。
（历史备注：Gemini API key 与 Gemini CLI OAuth 均因账号区域限制不可用，勿再尝试。）

非交互调用（cwd 必须设为课程图片目录，如 `public/images/nce1/l137/`）：

```bash
agy --add-dir . --dangerously-skip-permissions --print-timeout 8m -p "<prompt>"
```

### 1.2 核心原理：编辑，不要文生图

一致性的关键是让模型**看到锚点图的像素**，而不是读它的文字描述。所以除每课第一张外，一律用「图像编辑」：

```text
CRITICAL: image EDITING task. Pass <anchor>.webp (current directory) as an
INPUT IMAGE to your image editing tool so the model sees the pixels.
Output MUST keep the exact same wide landscape framing as the input.

Edit instruction: keep the painting exactly as it is — same <场景要素清单>,
same <人物名 + 发型 + 服装>, same watercolor style. Make ONLY these changes:
1) ... 2) ... 3) ...  NO text or letters anywhere.

Save as <frame_id>.png in the current directory.
```

要点：
- 「keep exactly as it is + Make ONLY these changes」是固定句式，改动列表越少越稳。
- 锚点选择：默认 `scene1`；**连续剧情帧用上一帧作锚点**（链式编辑，背景道具能跨帧延续，见 L143 垃圾场三连）；回到旧场景就换回该场景的锚点。
- 整课重画 / 新课：先用文生图出 `scene1`（宽幅横版，含完整人物定义），验收合格后再链式编辑其余帧。电话戏等双场景课用分屏构图（见 L139 scene1）。
- **换人修正（见 L141 爷爷→妈妈）**：某个角色画错时不必整课重画——对每帧做「REPLACE X with Y, keep everything else」的换人编辑。跨帧脸部一致的做法：先换 scene1，后续帧**同时传两张图**——原帧作 BASE image to edit + 换好人的 scene1 作 IDENTITY REFERENCE for the face/hair/clothing。
- 实测效果：房间与人物近乎零漂移，L137/L141/L143 共 10 帧全部一次通过。

### 1.3 已知的坑（每条都踩过）

1. **scratch 目录**：agy 常把输出存到 `~/.gemini/antigravity-cli/scratch/` 而不是 cwd，每帧跑完必须检查并拷回。
2. **假文件**：额度耗尽时 agy 可能把输入图复制成输出文件名——**字节数与锚点图完全相同即为假文件**，入库前必须比对（`ls -la` 看 size 或哈希）。
3. **额度锁**：连续生成会触发约 4.5 小时的 quota lock（Max 一晚约可出 10+ 帧）。批量任务要按课分批，锁了就记录进度等重置。
4. **方图**：偶发输出 1024x1024 正方形，播放器会裁掉顶部（气泡最常受害）。prompt 里必须带 `keep the exact same wide landscape framing`；出图后校验尺寸应为 1376x768。
5. **格式**：输出为 PNG，入库前转 WebP（`PIL: quality=82, method=6`），命名 `<frame_id>.webp`。

### 1.4 单课工作流（强制顺序）

1. **通读全课台词**（课程 JSON 的 segments），先判断现有图讲的是不是这个故事——叙事错位比风格漂移更常见也更致命（L139 整课画错故事、L143 悲伤台词配赏花图，都是这么漏掉的）。
2. 设计分镜：每课 ≥5 帧，优先覆盖剧情转折点 / 动作变化点 / punchline。
3. 按 §1.2 生成，逐帧用 Read 工具查看验收（标准见 §4）。
4. 转 WebP 入库，**同步更新课程 JSON 的 `segments[].image` 映射**，删除不再引用的旧图。
5. 校验：JSON 里每个图片引用的文件都存在；`jq .` 语法通过。
6. Git 提交。

参考实现：`scripts/nce1/generate_l137_storyboard.py`（含 L137 实际使用的四段编辑指令）。

## 2. 视觉风格与 Prompt 规格（强制性）

- **视觉风格**：带水彩质感的吉卜力工作室（Studio Ghibli）插画风格。严禁写实、3D 渲染或非吉卜力风格。
- **Master Specs（物理强锚定）**：每课的人物与场景定义要完整写进 prompt——
  - 人物：发型（色/长/款）、上装（色/领/袖/饰）、下装、特定配饰，附 `CRITICAL: MALE/FEMALE`。
  - 场景：物理边界（如：严格在厨房内）、主色调、核心地标；需要排他时写 `Strictly in [A], NO [B]`。
- **环境纯净度**：每帧 prompt 必须包含 `NO text or letters anywhere`（思想气泡允许，气泡内不得有文字；剧情需要的招牌一律画成空白风化的牌面）。
- **叙事剧透防护（教训：L13）**：scene1 不得提前展示故事中计划揭秘的道具；每帧只反映角色此刻的剧情位置。
- **人物复制防护（教训：L81）**：两个同性别角色同帧时加三层约束：`STRICTLY N INDIVIDUALS ONLY. Do NOT duplicate any character.` + 逐人指定位置外貌 + `These are DIFFERENT people`。气泡内出现「同一人物的幻想形象」时反向声明 same face and hair as the person below（见 L137 貂皮帧）。
- **封面图同步**：`scene1` 同时用于 `curriculum.json`（缩略图 `thumb.webp`）和课程 JSON 的根 `image` 字段。

## 3. 数据完整性与教材对齐

- **台词校验**：对照 `.lrc` 文件，确保对话片段 100% 完整。
- **角色映射**：查阅教材插图确认性别/年龄/人数，通过录音音色双重验证。
- **性别强锚（教训：L75、L141）**：写人物定义前先以录音音色确认性别，不可凭情境猜测，也不可默认沿用旧图的设定（L141 的旧图把妈妈画成了老爷爷，重绘时沿用导致返工）。**AI 无法听录音，叙述者性别不明时必须先问领导，不许猜。**

## 4. 课程验收标准

1. **物理一致性**：Scene 2+ 与锚点帧的发型、服装、场景色调完全相同；严禁"变装"或"变脸"。
2. **叙事对齐**：每帧画面与该时间点台词的剧情位置一致，不提前剧透，不跳跃；**整课图讲的必须是课文的故事**。
3. **语义匹配**：画面直观呈现 Segment 核心动词（摇头、递物、指向等）；课文里的关键名词要画出来（L143 的 7 辆旧车 3 台冰箱、L141 的 blue coat + large funny hat）。
4. **环境纯净度**：画面无文字、字幕、带字对话气泡、漫画分栏。
5. **JSON 有效性**：中文翻译地道，JSON 结构合规（`jq .` 验证）。

## 5. 交付自检流程

生成完成后必须用 `Read` 工具逐帧查看，确认：
- [ ] 叙事节点正确：每帧画面与对应台词的故事进度一致，无剧透。
- [ ] 角色一致性：全课发型/服装/年龄无漂移，无重复人物。
- [ ] 场景正确：每帧位于正确的物理空间。
- [ ] 无文字污染：图面无任何字符。
- [ ] 尺寸为 1376x768 横幅（非方图），字节数与锚点图不同（防假文件）。
- [ ] JSON 图片映射完整：`实际图片数 >= 5`，每个引用的文件都存在，无未引用的废图。

**若发现问题**：修改编辑指令加强约束 → 重新生成 → 再次查看，直到合格。禁止带已知错误交付。

## 6. 图片继承机制（LessonView）

- **无 `image` 字段的 segment**：回溯最近一个有图的 segment 继续显示，不跳回根图。
- **根图**：仅在音轨开始、尚未到达第一个有图 segment 之前作为默认背景。
- **验收核查**：统计每张图实际显示时长，单张超过 30% 说明有段落未映射，需补 `image` 字段。

## 7. Git 规则

- 始终在 `main` 分支直接工作，及时提交。
