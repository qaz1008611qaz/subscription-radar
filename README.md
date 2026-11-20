# 订阅雷达 Subscription Radar
上传账单 / 截图 / 邮件 → 自动识别订阅 → 续费前 3 天提醒。
由 Devin Bot 协作开发，7 天交付第一版。

## 技术栈
- 后端：Python 3.11 + FastAPI + SQLite
- 解析：pdfplumber（PDF）、PaddleOCR（截图）、邮件转发解析
- 前端：Next.js
- 提醒：定时任务 + 邮件 / Telegram

## 排期
- Day 1-2：解析流程 + 样本测试
- Day 3-4：订阅识别
- Day 5：续费提醒
- Day 6-7：界面、部署、公开
