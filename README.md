#**RepairAgent**
A DIY household repair agent that can take in images and text, classify what is wrong, and give steps on how to repair it.


**Features**
Conversational AI: Interact with an AI assistant to discuss home repair problems.

DIY Advice: Get diagnoses, repair steps, material lists, and safety tips for common issues like damp, cracks, and stains.

Intelligent Clarification: If the AI needs more information, it will ask specific follow-up questions.

Basic Image Analysis: Upload a photo of your problem (e.g., a wall with mold) and the system will attempt to describe it to the AI.

Note on Image Analysis: The image detection is not very good. It uses very basic image processing and is primarily for demonstrating the workflow from image input to AI processing, not for accurate diagnosis.

External Tool Use: The AI can use a Wikipedia search tool to gather additional information.

Powered by Gemini: Uses Google's Gemini LLM for AI capabilities.

**1. Prerequisites**
Before you begin, make sure you have the following installed on your system:
Python 3.8 or newer: You can download it from the official Python website.

**2. Create Project Files**
You will need to create three specific Python files and one text file in your project's main folder: main.py, tools.py, requirements.txt, and .env.

main.py: This is the core application file. Create a file named main.py in the root of your project directory. Its content includes the main conversational logic, the setup for the AI model (Gemini), the Pydantic model for structured output, and the function for rudimentary image analysis.

tools.py: This file defines the external tools your AI can use. Create a file named tools.py in the root of your project directory. It contains the definition for the Wikipedia search tool that the AI can call upon.

requirements.txt: This file lists all the necessary Python libraries that your project depends on. Create a file named requirements.txt in the root of your project directory and include a list of essential packages like python-dotenv, langchain, langchain-core, pydantic, langchain-community, wikipedia, opencv-python, and langchain-google-genai.

.env: This special file will securely store your API key. Create a new file named .env in the root of your project directory (note the dot at the beginning, which often makes it a hidden file).

**3. Get Your Google Gemini API Key**
Your project needs an API key to communicate with the Google Gemini model.

Obtain an API Key: Navigate to the Google AI Studio website (you can find it by searching for "Google AI Studio" or directly via aistudio.google.com/app/apikey) or the Google Cloud Console. Follow their instructions to create a new API key for yourself.

Add to .env: Open the .env file you created in your project's main folder using a text editor. Add the following line to it, making sure to replace "YOUR_GEMINI_API_KEY_HERE" with the actual API key you just obtained. Remember to keep the quotation marks around your key.

GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
Save the .env file.

**4. Install Dependencies**
It is strongly recommended to use a Python virtual environment to manage the project's dependencies. This keeps the project's specific libraries isolated from your system's global Python packages.

Create a virtual environment: In your terminal, ensure you are in your project's main folder (the one containing main.py). Then, run the command to create a virtual environment named venv:

python -m venv venv
Activate the virtual environment: You need to activate this environment each time you work on the project to ensure you're using the correct installed libraries.

On Windows: In your terminal, run:

venv\Scripts\activate
On macOS/Linux: In your terminal, run:

source venv/bin/activate
You will know it's activated because (venv) will typically appear at the beginning of your terminal prompt.

Install the required packages: With the virtual environment active, install all the libraries listed in your requirements.txt file by running:

pip install -r requirements.txt

**5. (Optional) Prepare Test Images**
If you plan to use the image analysis feature, it's good practice to organize your test images in a dedicated subfolder.

In your project's main folder, create a new folder named images. You can do this using your file explorer or by running mkdir images in your terminal.

Place any images you want to test (e.g., photos of damp walls, cracks, or stains) into this newly created images folder.

Your project directory structure should now resemble this:

your_project_folder/
├── main.py

├── tools.py

├── requirements.txt

├── .env

├── venv/ (This folder is created automatically by the virtual environment setup)

└── images/

    ├── your_test_image1.jpg

    └── your_test_image2.png

How to Run the Application
Now that everything is set up, you can run the DIY Home Repair Assistant and start interacting with it.

Ensure your virtual environment is activated. If you closed your terminal or started a new one, remember to activate your virtual environment again as shown in step 4 of "Install Dependencies".

Navigate to your project's main folder in your terminal (the directory where your main.py file is located).

Run the script: Execute the main application file using Python:

python main.py
Follow the prompts in the terminal:

The assistant will greet you and ask how you'd like to describe your issue.

For text input: Type text when prompted, press Enter, and then type your problem description (e.g., "There's a dark stain on my bathroom ceiling").

For image input: Type image when prompted, press Enter. The assistant will then ask for the file path. Provide the path to your image relative to your project's main folder. For example, if your image is named damp_wall.jpg and it's located inside the images subfolder, you would type:

On Windows: images\damp_wall.jpg

On macOS/Linux: images/damp_wall.jpg (forward slashes usually work on Windows too)

The AI will process your request. It will either provide a diagnosis, DIY steps, a list of materials needed, and safety tips, or it might ask for more specific clarification if your initial description is too vague.

To exit the application at any time, simply type exit when prompted for input and press Enter.


**Important Notes**
Rudimentary Image Analysis: Please be aware that the analyze_image_for_repair function built into this project uses very basic image processing techniques (like analyzing pixel darkness or average brightness). It is not an advanced, intelligent computer vision system. Therefore, it will often provide generic or even incorrect identifications for complex visual problems. Its primary purpose here is to demonstrate how image input can be integrated into the AI's workflow, not to provide accurate visual diagnoses. For real-world, precise image-based diagnosis, more sophisticated machine learning models would be required.

API Usage Considerations: Your use of the Google Gemini API may be subject to usage limits and could incur costs depending on your query volume. It's advisable to review the official Gemini pricing documentation on the Google AI website for the latest information.

Safety First: The DIY home repair advice provided by this assistant is intended for general guidance only. Always prioritize safety when undertaking any home repair tasks. For complex, potentially dangerous (e.g., electrical, gas), or structural issues, it is highly recommended to consult with qualified professional contractors or technicians. This AI assistant is a helpful tool, but it should not replace expert human judgment.

For improvement to this model and integrating multiple different models (ie if you wanted to create a ML model trained on imaages of damages so the agent could accurately classify different types of damges (mould vs crack for example)) you can look into these images from roboflow that have image datasets:
https://universe.roboflow.com/bharati-vidhypeeth-college-of-engineering-pune/brick-crack-detection-2

https://universe.roboflow.com/project-kx3zs/wall-damage-monitoring

https://universe.roboflow.com/image-uhpot/property_defects

https://universe.roboflow.com/mould-detection/mould-detection-v3

https://universe.roboflow.com/my-4lxv5/cracks-detection-qgvtg
