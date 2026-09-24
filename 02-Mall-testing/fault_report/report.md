# 故障复盘报告：Mall系统数据库容器意外宕机

## 1. 故障现象
执行自动化回归测试时，所有涉及数据库读写的接口（如品牌列表、登录）全部报错，错误率为 100%。日志显示 `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server...")`。

## 2. 影响范围
所有依赖 MySQL 数据库的线上业务接口（登录、商品查询、品牌列表），影响全部线上用户。

## 3. 排查过程
-  查看 Jenkins 构建日志，发现测试用例全部异常退出。
-  执行 `docker ps`，发现 `mysql` 容器已不在运行列表中（State: Exited）。
-  执行 `docker logs mysql`，发现容器因底层资源问题或进程异常被强制终止。

## 4. 根因分析
1. **直接原因**：MySQL 容器进程异常退出。
2. **深层原因**：服务器仅有 3.5G 内存，且未配置 Swap（交换分区）。在高并发或资源竞争下，内核触发 OOM Killer，优先杀死了内存占用较大的 MySQL 容器。
3. **质量体系漏洞**：缺乏容器级别的健康检查（Healthcheck）和自动重启机制。

## 5. 修复验证
- 紧急执行 `docker start mysql`，服务恢复。
- 重新运行自动化接口测试，4 个用例全部通过，错误率降至 0%，验证通过。

## 6. 预防措施（测试左移）
1. **架构优化**：为 Docker 容器配置 `restart: always`（自动重启策略），并增加 Swap 分区。
2. sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab,已为该 2核4G ECS 创建并挂载 2GB Swap 交换分区，并写入 /etc/fstab 实现开机自动挂载，有效规避了高并发下 OOM（内存溢出）导致的服务意外被杀问题。
3. **测试左移**：在 Jenkins Pipeline 中，增加对数据库、中间件等核心依赖的服务存活探针（Healthcheck）检查，在应用启动前先检查依赖是否就绪。
4. **混沌工程常态化**：引入定时的“故障注入”演练，模拟数据库宕机、网络延迟，验证系统的鲁棒性和监控告警的灵敏度。
5. 原本计划在测试环境部署 K8s 进行混沌工程演练，但经过资源评估，测试服务器只有 4G 内存且已部署了完整的 CI/CD 和监控体系。
6. 为了避免 OOM 导致环境崩溃，我选择在现有 Docker 架构下进行轻量级的混沌测试，这同样达到了验证系统容错性和复盘故障的目的。