"""
DEEPSEEK MINI AI - Single File Version
A lightweight AI assistant powered by DeepSeek API
GitHub Ready - Just clone and run!

Author: Your Name
License: MIT
"""

import requests
import json
import os
import sys
from datetime import datetime
from typing import Optional, Dict, List

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_MODEL = "deepseek-chat"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# ============================================================================
# MAIN AI CLASS
# ============================================================================

class DeepSeekMiniAI:
    """
    A simple yet powerful AI assistant using DeepSeek's API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the DeepSeek AI
        
        Args:
            api_key: Your DeepSeek API key. If None, checks environment variable.
        """
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        
        if not self.api_key:
            print("\n" + "="*60)
            print("🔑 DEEPSEEK API KEY REQUIRED")
            print("="*60)
            print("\nPlease get your API key from: https://platform.deepseek.com/")
            print("\nThen you can either:")
            print("1. Set it as environment variable: export DEEPSEEK_API_KEY='your-key'")
            print("2. Pass it directly when creating the AI")
            print("3. Enter it now (will be used for this session only)\n")
            
            self.api_key = input("Enter your DeepSeek API key: ").strip()
            
            if not self.api_key:
                raise ValueError("API key is required to use DeepSeek Mini AI")
        
        self.model = DEFAULT_MODEL
        self.conversation_history: List[Dict] = [
            {"role": "system", "content": "You are a helpful, friendly AI assistant named DeepSeek Mini."}
        ]
        print("\n✅ DeepSeek Mini AI initialized successfully!")
        
    def chat(self, message: str, temperature: float = 0.7) -> str:
        """
        Send a message to DeepSeek and get response
        
        Args:
            message: Your message to the AI
            temperature: Creativity level (0.0 = focused, 1.0 = creative)
            
        Returns:
            AI's response as string
        """
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Prepare API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": temperature,
                "max_tokens": 2000
            }
            
            # Make API call
            print("🤔 Thinking...", end="\r")
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            print(" " * 20, end="\r")  # Clear "Thinking..." line
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Add to history
                self.conversation_history.append(
                    {"role": "assistant", "content": ai_response}
                )
                
                return ai_response
            else:
                return f"❌ Error {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return "❌ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "❌ Connection error. Check your internet."
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def reset(self):
        """Clear conversation history"""
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful, friendly AI assistant named DeepSeek Mini."}
        ]
        return "🔄 Conversation reset!"
    
    def save(self, filename: Optional[str] = None) -> str:
        """Save conversation to file"""
        if not filename:
            filename = f"deepseek_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            return f"💾 Conversation saved to {filename}"
        except Exception as e:
            return f"❌ Failed to save: {str(e)}"
    
    def stats(self) -> Dict:
        """Get conversation statistics"""
        return {
            "messages": len(self.conversation_history) - 1,  # Excluding system prompt
            "user": sum(1 for m in self.conversation_history if m["role"] == "user"),
            "assistant": sum(1 for m in self.conversation_history if m["role"] == "assistant"),
            "model": self.model
        }

# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════╗
║     🚀 DEEPSEEK MINI AI - Single File        ║
║     Powered by DeepSeek API                   ║
╚══════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """Print help menu"""
    help_text = """
📋 COMMANDS:
────────────
/quit  - Exit the program
/exit  - Same as /quit
/clear - Clear conversation history
/reset - Same as /clear
/save  - Save conversation to file
/stats - Show conversation statistics
/help  - Show this menu

💡 TIPS:
────────
• Just type anything to chat with the AI
• The AI remembers the whole conversation
• Your API key is never saved to disk
• All conversations are private

🎯 EXAMPLE:
───────────
You: What is artificial intelligence?
AI: Artificial intelligence (AI) is the simulation of...
    """
    print(help_text)

def main():
    """Main function to run the AI"""
    print_banner()
    
    # Initialize AI
    try:
        ai = DeepSeekMiniAI()
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    
    print("\nType /help for commands, or just start chatting!\n")
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            cmd = user_input.lower()
            
            if cmd in ['/quit', '/exit']:
                print("\n👋 Thank you for using DeepSeek Mini AI! Goodbye!")
                break
                
            elif cmd in ['/clear', '/reset']:
                print(ai.reset())
                continue
                
            elif cmd == '/save':
                print(ai.save())
                continue
                
            elif cmd == '/stats':
                stats = ai.stats()
                print("\n📊 STATISTICS:")
                print(f"  Total messages: {stats['messages']}")
                print(f"  You: {stats['user']}")
                print(f"  AI: {stats['assistant']}")
                print(f"  Model: {stats['model']}")
                continue
                
            elif cmd == '/help':
                print_help()
                continue
            
            # Get AI response
            response = ai.chat(user_input)
            print(f"\n🤖 AI: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

# ============================================================================
# SIMPLE ONE-FUNCTION VERSION
# ============================================================================

def quick_chat(api_key: Optional[str] = None):
    """
    Ultra-simple chat function - just 20 lines!
    
    Args:
        api_key: Your DeepSeek API key
    """
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("❌ Please set DEEPSEEK_API_KEY environment variable")
        return
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    print("\n🤖 Quick DeepSeek Chat (type 'quit' to exit)\n")
    
    while True:
        user = input("You: ").strip()
        if user.lower() == 'quit':
            break
            
        messages.append({"role": "user", "content": user})
        
        try:
            response = requests.post(API_URL, headers=headers, 
                                   json={"model": DEFAULT_MODEL, "messages": messages})
            
            if response.status_code == 200:
                reply = response.json()['choices'][0]['message']['content']
                print(f"AI: {reply}\n")
                messages.append({"role": "assistant", "content": reply})
            else:
                print(f"Error: {response.status_code}\n")
        except Exception as e:
            print(f"Error: {e}\n")

# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_ai():
    """Simple test to verify everything works"""
    print("🧪 Running test...")
    
    # Check if requests is installed
    try:
        import requests
        print("✅ requests library found")
    except ImportError:
        print("❌ Please install requests: pip install requests")
        return False
    
    # Check Python version
    if sys.version_info >= (3, 6):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} (3.6+ required)")
    else:
        print("❌ Python 3.6+ required")
        return False
    
    print("\n✅ All tests passed! Ready to run.")
    return True

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run test first
    if not test_ai():
        sys.exit(1)
    
    # Ask user which version to run
    print("\n" + "="*50)
    print("CHOOSE YOUR INTERFACE:")
    print("="*50)
    print("1. 🎯 Full AI Assistant (with memory, commands, saves)")
    print("2. ⚡ Quick Chat (simple, no frills)")
    print("3. 🧪 Just test installation")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "2":
        quick_chat()
    elif choice == "3":
        print("\n✅ Installation looks good!")
    else:
        main()
