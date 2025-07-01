import cv2
import os
import numpy as np
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

# Import your tools
from tools import wiki_tool

load_dotenv()

# Pydantic Model for structured AI output
class RepairAdvice(BaseModel):
    # Added 'type' field to distinguish between advice and clarification
    type: str = "advice" # Can be "advice" or "clarification"
    issue_type: str | None = None 
    diagnosis: str | None = None 
    diy_steps: list[str] | None = None 
    materials_needed: list[str] | None = None 
    safety_tips: list[str] | None = None 
    # Added fields for clarification
    clarification_question: str | None = None
    clarification_reason: str | None = None

# Placeholder Image Analysis Function 
def analyze_image_for_repair(image_path: str) -> str | None:
    """
    Loads an image from the given path and performs a rudimentary "analysis"
    to determine a repair issue. This is a placeholder for actual machine
    learning/computer vision models and is NOT accurate for real diagnosis.
    It's for demonstrating the pipeline from image to agent input.
    """
    try:
        # Check if the file exists
        if not os.path.exists(image_path):
            print(f"Error: File not found at '{image_path}'. Please check the path.")
            return None

        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image from '{image_path}'. "
                  "The file might be corrupted, not an image, or permissions are wrong.")
            return None

        # Rudimentary "Analysis" Logic (Highly Simplified) 
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        binary_mask = (gray_img < 50).astype(np.uint8) * 255
        num_very_dark_pixels = cv2.countNonZero(binary_mask)

        total_pixels = img.shape[0] * img.shape[1]
        dark_percentage = (num_very_dark_pixels / total_pixels) * 100 if total_pixels > 0 else 0

        avg_pixel_value = gray_img.mean()

        # Improved rudimentary logic for testing based on image context
        if dark_percentage > 8:# Increased threshold slightly for very dark spots like mold
            return "damp or mold on my wall"
        elif avg_pixel_value < 100:
            return "a dark stain or discoloration on my wall"
        else:
            return "a general wall problem" # Changed default to be less specific

    except Exception as e:
        print(f"An unexpected error occurred during image processing: {e}")
        return None

#  LangChain Setup 
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro") # WILL RATE LIMIT

parser = PydanticOutputParser(pydantic_object=RepairAdvice)

prmpt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a friendly and knowledgeable DIY home repair assistant, here to help with common housing issues like damp, cracks, and other minor household repairs.
            Your goal is to provide clear, actionable, and safe advice to users who are looking to fix things themselves.
            Please diagnose the problem based on the user's description (which might come from an image analysis) and offer step-by-step DIY repair instructions, including necessary materials and safety tips.
            Remember to always be encouraging and supportive!

            If the user's initial description is too vague or incomplete and you need more information to provide specific, useful advice,
            you MUST set the 'type' field to "clarification" and ask a specific 'clarification_question' along with a brief 'clarification_reason'.
            In this case, only fill the 'type', 'clarification_question', and 'clarification_reason' fields, and set all other fields to null.

            If any section like 'materials_needed' or 'safety_tips' is genuinely not applicable or empty for a given diagnosis,
            you MUST provide an empty list `[]` for that field. Do not use phrases like 'Not Applicable' inside the lists.

            If a described issue is too complex, dangerous, or clearly requires professional expertise (e.g., major structural damage, electrical faults, gas leaks),
            please clearly state this in the 'diagnosis' and suggest consulting a qualified professional, providing very minimal or no DIY steps.
            For 'issue_type' in such cases, you can use "Professional Assistance Recommended".

            You can use your tools, including searching online for current information, to gather details if needed.
            If you attempt to use a tool and it doesn't provide the necessary information, or if you cannot find a relevant answer,
            please state clearly that you were unable to find the specific information, and then provide the best general advice you can, or ask for more details.
            Do not make up information if your tools fail to provide it.

            IMPORTANT: ONLY return your answer in raw JSON, no explanations, no extra text outside the JSON.
            Format it exactly like this:\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Tools setup 
tools = [wiki_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prmpt,
    tools=tools,
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False) # verbose=True can be helpful for debugging agent's thoughts

# Main CLI Loop 
chat_history = [
    ("system", "Hello! I'm your friendly DIY home repair assistant. What seems to be the problem you're facing today? You can describe it in detail, or type 'image' to provide a path to a picture. (Type 'exit' at any time to quit)."),
]

print(chat_history[0][1])

while True:
    input_choice = input("\nHow would you like to describe your issue? (Type 'text' or 'image'): ").lower().strip()

    user_query = ""
    identified_issue_from_image = None

    if input_choice == 'exit':
        print("Goodbye! Happy repairing!")
        break
    elif input_choice == 'image':
        image_path = ""
        while not image_path.strip():
            image_path = input("Please enter the full path to your image file: ").strip()
            if image_path.lower() == 'exit':
                break
        if image_path.lower() == 'exit':
            print("Goodbye! Happy repairing!")
            break

        if image_path:
            identified_issue_from_image = analyze_image_for_repair(image_path)
            if identified_issue_from_image:
                user_query = f"I have {identified_issue_from_image}. Can you help me fix this?"
                print(f"Agent will process: '{identified_issue_from_image}' based on your image.")
            else:
                print("Could not process image or identify an issue from the provided path. Please try describing your problem in text instead.")
                continue

        else:
            print("No image path provided. Please try again.")
            continue

    elif input_choice == 'text':
        user_query = ""
        while not user_query.strip():
            user_query = input("\nYou (Please describe your home repair issue): ")
            if user_query.lower() == 'exit':
                break
        if user_query.lower() == 'exit':
            print("Goodbye! Happy repairing!")
            break

    else:
        print("Invalid choice. Please type 'text' or 'image'.")
        continue

    if not user_query:
        continue

    chat_history.append(("human", user_query))

    raw_response = agent_executor.invoke({"query": user_query, "chat_history": chat_history})

    try:
        # LangChain's invoke() for tool-calling agents often returns a dict with 'output' key directly.
        agent_output_text = raw_response.get("output")
        if not agent_output_text:
            raise ValueError("Agent returned empty output or unexpected format.")

        structured_response = parser.parse(agent_output_text)

        # Logic for Clarification or Full Advice 
        if structured_response.type == "clarification" and structured_response.clarification_question:
            print("\n🤔 I need a bit more information to help you effectively.")
            print(f"Question: {structured_response.clarification_question}")
            print(f"Reason: {structured_response.clarification_reason}")
            # Add the clarification question to history so the agent remembers it
            chat_history.append(("ai", f"I need more info: {structured_response.clarification_question} (Reason: {structured_response.clarification_reason})"))
            print("\nPlease provide more details.")
            continue # Skip the rest of this iteration and go back to ask for user input

        else: # This block is for when the type is "advice" (or default)
            # Add the agent's (parsed) response to chat history for future turns
            chat_history.append(("ai", f"Okay, based on your description, my diagnosis is: {structured_response.diagnosis}"))

            print("\n🛠️ DIY Repair Advice\n----------------------")
            print(f"Issue Type: {structured_response.issue_type}")
            print(f"\nDiagnosis:\n{structured_response.diagnosis}")

            if structured_response.diy_steps:
                print("\nSteps to Fix:")
                for i, step in enumerate(structured_response.diy_steps):
                    print(f"- {step}")
            else:
                print("\nNo specific DIY steps provided for this issue (perhaps consult a professional?).")

            if structured_response.materials_needed:
                print("\nMaterials Needed:")
                for item in structured_response.materials_needed:
                    print(f"- {item}")
            else:
                print("\nNo specific materials listed.")

            if structured_response.safety_tips:
                print("\nSafety Tips:")
                for tip in structured_response.safety_tips:
                    print(f"- {tip}")
            else:
                print("\nNo specific safety tips provided.")

            print("\n----------------------")
            print("I hope this detailed advice helps you with your repair! Always prioritize safety.")
            print("If you have any more questions or need further assistance, just ask!")

    except Exception as e:
        print("\nAn internal error occurred while processing my advice. This is likely due to a misformatted response from my side.")
        print("Could you please try describing your issue again, perhaps with slightly different words?")
        print(f"DEBUG: Error details: {e}")
        error_message = "I'm sorry, I couldn't understand my own generated response. Please try again."
        chat_history.append(("ai", error_message))