# 教学使用与二次改编 / Teaching and adaptation

这套资源对应七年级下册因式分解入门，主题是提公因式法。讲授按整系数多项式组织。15 屏合计 600 秒，包含停顿、板书和翻页。面向师范生无生试讲与中学数学备课。

## 中文

**直接使用。** 在线打开[教学站](https://yuchen486.github.io/FactorizationTeaching/)，或克隆仓库后双击 [docs/index.html](docs/index.html)。教案和逐字稿可打印，分步板书可推进、回退、重置和打印终局。课件可按方向键翻页，按 F 全屏，按 H 切换投影控件。[PPTX](outputs/L01-课件.pptx) 的每页是一张整图，教师备注单独保存。

**改编顺序。**

1. 以[练习 E01–E06](exercises/L01-exercises.md)为题目与答案的来源，以[时间轴](planning/alignment-and-plan.md)为节奏依据，再对照[教案](lesson-plans/L01-lesson-plan.md)、[逐字稿](lesson-plans/L01-script.md)和[讲者提示卡](outputs/L01-提示卡.md)。
2. 按稳定页面 ID 更新[页面内容](slides/pages.json)以及[可见文案和插图方案](slides/L01-api-v3.json)。画面与讲者备注分开保管。答题页先留出思考时间，反馈页再显示答案。变更板书时同步[动作说明](board-design/L01-board-plan.md)和[网页生成脚本](scripts/build_site.py)里的板书条目，该脚本也输出 [SVG](board-design/L01-board.svg)。
3. 将验收后的 16:9 PNG 放到 `assets/slides/`，沿用页面 ID 命名。在 PowerPoint 或兼容编辑器中用同一张图更新对应页，并同步备注。检查平方上标、正负号、括号和错例标记，再核对 [PPTX](outputs/L01-课件.pptx) 与 [HTML](docs/slides.html) 的页序和题面。
4. 从仓库根目录执行 `python scripts/build_site.py` 重建网页。脚本使用 Python 3.10+ 标准库，沿用当前 PNG 和 PPTX。部署时发布整个 `docs/`，保留相对路径。可在无凭据环境中预览并复用已交付资源。

**Agent 协作。** 先读 [llms.txt](llms.txt) 和 [AGENTS.md](AGENTS.md)，再按上面的权威文件查证题面、节奏与输出。请标明已验证事实和预设学生反馈。交付前核对页序、每页秒数、等式展开和素材引用。

**署名与许可。** 转载或改编时保留作者 HNNUYUXUAN / Yuxuan Miao，链接原仓库和 [CC BY-NC-SA 4.0](LICENSE)，注明改动并按相同条件共享。教材用于确定教学范围，引用来源见[来源说明](references/sources.md)。第三方标识与素材请按其权利说明使用。

## English

**Use the lesson.** Open the [live site](https://yuchen486.github.io/FactorizationTeaching/) or open [docs/index.html](docs/index.html) from a clone. The Chinese-language package covers greatest-common-factor extraction for grade 7. It has 15 slide states and a 600-second rehearsal budget. You can print the script and lesson plan, step through the board, and navigate slides with the arrow keys. Use F for fullscreen and H to toggle the controls. Each PowerPoint slide contains one complete image and separate speaker notes.

**Adapt the lesson.** Start with the [exercise and answer source](exercises/L01-exercises.md) and [timing plan](planning/alignment-and-plan.md). Keep the [script](lesson-plans/L01-script.md), [speaker cards](outputs/L01-提示卡.md), [slide data](slides/pages.json), [visual copy](slides/L01-api-v3.json) and [board plan](board-design/L01-board-plan.md) aligned by page and exercise ID. Update the board items in [the site builder](scripts/build_site.py) when changing the board. Use reviewed 16:9 PNGs in `assets/slides/` and the same images in the [PowerPoint](outputs/L01-课件.pptx). Check exponents, signs, parentheses, the explicitly marked incorrect example, and the distinction between questions and feedback.

Run `python scripts/build_site.py` at the repository root to rebuild the website with Python 3.10+ and its standard library. It repackages the existing PNG and PPTX assets. Publish the entire `docs/` directory and keep relative paths intact. The shipped materials work offline without service credentials.

**For agents.** Start with [llms.txt](llms.txt) and [AGENTS.md](AGENTS.md), then use the sources above for lesson facts and update rules. Treat proposed learner responses as scripted examples. Confirm page order, planned timing, math notation and asset links before handing off changes.

**Attribution.** Credit HNNUYUXUAN / Yuxuan Miao, link to the original repository and [CC BY-NC-SA 4.0](LICENSE), describe adaptations and share under the same terms. See [source notes](references/sources.md) for textbook references. Use third-party marks and materials under their applicable terms.
