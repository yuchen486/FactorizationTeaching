# 私有仓库交接与Pages部署准备

仓库：HNNUYUXUAN/FactorizationTeaching。源代码与内容源均保留。网站目录为docs/，无需构建或后端。接收人可本地双击docs/index.html使用。

## 接收账号发布

1. 克隆本私有仓库，或取得本地完整目录。
2. 在接收账号建立目标仓库，以该账号的凭据推送；根据该账号Pages可用条件选择仓库可见性。
3. 在目标仓库Settings → Pages选择从分支部署，main分支、/docs目录。
4. 发布后检查四个资料入口、课件图片与PPTX下载、板书前后步骤与终局打印。

本仓库不包含启用状态的部署工作流，不在HNNUYUXUAN账号启用Pages，不自动邀请协作者或转移仓库。

## 内容修改

练习编号以exercises/L01-exercises.md为准，时间表以planning/alignment-and-plan.md为准。修改时同步逐字稿、分镜、板书与网页。图片文案修改应重新生成相关整图并更新SHA与PPTX。scripts/build_site.py由现有内容重建网页，scripts/prepare_content.py会重写内容源，应修改该程序中的内容后再运行。

## 生图恢复

scripts/generate_images.py读取当前Windows用户new-api数据库中已配置的openai-next-image渠道；密钥只在内存及curl标准输入中使用。接收账号需自行配置同名渠道后才可重新生图。已有图像、网页和PPTX可直接使用，不需要API密钥。自动跳过已有图片；返回非零时查看非密钥日志及缺图页。不得上传数据库、密钥或原始认证信息。
