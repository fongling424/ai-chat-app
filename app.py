from flask import Flask, request, jsonify
from together import Together
import os

app = Flask(__name__)
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=[{"role": "user", "content": user_message}]
    )

    ai_response = response.choices[0].message.content
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
