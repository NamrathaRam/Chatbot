from flask import Flask, request, jsonify, render_template
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential
import config

app = Flask(__name__)

client = OpenAIClient(
    endpoint=config.AZURE_OPENAI_ENDPOINT,
    credential=AzureKeyCredential(config.AZURE_OPENAI_KEY)
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    system_prompt = """
    You are an AI Chatbot for customer query resolution.
    Be helpful, concise, and context-aware.
    """

    response = client.chat.completions.create(
        model=config.AZURE_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
