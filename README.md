# 因式分解 · 十分钟课堂

[English](README.en.md) · [在线体验](https://yuchen486.github.io/FactorizationTeaching/)

![因式分解十分钟课堂的静态站点首页](assets/pages-overview.png)

面向师范生教学方法课程的完整教学资源包。项目参照淮北市现行沪科版七年级下册 8.4，围绕“因式分解——提公因式法入门”设计 600 秒无生试讲，并提供可离线使用的逐字稿、教案、板书、课件与练习。

## 使用入口

- [GitHub Pages 在线站点](https://yuchen486.github.io/FactorizationTeaching/)
- 本地直接打开 [docs/index.html](docs/index.html)，无需构建或后端服务
- [教学来源与核验状态](references/sources.md)

|资料|可编辑源文件|阅读或展示入口|
|---|---|---|
|逐字稿|[Markdown](lesson-plans/L01-script.md)|[阅读打印](docs/script.html)|
|教学设计|[教案](lesson-plans/L01-lesson-plan.md)|[阅读打印](docs/lesson.html)|
|板书|[SVG](board-design/L01-board.svg)|[逐步板书](docs/board.html)|
|课件|[文案](slides/pages.json)、[提示词](slides/prompts/)|[HTML 课件](docs/slides.html)、[PPTX](outputs/L01-课件.pptx)|
|练习|[题目与答案](exercises/L01-exercises.md)|E01—E05 课堂练习，E06 课后练习|

## 仓库结构

- `docs/`：GitHub Pages 直接发布的静态站点
- `lesson-plans/`、`board-design/`、`slides/`、`exercises/`：教学材料与可编辑源文件
- `assets/`、`outputs/`：课件图片和已验收成品
- `scripts/`：内容构建与核验脚本；`work/` 为 Git 忽略的本地临时目录

学生回答均为预设，实际授课时长请结合排练调整。教材仅用于教学范围与结构参照；本站不附教材整册文件。

## 署名与许可

原作者：[HNNUYUXUAN / Yuxuan Miao](https://github.com/HNNUYUXUAN)。公开仓库由 [yuchen486](https://github.com/yuchen486) 维护。

本仓库以 [CC BY-NC-SA 4.0](LICENSE) 许可发布：使用或改编时须署名、限非商业用途，并以相同方式共享。
