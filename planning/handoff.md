# 私有仓库交接与Pages部署准备

仓库：HNNUYUXUAN/FactorizationTeaching。源代码与内容源均保留。网站目录为docs/，无需构建或后端。接收人可本地双击docs/index.html使用。

## 接收账号发布

1. 克隆本私有仓库，或取得本地完整目录。
2. 在接收账号建立目标仓库，以该账号的凭据推送；根据该账号Pages可用条件选择仓库可见性。
3. 在目标仓库Settings → Pages选择从分支部署，main分支、/docs目录。
4. 发布后检查四个资料入口、课件图片与PPTX下载、板书前后步骤与终局打印。

本仓库不包含启用状态的部署工作流，不在HNNUYUXUAN账号启用Pages，不自动邀请协作者或转移仓库。

## 内容修改

练习编号以 `exercises/L01-exercises.md` 为准，时间表以 `planning/alignment-and-plan.md` 为准。v3 可见文案和插图说明见 `slides/L01-api-v3.json`。变更页面后重新出候选，逐字、逐符号检查，再更新 PPTX、HTML 和备注。 `scripts/build_site.py` 可从已定稿内容重建网页。

## 生图恢复

`scripts/generate_images.py` 读取本机 Windows 已配置的 `openai-next-image` 渠道，自动复用系统代理。生成候选和记录在 `work/image-v3/`，已核对的候选记录和提示词随版本归档。接收账号重新出图时配置自己的渠道，既有网页和 PPTX 可直接离线使用。
