from flask import Flask, request, jsonify
from together import Together
from flask_cors import CORS
import os
from dotenv import load_dotenv
import re

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# ✅ 允许所有前端访问（测试用，成功后可改回特定域名）
CORS(app)

# ✅ 确保 API 响应包含 CORS 头
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# 获取 API Key
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("❌ 缺少 TOGETHER_API_KEY，请在 Render 环境变量中设置！")

# 创建 AI 客户端
client = Together(api_key=TOGETHER_API_KEY)

# ✅ 主页路由，避免 404
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Flask API is running!"})

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return jsonify({"message": "✅ Chat API is ready! Use POST to send messages."})

    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "❌ 请输入消息！"}), 400

        # 发送请求到 Together AI
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[{"role": "user", "content": user_message}]
        )

        if not response.choices:
            return jsonify({"error": "❌ AI 生成失败，请稍后再试！"}), 500

        ai_response = response.choices[0].message.content

        # ✅ 过滤掉 `<think>...</think>` 避免影响显示
        cleaned_response = re.sub(r"<think>.*?</think>", "", ai_response, flags=re.DOTALL).strip()

        return jsonify({"response": cleaned_response})

    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 确保使用 Render 的 PORT 变量
    print(f"✅ 服务器运行在端口 {port}")
    app.run(host="0.0.0.0", port=port)
