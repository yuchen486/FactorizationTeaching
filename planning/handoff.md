# 公开维护与 Pages 部署

公开仓库：[yuchen486/FactorizationTeaching](https://github.com/yuchen486/FactorizationTeaching)。网站目录为 `docs/`，不需要构建步骤或后端；本地可直接打开 `docs/index.html` 使用全部资料。

## 发布方式

`.github/workflows/pages.yml` 会在 `main` 分支的站点或工作流变更后，将 `docs/` 部署到 GitHub Pages。发布地址为：

`https://yuchen486.github.io/FactorizationTeaching/`

发布后应检查首页、逐字稿、教案、板书与课件入口，以及课件图片、PPTX 下载、板书步骤和终局打印。

## 内容修改

练习编号以 `exercises/L01-exercises.md` 为准，时间表以 `planning/alignment-and-plan.md` 为准。v3 可见文案和插图说明见 `slides/L01-api-v3.json`。变更页面后重新出候选，逐字、逐符号检查，再更新 PPTX、HTML 和备注。`scripts/build_site.py` 可从已定稿内容重建网页。

## 图像再生成

`scripts/generate_images.py` 使用本机 Windows 的 `openai-next-image` 渠道和系统代理。候选与生成记录保存在 `work/image-v3/`，本版的候选、提示词和验收记录随版本归档。离线使用既有 PPTX 和网页无需服务凭据。
