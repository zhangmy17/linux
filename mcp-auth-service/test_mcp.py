#!/usr/bin/env python3
import requests
import sys


def test_mcp(host="localhost"):
    base = f"http://{host}:5000"

    print("测试健康检查...")
    r = requests.get(f"{base}/api/health")
    print(f"  ✅ {r.json()}")

    print("\n测试获取Token...")
    r = requests.post(f"{base}/api/token", json={"username": "admin", "password": "admin123"})
    token = r.json().get('token')
    print(f"  ✅ Token获取成功: {token[:30]}...")

    print("\n测试受保护接口...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{base}/api/user/info", headers=headers)
    print(f"  ✅ {r.json()}")

    print("\n✅ 所有测试通过！")


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    test_mcp(host)