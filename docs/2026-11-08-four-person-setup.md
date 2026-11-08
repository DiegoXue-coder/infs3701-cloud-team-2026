# 四人配置实际记录 / Four-person setup record

DiegoXue-coder授权将剩余工作扩为四人，并提供Tenzin的GitHub用户名wyend12。2026-11-08实际查询GitHub公开用户API确认login=wyend12，profile=https://github.com/wyend12；仓库权限查询返回none，pending invitations查询中无该用户。未发送邀请、未授予访问或AWS权限，未用他的身份登录或认领。

实际代码/文件变更：协调器与本机设置增加D；角色预留到wyend12；T19/T20从原计划B/C改为D（实际远程查询均todo且owner=null）；新增英文T25独立准备目标/证据矩阵；英文工作规则、角色指南、开工提示词；静态入口与动态看板包含D；新回执增加英文摘要，原文与结构化字段保留。历史中文回执不重写，不承诺动态自由文本自动翻译。

实际测试：[最终执行日志](../evidence/T02/2026-11-08-four-person-workflow-final-tests.log)，62项通过。包含D绑定幂等、不覆盖他人角色、本人英文认领/partial交付验证与回执、重试不重复回执、最终依赖与自批限制、并发同步锁和原三角色规则。早一轮60项日志保留；新增防止已有认领被重新分配覆盖的检查后，以62项结果为最终版本。

本机使用setup_member.py --role D（未--install）验证D计划检查入口；没有声称在Tenzin电脑完成安装/授权。任何fake GitHub测试仅为离线单元测试，不能写为wyend12真人已加入。D还需由持有人邀请Write权限、本人接受、本人AI/Git授权、doctor/start和实际首项认领。

下次成员可直接使用[prompts/START-en.md](../prompts/START-en.md)与[docs/member-D.md](member-D.md)。A/B/C/D分工见[four-person-plan.md](four-person-plan.md)。本轮未恢复或改变AWS，B报告的503原因仍未知。
