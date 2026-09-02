import sys
from ai_router import ask_railway_ai


# ============================================================
# RAILWAY AI ASSISTANT - TERMINAL VERSION
# ============================================================

def print_welcome():
    print()
    print("=" * 70)
    print("🚆  INDIAN RAILWAY AI ASSISTANT")
    print("=" * 70)
    print("🤖 Ask me anything about Indian Railways.")
    print()
    print("You can ask about:")
    print("  🚆 Trains")
    print("  🛤️  Routes")
    print("  🕐 Train schedules")
    print("  📍 Railway stations")
    print("  🔎 Train numbers")
    print("  💬 Follow-up questions")
    print()
    print("Examples:")
    print("  • Mumbai to Goa")
    print("  • Find trains from Mumbai to Delhi")
    print("  • Tell me about train 10103")
    print("  • Show schedule of 10103")
    print("  • What is Karmali station?")
    print("  • Which trains run between Delhi and Mumbai?")
    print()
    print("Type 'help' for help.")
    print("Type 'exit' or 'quit' to close the assistant.")
    print("=" * 70)
    print()


def print_help():
    print()
    print("🤖 WHAT YOU CAN ASK")
    print("-" * 60)

    print()
    print("🚆 TRAIN INFORMATION")
    print("  Tell me about train 10103")
    print("  Find train 12051")
    print("  What is train 12951?")

    print()
    print("🛤️ ROUTE SEARCH")
    print("  Mumbai to Goa")
    print("  Find trains from Mumbai to Delhi")
    print("  Which trains go from Delhi to Chennai?")

    print()
    print("🕐 TRAIN SCHEDULE")
    print("  Show schedule of 10103")
    print("  What is the timing of train 10103?")
    print("  Tell me the schedule of train 12051")

    print()
    print("📍 STATION INFORMATION")
    print("  What is Karmali station?")
    print("  Tell me about Mumbai station")
    print("  Give me information about Madgaon")

    print()
    print("💬 GENERAL")
    print("  I want to travel from Mumbai to Goa")
    print("  Find trains from Mumbai to Goa")
    print("  Which train should I check?")

    print()
    print("Type 'exit' to leave.")
    print()


def ask_question(question, conversation):
    """
    Send the user's question to the AI router.
    """

    try:

        result = ask_railway_ai(
            question,
            conversation=conversation
        )

        return result

    except TypeError:
        # Supports older versions of ai_router.py
        try:
            result = ask_railway_ai(question)
            return result

        except Exception as e:
            return f"❌ Error: {e}"

    except Exception as e:
        return f"❌ Error: {e}"


def main():

    print_welcome()

    # Conversation history
    conversation = []

    while True:

        try:
            question = input("👤 You: ").strip()

        except KeyboardInterrupt:
            print()
            print("\n👋 Goodbye!")
            sys.exit(0)

        except EOFError:
            print()
            print("\n👋 Goodbye!")
            sys.exit(0)

        # ----------------------------------------------------
        # Empty input
        # ----------------------------------------------------

        if not question:
            print("🤖 Please enter a question.")
            continue

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if question.lower() in {
            "exit",
            "quit",
            "bye",
            "goodbye"
        }:
            print()
            print("🤖 Thank you for using Indian Railway AI Assistant.")
            print("👋 Goodbye!")
            break

        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        if question.lower() in {
            "help",
            "commands",
            "options"
        }:
            print_help()
            continue

        # ----------------------------------------------------
        # CLEAR CONVERSATION
        # ----------------------------------------------------

        if question.lower() in {
            "clear",
            "reset",
            "new conversation"
        }:
            conversation = []
            print("🤖 Conversation cleared.")
            print()
            continue

        # ----------------------------------------------------
        # PROCESS QUESTION
        # ----------------------------------------------------

        print()
        print("🤖 Railway Assistant: ", end="", flush=True)

        answer = ask_question(
            question,
            conversation
        )

        print()
        print(answer)
        print()

        # ----------------------------------------------------
        # SAVE CONVERSATION
        # ----------------------------------------------------

        conversation.append({
            "role": "user",
            "content": question
        })

        conversation.append({
            "role": "assistant",
            "content": str(answer)
        })


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()