# 公开维护与 Pages 部署

公开仓库：[yuchen486/FactorizationTeaching](https://github.com/yuchen486/FactorizationTeaching)。网站目录为 `docs/`，不需要构建步骤或后端；本地可直接打开 `docs/index.html` 使用全部资料。

## 发布方式

`.github/workflows/pages.yml` 会在 `main` 分支的站点或工作流变更后，将 `docs/` 部署到 GitHub Pages。发布地址为：

`https://yuchen486.github.io/FactorizationTeaching/`

发布后应检查首页、逐字稿、教案、板书与课件入口，以及课件图片、PPTX 下载、板书步骤和终局打印。

## 内容修改

练习编号以exercises/L01-exercises.md为准，时间表以planning/alignment-and-plan.md为准。修改时同步逐字稿、分镜、板书与网页。图片文案修改应重新生成相关整图并更新SHA与PPTX。scripts/build_site.py由现有内容重建网页，scripts/prepare_content.py会重写内容源，应修改该程序中的内容后再运行。

## 图像再生成

`scripts/generate_images.py` 需要调用方自行配置图像服务；已有图像、网页和 PPTX 可直接使用，不需要 API 密钥。不得提交数据库、密钥或原始认证信息。
