from flask import Flask, request, jsonify
from together import Together

app = Flask(__name__)
client = Together(api_key="ffca1a6d58f718fb91ec5e75a3d783fc3ae2bd5a8d52e7f8bdf0e98937e1e0d6")

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
    app.run(host="0.0.0.0", port=5000)
