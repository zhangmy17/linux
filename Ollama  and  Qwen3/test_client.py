#!/usr/bin/env python3
import requests
import sys

def test_ollama(host="localhost"):
    url = f"http://{host}:11434/api/generate"
    payload = {
        "model": "qwen3:0.6b",
        "prompt": "介绍一下你自己",
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ 测试成功！")
            print("响应:", result.get("response", "")[:200] + "...")
            return True
        else:
            print(f"❌ 错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    test_ollama(host)