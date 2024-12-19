# Scoop

关于 scoop 环境变量资料补充，目前观察到两类

1. (以 7z 为例) 在 json 文件下指定了 bin 字段，scoop 会为相关文件创建 shim
2. (以 gcc 为例) 在 json 中使用 env_add_path, env_set 直接设置环境变量

所以如果发现安装完依然提示找不到程序，可以尝试从这两点检查
