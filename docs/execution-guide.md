# Three people completing a cloud service together: execution manual

INFS3701 cloud architecture and AWS practice | Drawn up 2026-10-31 | All dates are Sydney time

For the latest schedule, handoffs and single-person AWS operation arrangements see [parallel-plan.md](parallel-plan.md); where they differ, that plan and the latest task cards prevail. This is an execution draft that can be taken to tonight's meeting to divide the work. Upgrading the user's own Reading Tracker is now confirmed; member names, the database and permissions still need confirming at the first meeting. The AWS project is not yet actually deployed; the private GitHub collaboration hub and task cards are set up, and the current way of operating is in the README and docs/system-status.md. The code entry point is app/reading_tracker.py, using Option A.

The formal brief deadline is **2026-11-17 16:00**; dates below such as 3 Nov and 6 Nov are suggested internal milestones. The goal is a submittable version by 16 Nov. The official evidence is the INFS3701 assignment brief and marking sheet in `source_materials/INFS3701/03_assessments/group_assessment/`; the earlier meeting outline has been worked through item by item.

## 1. What we finally build

Keep a small, usable reading-record web page: add records, view records, show statistics. Upgrade the system behind it to:

`User's browser → single entry point (load balancer) → two application servers in different Availability Zones → one shared managed database`

Plus a monitoring page to observe how it is running and an alarm that can really be triggered. An Availability Zone can be understood as a separate data-centre area within the same region; stateless means important data cannot live only in one application server's memory or local files.

First get "still available when one fails, two servers read and write the same data, with alarm evidence" right. A new account system, recommendation algorithms, complex interfaces and the like are left out of scope for now. Whether there are real users and real traffic must be stated honestly; test concurrency can be used as a design assumption, but user scale must not be invented.

**Draft selection:** continue with Flask + two EC2 + Application Load Balancer; for the database first compare DynamoDB and Multi-AZ RDS. If it is only small independent book records, the DynamoDB route can be verified first; if course labs, query needs or permissions suit a relational database better, choose Multi-AZ RDS. The choice is not a price conclusion; it finally rests on requirements, operability, permissions and the calculator estimate.

## 2. The three people's responsibilities

| Code | Suggested person | Main responsibility | What must be handed to the others |
| --- | --- | --- | --- |
| A | You (DiegoXue-coder) | Network, servers, single entry point, deployment environment | A reachable address, resource configuration, deployment steps, architecture diagram |
| B | Member two | Web back end, database read/write, both servers running the same version | Runnable code, data fields, start method, feature demo |
| C | Member three | Monitoring, testing, evidence, cost estimate, video integration | Test results, alarm evidence, estimate, video draft |

Being responsible does not mean doing it all alone: A's deployment needs B's code; C's testing needs A/B's cooperation. Everyone writes their own design reasons, steps and limitations, and the whole report is not dumped on C. A finally integrates the architecture, B the report, and C the video and evidence; the three cross-check.

Divide the work by the codes above first and write the names on the task board tonight. Adjust for free time, and do not presume the three people's actual contributions are equal.

## 3. How the time runs and what can be done at the same time

| Time | A at the same time | B at the same time | C at the same time | What to have at the end of the stage |
| --- | --- | --- | --- | --- |
| 31 Oct | Jointly settle the topic, confirm permissions/balance | Jointly confirm whether the old code can be reproduced | Jointly set up the task board, record questions to ask | Project, owners, collaboration location and first integration time settled |
| 1–3 Nov | Verify network/servers, HTTPS and lab permissions | Settle the database, get the single-instance application working | Test checklist, report skeleton, cost assumptions | First version of the application can write new records to the managed database |
| 4–6 Nov | Connect the single entry point and the second server | Get both running the same code version, sharing data | Check read/write on both, build the monitoring page | Single entry point usable, both healthy, data shared |
| 7–10 Nov | Help with failure testing, security checks and the chosen enhancement | Fix test problems, organise reproduction steps | Measure the alarm, record failure and routing, calculate the formal cost | Every core requirement has evidence; decide whether to complete the enhancement |
| 11–13 Nov | Finalise the architecture diagram and network chapter | Integrate the report, others reproduce by the steps | Joint recording, edit the video, finalise the cost | First drafts of all five deliverables complete |
| 14–16 Nov | Check the deployment against the diagram | Check text, code, references | Check the video, evidence, file completeness | A submittable version signed off by everyone |
| Before 17 Nov 16:00 | Designated submitter uploads | Check content and that files open | Save the submission receipt | Formal submission complete |

Dates are only available windows and do not mean everyone is online all day every day. Each person schedules independent work; four joint checks of about 30–45 minutes are suggested on 3, 6, 10 and 13 Nov; set the actual times tonight from the three timetables.

### Order of joint completion (independent preparation can start early)

On 2026-10-31 the actual task cards were changed to two gates, "start preparation" and "complete acceptance"; the details are in [parallel-plan.md](parallel-plan.md) and the latest Issues. The order below describes real integration results and does not mean the next member must wait for the previous one to finish everything before starting.

1. Settle the service and database direction → write down the data fields and start convention.
2. The application works with the database → both application hosts run the same version.
3. The network and both application hosts are ready → connect the single entry point and test jointly.
4. The joint system works → measure routing, stopping one host, and the alarm.
5. Tests pass and evidence is saved → record the real-operation video and finalise documents.
6. All three check and sign → submit → clean up resources according to the confirmed acceptance arrangement.

**Can be done early:** report outline, first architecture draft, test scripts, cost assumptions, video script and deployment document, from day one. **Can only be finished with real results:** the actual failure conclusion, final cost, final architecture diagram and real demo video. An experiment that stops one server cannot be written up as a fully measured AZ failure.

## 4. How to do each step

Task numbers, live owners and acceptance are detailed in the [GitHub task cards](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues) and `DASHBOARD.md` in the root. The operating order below is the team's workflow and does not assume the lab has every AWS permission.

### Step 1: write down the joint agreements tonight (T01–T03)

The starting service is confirmed as Reading Tracker, with no reselection of topic. Write in one sentence "who uses it, what it does, and why it should not go down". Confirm which Learner Lab is used for the final demo and note the remaining credit. C organises and asks the tutor: video length, whether auto scaling is mandatory, whether teardown is allowed after evidence collection, and how several members should obtain permitted lab access.

A creates the private code repository and invites the other two under course rules; C sets up the task board with owners, start dates, target dates and prerequisite tasks; B uploads the cleaned-up application code and dependency list. Do not upload the whole study-materials directory to the repository.

**Handoff:** C records the meeting conclusions in `collaboration_starter/docs/decisions.md`; the three confirm, and later changes are recorded here too.

### Step 2: first agree how the code connects (T04)

B writes a short agreement; after A/C review it, work proceeds in parallel:

- Which features the page keeps, and what result a test insert should produce.
- Data fields, for example `record_id`, `title`, `status`, `pages_read`, `total_pages`, `rating`, `created_at`; the primary key uses an ID that will not easily collide on simultaneous submissions.
- Configuration goes in environment variables, such as region, table name and server label; access keys must not be written in the code.
- Provide `/health` for the load balancer to judge whether the application has started, returning 200 when the process can respond; data-tier read/write gets a separate functional test. Do not treat "the process is alive" as "the database is definitely available".
- For example, standardise the application port as `8000` and a single start entry point; add the exact command to `docs/deploy.md` once dependencies and file names are settled. The two machines must be identical, and the Flask development server is not used as the final deployment method.
- 页面或日志显示简短的 `APP_INSTANCE_LABEL` 和代码版本标识，便于演示请求来自不同实例；不要在界面暴露密钥、完整配置或敏感内部信息。

**为什么现在约定：**A 不必等全部功能完成才搭服务器，C 不必等系统上线才写测试。

### 第三步：A 搭基础环境，B 改应用，C 准备检查（T05–T08，并行）

**A：**进入 Learner Lab 后先确认 us-east-1、余额和允许使用的角色。检查能否用两个 AZ、负载均衡、托管数据库、监控和 HTTPS 所需资源。画出 VPC 中每个 AZ 的公有/私有子网、入口、应用及数据路径。确认私有应用怎样访问数据库、下载依赖以及如何维护，再创建最小可测环境；出口或 endpoint 若收费，要记入成本。私有子网里的程序无法下载依赖时，不能只靠反复重启解决，要检查路径。

HTTPS 从第一阶段就验证域名/证书/实验室权限是否可行，不等录视频时才发现不能配置。若受限，保留错误并问 tutor，不画出并未实现的 HTTPS。RDS 路线还需配置独立数据库安全组、跨 AZ 能力和凭证管理；DynamoDB 路线需确认应用角色及访问路径。

**B：**先在自己的开发环境复现旧应用，再把存取数据的代码单独整理，迁到选定数据库。按“创建测试记录 → 查回记录 → 刷新后仍在 → 重启应用后仍在”验证。用 UUID 等唯一标识避免旧代码按秒时间戳加标题导致同秒同名记录覆盖。数据不要只写在本地 JSON 文件；测试使用虚构书籍记录，不导入私人信息。

若 B 无最终环境操作权限，B 提交代码与数据库创建步骤，由 A 在共享屏幕时执行；B 负责指导、解释及核验结果。开发可使用允许的本地替代方式或自己的 Lab，但最终证据来自同一套集成系统。

**C：**先写测试步骤和证据表，列明负载分发、数据共享、故障、告警、安全核对分别怎么验收。准备报告标题、成本表的项目与流量假设、60 秒视频脚本。不要等待截图齐了才开始想要证明什么。

**11/3 检查门槛：**A 能展示环境草图和权限结果；B 能演示一次真实数据库写入及读取；C 有测试表。如果其中一项失败，先解决它，暂不做增强。

### 第四步：把两个应用接到一个入口（T09–T12）

A 按双 AZ 设计创建两个实例，部署 B 已复核的同一个提交版本；不是分别手工修改两台服务器代码。配置目标组（可理解为负载均衡器的服务器名单）、应用端口和健康检查地址，确认两台健康后再通过统一入口访问。应用入站只允许必要来源，不能为了调试长期开放所有端口。

B 在这个入口添加一条记录，验证另一个实例也能读到；检查会话或临时文件是否让用户换服务器就丢数据。部署结果记下代码提交编号和配置，不只记一个网址。

C 发一组小规模、间隔合理的请求，保留时间、响应状态和实例标签。连接复用可能让连续几次请求来自同一台，不要求每次轮流；要有足够结果证明两台都处理过。数据读回若采用最终一致读取，测试应明确预期和等待方式，不能把一切短暂延迟都归为故障。

**11/6 检查门槛：**三人都能通过同一个地址使用功能；两台健康；两台看到相同持久数据；图上每个主要组件都能对应到资源清单。

### 第五步：监控、故障和安全检查（T13–T16）

C 根据真实资源制作 dashboard，至少显示入口请求量/错误、目标健康情况及适当的应用或数据库指标。选择一个有意义的 alarm，例如健康目标数不足或错误率异常。说明为何选它、阈值与统计窗口是什么、怎样测试；通知方式以实验室允许能力为准。保存从正常到 ALARM 再恢复的时间与证据，不能只保存“创建成功”。

故障测试由三人一起做：C 先开始持续请求并记录结果 → A 在已确认另一台健康后停止一台测试实例 → B 操作读写功能 → C 记录失败数、切换时间和恢复结果 → A 恢复环境。先记录目标组的健康检查配置；实际可能有短暂失败，要解释，而不是要求日志一定零失败。

安全检查由 C 提问、A/B 展示：公开入口是什么？应用端口谁能访问？数据库谁能读写？EC2 是否使用允许的角色而非复制旧会话密钥？传输和存储加密实际在哪里配置？是否有未处理限制？把实际情况写入文档，避免再次出现“图是 HTTPS、运行是 HTTP”。

若自动扩容被选为增强，A 配策略、B 保证新实例可复现启动、C 在受控流量下记录扩容与回落。不能仅因 ASG 最小数量设为 2，就说已经证明自动随需求扩容。若改选三个增强主题，要在实施前确认不重复计算 core，并为每个主题留测试和业务理由。

**11/10 检查门槛：**core 证据齐全，未解决问题有负责人；没有证据的增强不能写成已完成。若进度紧，先停止非必要新功能，但课程强制项不能以“降级”省略。

### 第六步：用实际系统生成文档、成本、视频（T17–T21）

- A 将架构图对照资源清单逐项核对：AZ、子网、入口协议、流向、两实例、启动卷、数据层、监控。图不是想象中的目标状态。
- B 汇总每人的章节。重要选择按“需要什么 → 考虑过什么 → 为什么这样选 → 代价/限制 → 实测证据”写。C/A 按部署文档复现关键步骤，缺步骤由原作者补。
- C 使用 AWS Pricing Calculator，选择 us-east-1、12 个月，计算最终架构重要资源。写明实例规格/运行时长、数据量、请求和流量等假设，包含实际选用的负载均衡、磁盘、数据库、日志、出口等。另附实验前后 Lab 余额记录；两者是不同账。
- 视频联合录真实浏览器操作。建议 0–10 秒讲目标及请求路径；10–25 秒现场添加并读取记录；25–45 秒展示已有真实分流或故障测试的关键片段；45–60 秒讲一项选择及代价。长故障测试可剪辑，但标明经过时间，不假装 1 秒完成。是否要求每人出镜以最新课程说明为准。
- 每人整理实际 AI 使用说明、进度截图和个人贡献，不补造历史记录。

### 第七步：交叉检查并提交（T22–T24）

A 查“图与部署一致”；B 查“报告、代码、步骤可复现”；C 查“视频实际操作、成本、证据”。再轮换：A 查 C 的成本，B 查 A 的图，C 查 B 的说明。检查模板残留和密钥，确认所有文件能打开。

Design document 正文严格少于 4,000 词且少于 8 页；架构图及成本估算保守各做 1 页 PDF；视频按 60 秒以内制作，待 tutor 确认冲突。备齐个人签认贡献声明和真实签名封面。指定一名上传者和一名复核者，核对 Moodle 所需代码、文件和提交回执。按已确认的验收安排清理，不要在最终录屏前拆资源，也不要认为 End Lab 就删除了全部资源。

## 5. 三个人怎样共同管理

协作系统已经建好，不再从零创建另一份进度表。当前正式流程见 [team-protocol.md](team-protocol.md)，新成员先读 [onboarding.md](onboarding.md)。

- GitHub Issues 是实时任务状态来源，DASHBOARD.md 和 data/snapshot.json 从它生成。
- 每个人的 AI 开始时运行 `python scripts/team.py --user 本人用户名 start`，读取自己的任务；结束时用 command 功能同步实际进度或交付。
- A/B/C 的真实用户名在 project/config.json 登记。认领需本人身份匹配，修改同一个 AWS 环境需协调；不共用个人密码或临时凭证。
- 代码各开分支，检查后合并同一版本；配置和文档也是交付，不要求每个人都写应用代码。
- 云端不能多人分别操作时，由环境持有人共享屏幕执行，其他人提供代码/步骤并共同验证；明确实际操作者和检查者。
- GitHub 托管自动刷新暂受账号付款/额度限制；当前由聊天时同步助手刷新，不依赖 GitHub Projects 或公开网站。
- 每项完成都要：实际产物、测试和证据、理由/限制、另一位成员复核。不能凭一句“做完”把任务标完成。

## 6. 今晚 45 分钟启动清单

- 0–10 分钟：确认 Reading Tracker 升级范围、认领 A/B/C，写实际名字和各自空闲时间。
- 10–20 分钟：确定最终 Lab 环境持有人；核对预算、权限、数据库候选和 HTTPS 难点。
- 20–30 分钟：打开已经建立的私有仓库与任务看板；检查成员加入和角色配置。
- 30–40 分钟：A/B/C 各讲自己的第一个交付，确认数据/端口/健康检查等对接约定。
- 40–45 分钟：定第一次集成时间、记录 tutor 问题与询问人。

会后第一个动作：A 查权限和网络方案，B 复现旧应用，C 写测试清单。三件事可以同时开始。

## 7. 常见词，用人话解释

| 名称 | 在你们项目里意味着什么 |
| --- | --- |
| GitHub 仓库 | 三个人放同一套代码、保留修改历史的地方 |
| 分支 / Pull Request | 各自先改副本，再请另一人检查后合并 |
| commit | 一次有编号的代码存档；两台服务器要用同一份存档 |
| VPC / 子网 | 你们在 AWS 里的网络范围，以及里面划分的区域 |
| 安全组 | 哪些来源可以访问哪些端口的规则 |
| 可用区 AZ | 同一地区里分开的机房区域，用来降低一起停机的风险 |
| 负载均衡器 / 目标组 | 用户统一访问的入口 / 入口后面可接收请求的服务器名单 |
| 无状态 | 重要记录放共享数据层，不能只存在某一台应用服务器里 |
| IAM 角色 | 程序被允许做哪些 AWS 操作的身份，不是共享个人密码 |
| Dashboard / Alarm | 看运行状态的页面 / 指标异常时进入告警状态的规则 |

## 8. 参考与适用范围

- 本课程源文件路径：`source_materials/INFS3701/03_assessments/group_assessment/`；正文为 INFS3701。要求冲突和 Moodle 更新仍待确认。
- [GitHub Projects 官方说明](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)：任务、看板、表格和时间轴能力。
- [EC2 应用使用 IAM 角色的 AWS 官方说明](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html)：避免向实例分发长期凭证；Lab 仍受课程权限约束。
- [DynamoDB 入门官方文档](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html)：建表和读写的后续操作参考。

这是可执行的组织和实施顺序，不是已经验证过的部署命令集。数据库、运行方式、TLS 和网络路径选定后，由各技术负责人把真实参数和实测命令补进部署记录；不编造 ARN、资源 ID、价格或测试结论。
