# Math Problem Solver & Search Assistant

A Streamlit-based chatbot powered by GEMMA 2 (9B) that can solve mathematical problems, perform logical reasoning, and search Wikipedia for additional information.

## Features

- **Mathematical Problem Solving**: Solves complex math problems with step-by-step solutions
- **Logical Reasoning**: Handles reasoning-based questions with detailed explanations
- **Wikipedia Integration**: Searches Wikipedia for supplementary information
- **Interactive Chat Interface**: User-friendly chat-based interaction
- **Real-time Processing**: Live response generation with visual feedback

## Prerequisites

- Python 3.8+
- Groq API Key (for accessing GEMMA 2 model)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd math-chatbot
```

2. Install required packages:
```bash
pip install streamlit langchain-groq langchain langchain-community python-dotenv
```

3. Create a `.env` file in the root directory (optional):
```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the displayed URL (usually `http://localhost:8501`)

3. Enter your Groq API key in the sidebar

4. Type your mathematical question or logical problem in the text area

5. Click "Find my answers" to get the solution

## Example Questions

- "What is the derivative of x^2 + 3x + 2?"
- "How many units are in a dozen?"
- "Solve the quadratic equation 2x^2 + 5x - 3 = 0"
- "What is the capital of France?" (uses Wikipedia search)

## Tools Used

- **Calculator**: For mathematical computations using LLMMathChain
- **Reasoning Tool**: For logical problem-solving with custom prompts
- **Wikipedia Tool**: For information retrieval and fact-checking

## Configuration

The application uses the following LangChain components:
- **LLM**: ChatGroq with GEMMA 2-9B-IT model
- **Agent Type**: ZERO_SHOT_REACT_DESCRIPTION
- **Callback Handler**: StreamlitCallbackHandler for real-time updates

## Notes

- Ensure you have a valid Groq API key
- The application handles parsing errors gracefully
- Responses are displayed in both chat format and as highlighted success messages
- Chat history is maintained throughout the session

## Troubleshooting

- **API Key Issues**: Make sure your Groq API key is valid and has sufficient credits
- **Import Errors**: Ensure all required packages are installed
- **Model Access**: Verify that you have access to the GEMMA 2-9B-IT model through Groq