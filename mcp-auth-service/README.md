# MCP鉴权服务

基于Flask和JWT的MCP服务，包含鉴权功能。

## API接口

### 获取Token（无需鉴权）
```bash
curl -X POST http://localhost:5000/api/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 获取用户信息（需要鉴权）
```bash
curl -X GET http://localhost:5000/api/user/info \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 快速启动
```bash
docker-compose up -d --build
python test_mcp.py
```

## 作者
张铭宇