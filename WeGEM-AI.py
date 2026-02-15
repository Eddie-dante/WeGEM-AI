"""
DEEPSEEK CHAT - Single File AI Assistant
Just run it and start chatting!
"""

import requests
import os
import json
from datetime import datetime

# ============================================
# CONFIGURATION - CHANGE THIS
# ============================================

# Option 1: Put your API key here (easiest)
YOUR_API_KEY = "YOUR_API_KEY_HERE"  # <-- PASTE YOUR DEEPSEEK API KEY HERE

# Option 2: Or set it in environment variable (more secure)
# export DEEPSEEK_API_KEY="sk-d7dae703a0ee45ff947e2b18d43044a4"

# ============================================
# MAIN AI CLASS
# ============================================

class DeepSeekChat:
    def __init__(self, api_key=None):
        """Initialize with your API key"""
        self.api_key = api_key or YOUR_API_KEY or os.getenv("sk-d7dae703a0ee45ff947e2b18d43044a4")
        
        if self.api_key == "sk-d7dae703a0ee45ff947e2b18d43044a4" or not self.api_key:
            print("\n" + "="*50)
            print("🔑 NEED DEEPSEEK API KEY")
            print("="*50)
            print("\n1. Get your free key at: https://platform.deepseek.com/")
            print("2. Edit this file and paste it where it says YOUR_API_KEY_HERE")
            print("\nOr run with:")
            print("   python deepseek_chat.py YOUR_API_KEY_HERE")
            print("="*50)
            exit()
        
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Be concise and friendly."}
        ]
        print("\n✅ DeepSeek AI Ready! Type /help for commands\n")
    
    def ask(self, question):
        """Ask the AI a question"""
        self.messages.append({"role": "user", "content": question})
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": self.messages,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
                self.messages.append({"role": "assistant", "content": answer})
                return answer
            else:
                return f"❌ Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear(self):
        """Clear conversation history"""
        self.messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Be concise and friendly."}
        ]
        return "🔄 Conversation cleared!"
    
    def save(self):
        """Save conversation to file"""
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=2)
        return f"💾 Saved to {filename}"

# ============================================
# INTERACTIVE CHAT
# ============================================

def main():
    """Start interactive chat"""
    print("="*50)
    print("🚀 DEEPSEEK AI CHAT - Single File Version")
    print("="*50)
    
    # Get API key from command line if provided
    import sys
    api_key = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Create AI instance
    ai = DeepSeekChat(api_key)
    
    # Show commands
    print("\nCommands: /clear, /save, /help, /quit")
    
    while True:
        try:
            # Get user input
            user = input("\n👤 You: ").strip()
            
            if not user:
                continue
            
            # Handle commands
            if user.lower() == '/quit':
                print("\n👋 Goodbye!")
                break
            elif user.lower() == '/clear':
                print(ai.clear())
                continue
            elif user.lower() == '/save':
                print(ai.save())
                continue
            elif user.lower() == '/help':
                print("\n📋 COMMANDS:")
                print("  /quit  - Exit")
                print("  /clear - Reset conversation")
                print("  /save  - Save to file")
                print("  /help  - Show this menu")
                continue
            
            # Get AI response
            print("🤖 AI: ", end="", flush=True)
            response = ai.ask(user)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# ============================================
# SIMPLE FUNCTION (Just 10 lines!)
# ============================================

def quick_chat(api_key):
    """Super simple chat function"""
    messages = [{"role": "system", "content": "You are helpful."}]
    
    while True:
        user = input("\nYou: ")
        if user == 'quit': break
        
        messages.append({"role": "user", "content": user})
        
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "deepseek-chat", "messages": messages}
        )
        
        reply = r.json()['choices'][0]['message']['content']
        print(f"AI: {reply}")
        messages.append({"role": "assistant", "content": reply})

# ============================================
# RUN IT
# ============================================

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("\n📦 Installing requests library...")
        os.system("pip install requests")
        import requests
    
    # Ask which mode
    print("\nChoose mode:")
    print("1. Full Chat (with memory & commands)")
    print("2. Quick Chat (simple & fast)")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "2":
        api_key = YOUR_API_KEY or input("\nEnter your API key: ")
        quick_chat(api_key)
    else:
        main()
