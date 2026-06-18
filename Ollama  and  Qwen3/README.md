# Ollama + Qwen3 模型部署

使用Docker部署Ollama服务，运行Qwen3 0.6B模型。

## 快速开始

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志（等待模型下载）
docker-compose logs -f

# 测试
python test_client.py

API接口
服务地址: http://localhost:11434

模型名称: qwen3:0.6b

作者
张铭宇