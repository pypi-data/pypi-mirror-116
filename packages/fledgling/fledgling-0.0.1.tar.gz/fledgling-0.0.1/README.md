# fledgling

管理nest中的任务、计划等数据的客户端程序。

# 特性

`fledgling`提供了与`nest`中大部分的 HTTP 接口对应的命令行子命令，列举如下：

| 功能|fledgling 子命令 | nest 的接口 |
|-|-|-|
|创建任务|create-task|POST /task|
|删除任务|delete-task|DELETE /task/<id_>|
|列出任务|list-task|GET /task|
|创建计划|create-plan|POST /plan|
|删除计划|delete-plan|DELETE /plan/<id_>|
|列出计划|list-plan|GET /plan|
|处理计划|event-loop| POST /plan/pop |

# 安装

<!-- TODO: 补充从 PyPI 中安装 fledgling 的方法。 -->

# 用法

## 帮助文档

可以用命令`fledgling --help`查看 fledgling 提供的所有子命令

```shell
bash-3.2$ fledgling --help
Usage: fledgling [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  change-plan    修改指定计划。
  create-config  创建一份空的配置文件。
  create-plan    为任务创建一个计划。
  create-task    创建一个任务。
  delete-plan    删除指定计划。
  delete-task    删除指定任务及其计划。
  event-loop     启动事件循环拉取计划并弹出提醒。
  list-plan      列出接下来的计划。
  list-task      列出任务。
```

子命令本身也可以接受`--help`参数来打印它的使用说明

```shell
bash-3.2$ fledgling change-plan --help
Usage: fledgling change-plan [OPTIONS]

  修改指定计划。

Options:
  --duration INTEGER
  --location-id INTEGER
  --plan-id INTEGER          [required]
  --repeat-interval INTEGER
  --repeat-type TEXT
  --trigger-time TEXT
  --visible-hours TEXT
  --visible-wdays TEXT
  --help                     Show this message and exit.
```

## 示例

### 创建一个任务，并设定它的提醒时间

```shell
fledgling create-task --brief '测试用的任务'
fledgling create-plan --task-id 69 --trigger-time '2021-08-15 17:40:00'  # 传给选项--task-id的数字69是上一道命令创建的任务的ID
```

### 设定一个每小时提醒一次的任务

```shell
fledgling create-task --brief '喝水'
fledgling create-plan --task-id 3 --trigger-time '2021-08-15 18:20:00' --repeat-type 'hourly'
```

