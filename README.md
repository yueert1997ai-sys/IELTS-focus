# IELTS Focus v4.0

完整的 S3 Focus 训练网站。桌面和手机使用同一份响应式页面。

## 版本与内容

唯一母版：`s3-focus-v4.0-natural-tts.html`，391765 字节。

- 压缩训练：140 道单选、15 组匹配。
- 选项上膛：20 个主题，80 道单选、20 组五选二、80 道匹配小题，共 200 个得分点。
- 保留动作建立、连续迁移、完整讨论、难度选择、文字高亮、复盘与导入导出。
- 使用浏览器系统英文语音，无外部神经音频链接。
- 无登录、无 Supabase、无云同步。记录分别保存在各设备的浏览器中。
- 原创练习内容及合成声音未经 IELTS 官方难度校准。

## 完整性

上传采用无损 XZ 分片，未删改题目。工作流先用 Python 标准库还原，核对每片哈希、完整文件 SHA-256、题目数量和 JavaScript 语法，再把普通完整 `index.html` 提交至 main 并发布。

SHA-256：`4921cab4583ae861b073f6eb9eda5d07244e6c887f41ff96744450893228a1f6`

本地重新还原：在仓库根目录执行 `python3 scripts/restore.py`（需要 Python 3 和 Node.js）。浏览器只使用还原后的 HTML，不需要解压程序或后端。

旧 Lite 的 `app.js / data.js / style.css` 已由恢复流程移除；历史提交仍保留，不改写 Git 历史。

## 访问

部署目标：https://yueert1997ai-sys.github.io/IELTS-focus/

Pages 首次开通需要仓库管理者在 Settings → Pages 选择 GitHub Actions，再在 Actions 运行此部署流程。文件入库和网站正式发布是两个不同状态，请以 Actions 的 deploy 成功为准。

iPhone 使用 Safari 打开上线后的网址，可通过分享菜单添加到主屏幕。不同设备进度不互通；不要使用无痕窗口保存长期记录。

## 测试

完整母版在 Chromium 桌面与 390px 触屏布局下通过 36 项交互测试，3 个脚本语法检查通过。交互测试的语音引擎为模拟对象；真实设备的发声与音色仍需通过站内试听确认，未声称完成实机 iPhone 音频验收。
