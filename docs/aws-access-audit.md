# 三个人能否分别登录同一课程 Lab：检查结果

检查日期：2026-10-31，Australia/Sydney。本人登录后，由 AI 只读查看该 Lab 实际说明，并通过其 AWS 按钮进入控制台。

**结论：这份 Learner Lab 明确禁止创建用户或组，不能采用“新建两位组员的 IAM 用户及密码”方案。未创建账号、密码或更改权限。**

## 实际依据

- 来源：[已登录课程的 Launch Lab](https://awsacademy.instructure.com/courses/188838/modules/items/18668931)，Vocareum Readme，ZH-CN，说明更新时间 2025-06-24。
- “AWS Identity and Access Management (AWS IAM)”段落原文：“受到极度限制的访问。不能创建用户或组。您可以创建服务相关的角色，但除此之外的角色，您均不能创建。”
- 同段说明已预置 LabRole；EC2 可通过 LabInstanceProfile 使用它。这是服务访问 AWS 的机制，不能当作组员登录账号。
- Lab 显示 Ready；通过 AWS 按钮成功进入 Console Home，区域 us-east-1。
- 检查时显示 Used $1.2 of $50，界面剩余约 $48.80。该数字有延迟，不代表本次架构的实测成本。

## 结论的边界

依据是当前 Lab 自身的限制说明；未调用 CreateUser 作失败实验，没有声称取得实际 API 拒绝日志。不通过创建用户或其他身份路线试探或绕过明确限制。

课程是否另有教师配置的小组环境或独立访问入口，仍需 tutor 确认。结论仅针对当前个人 Learner Lab。

未盘点旧 EC2/S3/数据，未验证应用、两个 AZ、HTTPS、资源级权限和架构预算，T05 仍未完成。没有读取 AWS Details、提取临时凭证、Reset、End Lab、删除资源或启动部署。

## 当前协作方式

1. 这份 Lab 可作为集成候选环境；正式持有人与部署负责人由三人会议确认。
2. A 准备网络和部署配置，B 准备应用和数据代码，C 准备测试、监控和证据，三人并行提交 GitHub。
3. 另一人检查改动后，由获准的环境持有人执行；共享屏幕时区分实际操作者、指导者和检查者。
4. 记录 commit、步骤、日志/截图、测试结果，再上报任务回执。
5. 由真人询问 tutor：是否提供三人各自身份访问同一环境的课程方案？收到真实答复再更新计划。暂不交换个人密码、密钥或会话 token。

操作流程见 [shared-aws.md](shared-aws.md)。
