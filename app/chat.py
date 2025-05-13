import os 
import openai
from flask import Blueprint, render_template, session
from flask_socketio import emit
from app import socketio

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_bp = Blueprint("chat", __name__)

def get_ai_reply(prompt, conversation=None,
                 model="gpt-4", temperature=0.7, max_tokens=150,
                 system_prompt=(
                    "You are a professional cybersecurity support agent. "
                     "Your responses must be clear, detailed, and formal. "
                     "Avoid one-word yes/no answers and provide thorough technical explanations."
                 )):
    """
    Sends the converstaion context along with the prompt to OpenAI's ChatCompletion API
    and returns the assistant's reply.
    """
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if conversation:
        messages.extend(conversation)
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response['choices'][0]['message']['content'].strip()
        print("AI: ", reply)
    except Exception as e:
        reply = f"Error: {str(e)}"
        print("OpenAI Error: ", e)

    return reply

@chat_bp.route("/chat")
def chat():
    session["conversation"] = []
    session.modified = True
    return render_template("chat.html")


@socketio.on("message")
def handle_message(data):
    """
    Socket.IO event handler that receives data (from the client) and then:
      1. Retrieves and appends the user's message to the conversation history (stored in session).
      2. Calls OpenAI to get a reply.
      3. Updates the conversation history.
      4. Emits both messages back to the client.
    
    Supports both a raw string or a JSON object with a "message" property.
    """
    if isinstance(data, dict):
        user_message = data.get("message")
    else:
        user_message = data
    
    if not user_message:
        print("No message provided")
        return
    
    conversation = session.get("conversation", [])
    conversation.append({"role": "user", "content": user_message})
    session["conversation"] = conversation
    session.modified = True
    print("User message: ", user_message)

    ai_reply = get_ai_reply(user_message, conversation=conversation)
    
    conversation.append({"role": "assistant", "content": ai_reply})
    session["conversation"] = conversation
    session.modified = True
    print("AI: ", ai_reply)
    
    emit("message", {"message": user_message, "sender": "User"}, broadcast=True)
    emit("message", {"message": ai_reply, "sender": "AI"}, broadcast=True)