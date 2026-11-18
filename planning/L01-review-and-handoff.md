# L01 规范化方案本地更新交接

> 本文保留更新前的交接背景。当前的 15 页课件与资料入口见 [交付索引](../outputs/README.md)。

## 现状

本轮检查确认，原PPT详细设计已有课前导入 S01A/B、课堂归纳 S07A/B，但**没有独立的课后作业页**，E06只在结束话术中口头布置。

## 下一版要求

新增课后作业 S08A（15秒），在 S04B 减少15秒，总计从14个课内状态变为15个，总时长仍600秒。E06题目为 `10m²n－15mn²`，作业页不能显示 `5mn(2m－3n)` 的答案。可选择另做一个正式计时前的待机封面 S00，但其时间不计入600秒。

## 推荐放入仓库的文件

- `slides/L01-detailed-design-v2.md`：本目录 `L01_PPT详细设计_v2_15状态含作业页.md` 的完整文本。
- `planning/L01-review-and-handoff.md`：本交接说明。

**不要在本轮只修改设计稿就声明 PPT 已更新**：现有 `slides/pages.json`、PPTX、HTML 及图片资源和验收清单还是14状态旧版。制作时按设计稿同步修改它们。

## 本地提交命令（将文件放入上述仓库路径之后）

```bash
git add slides/L01-detailed-design-v2.md planning/L01-review-and-handoff.md
git commit -m "docs: specify intro summary and homework slide for L01"
git push origin main
```

本轮通过ChatGPT的GitHub连接尝试写入，GitHub返回403 Resource not accessible by integration，故远端没有新增commit。
