# 追踪与跨度：你应该了解的可观测性基础 | Last9

2025年4月23日

在现代软件架构中，应用不只是变得更大——它们正变得越来越分布式。随着微服务、无服务器函数和容器在多个环境中运行，想要了解系统内部到底发生了什么，感觉就像试图在暴风雨中追踪一滴雨点。

这正是追踪（trace）与跨度（span）登场的地方。这些可观测性（observability）工具不只是流行词——它们是你理解复杂分布式系统的秘密武器。下面我们拆解一下追踪和跨度是什么、为什么重要，以及如何用它们更快地排障、构建更可靠的系统。

## 理解追踪与跨度：核心概念

追踪记录一个请求在分布式系统中的旅程。可以把追踪想象成一个请求从头到尾的完整故事——从用户点击按钮，到他们看到结果。

跨度是构成追踪的积木。每个跨度代表这段旅程中的一个工作单元——比如一次数据库查询、一次 API 调用，或一次函数执行。跨度彼此嵌套，用来展示操作之间的父子关系。

用简单的话说，它们的关系如下：

- 一条追踪包含多个跨度
- 每个跨度代表一个操作
- 跨度带有计时数据和元数据
- 跨度可以嵌套，用来展示操作之间如何相互关联

```
Trace ├── Span（API 网关）
     │    ├── Span（认证服务）
     │    └── Span（用户服务）
     │         └── Span（数据库查询）
     └── Span（响应格式化）
```

如果你好奇追踪和跨度如何与指标（metrics）、日志（logs）和事件（events）配合，本文会分解这四者。

## 追踪与跨度对 DevOps 专业人员的价值

你正在运行一个有几十个微服务的复杂系统。突然，用户反馈结账流程很慢。如果没有追踪，你得逐个检查每个服务，白白浪费时间。

有了追踪和跨度，你可以：

- **即时定位瓶颈**：精确看出哪个服务或函数耗时过长
- **跨服务边界调试**：跟随请求在服务之间跳转
- **理解依赖关系**：可视化服务之间如何连接、如何相互依赖
- **提升性能**：精确地识别并修复慢操作
- **缩短平均恢复时间（MTTR）**：问题出现时更快找到根因

## 追踪与跨度的技术实现

下面进入分布式系统中追踪的工作原理。

### 追踪上下文与传播

要让追踪跨服务边界生效，每个服务都需要知道自己在处理同一个请求的一部分。这通过上下文传播（context propagation）实现——在服务之间传递追踪 ID 和跨度 ID。

当一个请求第一次进入你的系统时，它会被分配一个唯一的追踪 ID。随着请求在服务之间流转，这个 ID 会随它一起传递（通常以 HTTP 头的形式）。每个服务随后创建自己的跨度，但把它们关联到同一条追踪上。

### 跨度属性与事件

跨度不只是时间戳——它们承载着丰富的数据：

- **名称（Name）**：这个跨度代表什么操作
- **计时（Timing）**：开始与结束时间
- **状态（Status）**：成功、错误等
- **属性（Attributes）**：自定义的键值对（比如 user_id 或 cart_size）
- **事件（Events）**：跨度内值得注意的发生事项
- **链接（Links）**：与其他跨度的连接

### 采样策略

追踪所有请求会产生海量数据。因此大多数系统会采用采样（sampling）——只收集一部分追踪。聪明的采样策略包括：

- **头部采样（Head-based sampling）**：在请求开始时决定是否采样
- **尾部采样（Tail-based sampling）**：在请求完成后决定（更擅长捕捉错误）
- **优先级采样（Priority sampling）**：总是追踪重要操作，只对常规操作采样

如果你想了解可观测性、遥测（telemetry）与监控（monitoring）之间的区别，可以看看这篇：Observability vs Telemetry vs Monitoring（可观测性 vs 遥测 vs 监控）。

## 追踪实施指南：工具与框架

准备好为系统添加追踪了吗？下面是你要用到的：

### OpenTelemetry：行业标准

OpenTelemetry 已成为实施追踪与跨度的事实标准框架。它提供：

- 覆盖所有主流编程语言的库
- 厂商中立的 API 与 SDK
- 对流行框架的自动埋点（instrumentation）
- 一套一致的数据采集与导出方式

### 追踪工具箱

以下工具有助于你采集、存储和可视化追踪：

| 工具 | 类型 | 最擅长 |
|---|---|---|
| Last9 | 一体化可观测性 | 成本可控、高基数（high-cardinality）可观测性，定价可预测 |
| Jaeger | 开源追踪 | 自托管追踪可视化 |
| Zipkin | 开源追踪 | 简单分布式追踪 |
| Grafana Tempo | 追踪后端 | 与 Grafana 仪表盘集成 |
| OpenTelemetry Collector | 数据采集管道 | 处理与路由遥测数据 |

如果你在寻找一款符合预算的可观测性方案，Last9 值得一看。它按摄取事件计费，成本可控可预测。此外，我们的平台能大规模处理高基数数据，并与 OpenTelemetry 和 Prometheus 集成，把指标、日志和追踪汇聚到一处。

### 在代码中实施追踪

下面是一个简化示例，展示如何在 Node.js 应用中使用 OpenTelemetry 创建跨度：

```js
// 初始化 OpenTelemetry SDK（在应用中只需一次）
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const provider = new NodeTracerProvider();
const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// 获取一个 tracer
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

// 在代码中创建跨度
async function processOrder(orderId) {
  const span = tracer.startSpan('process-order');
  // 为跨度添加属性
  span.setAttribute('order.id', orderId);
  span.setAttribute('customer.type', 'premium');
  try {
    // 执行工作...
    // 创建一个子跨度
    const dbSpan = tracer.startSpan('database-query', {
      parent: span,
    });
    try {
      // 执行数据库查询...
      dbSpan.end();
    } catch (error) {
      dbSpan.setStatus({ code: SpanStatusCode.ERROR });
      dbSpan.recordException(error);
      dbSpan.end();
      throw error;
    }
    span.end();
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR });
    span.recordException(error);
    span.end();
    throw error;
  }
}
```

想知道 OpenTelemetry 与传统 APM 工具相比如何？本文分解了关键区别：OpenTelemetry vs Traditional APM Tools（OpenTelemetry vs 传统 APM 工具）。

## 进阶追踪技术

一旦基础追踪就位，这些进阶技术能把你的可观测性提升到新的层次。

### 分布式上下文管理

在复杂系统中，你需要管理追踪 ID 之外的上下文。W3C Trace Context 规范为以下内容提供了标准：

- **traceparent**：包含追踪 ID 与父跨度 ID
- **tracestate**：允许厂商添加自定义上下文数据

使用这些头能确保你的追踪在不同服务与厂商之间正常运作。

### 追踪、指标与日志的关联

可观测性真正的威力来自连接不同的信号：

- **样例追踪（Exemplar traces）**：把指标链接到产生它们的追踪上
- **日志中的追踪 ID**：把追踪 ID 加入日志消息以便交叉引用
- **自定义属性**：在各类遥测数据中使用一致的属性

### 错误处理与异常追踪

当异常发生时，跨度能提供关键上下文：

- 把跨度标记为错误状态
- 用堆栈轨迹记录异常
- 为跨度添加展示错误进展的事件
- 创建跨服务边界携带错误上下文的 baggage 项

如需深入了解如何领先一步处理问题、提升系统可靠性，可以看看这篇关于主动监控的文章：Proactive Monitoring（主动监控）。

## 真实世界的追踪模式与反模式

### 有效的追踪模式

- **有意义的跨度名称**：使用一致的命名约定，如 service_name/operation
- **合适的粒度**：只为重要操作创建跨度，而不是每个函数调用
- **正确的上下文传播**：确保追踪上下文流经所有通信渠道
- **有用的属性**：添加有助于排障的属性，比如用户 ID 或特性开关
- **性能意识**：警惕过度创建跨度带来的开销

### 需要避免的追踪反模式

- **过度埋点**：创建过多跨度会导致性能问题
- **缺失上下文**：无法传播上下文会打断跨服务边界的追踪
- **命名不一致**：使用不同的命名标准会让追踪更难解读
- **数据过多**：在跨度中放入大体积负载会压垮追踪后端
- **忽略第三方服务**：缺少外部调用的跨度会产生盲区

探究可观测性如何在 LLM 的性能与可靠性中扮演关键角色：LLM Observability（LLM 可观测性）。

## 追踪与跨度的商业价值：超越技术收益

追踪不只是用来排障——它也能提供商业洞察：

- 端到端追踪关键用户旅程
- 衡量关键业务操作的性能
- 基于追踪数据设定 SLO（服务级别目标）
- 用真实用户维度量化性能问题的成本
- 通过为跨度添加相关属性来建立业务上下文

当你能展示技术改进如何影响用户体验与业务指标时，你就在 DevOps 与业务干系人之间架起了桥梁。

## 结论

追踪和跨度让你拥有对分布式系统的"X 光"视野。它们揭示服务之间隐藏的连接、精准定位性能瓶颈，并大幅加速调试。

随着系统日益复杂，这种可观测性不再是奢侈品——而是必需品。

## 常见问题（FAQ）

### 追踪和日志的区别是什么？

日志记录的是离散事件，而追踪展示的是操作在服务之间的关联。日志告诉你"发生了什么"，追踪则展示"它是如何发生的"。

### 添加追踪会拖慢我的应用吗？

现代追踪库的开销极小——在配置得当的情况下，性能影响通常低于 3%。配合采样，还可以进一步降低影响。

### 我需要修改所有代码才能添加追踪吗？

不一定。许多框架提供自动埋点，只需极少代码改动即可添加追踪。OpenTelemetry 为多数语言的主流框架提供了自动埋点。

### 分布式追踪会产生多少数据？

这因流量、采样率和跨度细节而异。繁忙系统每天可能产生从 GB 到 TB 级别的数据。因此选择合适的可观测性平台对成本控制至关重要。

### 追踪能帮助安全和合规吗？

能！追踪会为请求流经系统的过程留下审计轨迹。配合合适的属性，你可以追踪哪些用户或服务在何时访问了哪些数据。

### 追踪和跨度如何与其他可观测性信号配合？

追踪与指标、日志互为补充。指标从高层展示系统健康度，日志提供详细事件，而追踪则串联起请求在服务之间的流动路径。
