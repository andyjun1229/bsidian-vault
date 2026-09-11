# PLC 实测记录：Agent 通过 Modbus TCP 控制虚拟 PLC（2026-09-05）

> 结论先行：**Agent → Modbus TCP → 虚拟PLC 的完整控制链路已跑通**。启停、调速、温控、监测全部实测通过。

## 环境

- 本机 macOS + Python（~/.venvs/hermes）
- pymodbus 3.6.9（注意：3.15 移除了 ModbusSlaveContext/zero_mode，改为 SimData；降级到 3.6.9 用经典 API 最省事）
- 无任何真实硬件，纯软件仿真

## 架构（两个文件，两个进程）

```
agent_ctrl.py (Modbus 主站/客户端)      virtual_plc.py (Modbus 从站/服务端 + 物理仿真)
        │  Modbus TCP 127.0.0.1:5020         ├─ datastore（client 读写）
        ├── 写线圈：电机/加热器启停            └─ 仿真线程：每秒按物理模型
        ├── 写寄存器：目标转速/温度               读 client 下发的目标值，
        └── 读寄存器：当前转速/温度/小时          更新转速（惯性趋近）和温度（热力学），
                                              回写到输入寄存器
```

## 关键设计（踩坑后定稿）

1. **pymodbus 3.6.9 经典 API**：`ModbusSlaveContext(zero_mode=True)`，客户端地址 1-based 直接传（内部-1）。3.15 改成 SimData/SimDevice 且服务端深拷贝 datastore，仿真线程无法直接读写 server 存储 → 3.15 路线放弃
2. **双进程解耦**：datastore（通信）与物理状态（仿真）分离，`modbus_poll_loop` 线程 10Hz 双向同步——这才是真实 PLC 网关的标准做法
3. **地址映射（zero_mode=True 后客户端地址=存储索引）**：
   - Coil 1=电机 2=加热器 3=报警（自动）
   - HR 1=目标RPM 2=目标温度
   - IR 1=当前RPM 2=当前温度×10 3=运行小时

## 实测记录

| 步骤 | 指令 | 结果 |
|---|---|---|
| 启动 | `write_coil(1, True)` | 转速 0→120→240→480（惯性爬升）✅ |
| 升速 | `write_register(HR, 1500)` | 转速指数趋近 1499 RPM（约 20s 稳定）✅ |
| 加热 | `write_coil(2, True)` + `HR2=80` | 温度 20→56°C 持续上升（+0.6°C/s）✅ |
| 停机 | `write_coil(1, False)` | 转速 1379→1259→1139 惯性下降 ✅ |
| 全程监测 | 轮询 IR | 报警灯未触发（未超 100°C/2800RPM 阈值）✅ |

## 意义与下一步

- **证明了 Agent（LLM）→ Modbus → PLC 链路完全可落地**，且不违反“LLM 不碰实时控制”铁律——实时环在仿真线程（未来是真实 PLC 固件），Agent 只通过寄存器下发目标值
- 下一步可做：① 封装成 MCP server 让 Hermes 直接对话控制 ② 接 OpenPLC 开源固件跑真树莓派 ③ 买 ESP32+继电器（¥100）控制真实小设备
- 公众号素材：《我用一杯咖啡的成本，让 AI 摸到了工业控制》实测记录直接可用
