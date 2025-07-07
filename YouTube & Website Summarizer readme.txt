# YouTube & Website Summarizer

A Streamlit web application that uses LangChain and Groq AI to automatically summarize content from YouTube videos and websites.

## 📋 What It Does

This application allows users to:
- **Summarize YouTube videos** by extracting transcripts and generating concise summaries
- **Summarize website content** by scraping and processing web pages
- **Generate 300-word summaries** using advanced AI language models
- **User-friendly interface** with real-time processing status

## 🛠️ Major Components

### **Frontend & UI**
- **Streamlit**: Web framework for creating the interactive user interface
- **Validators**: URL validation to ensure proper input format

### **AI & Language Processing**
- **LangChain**: Framework for building AI-powered applications
  - `PromptTemplate`: Structures prompts for consistent AI responses
  - `load_summarize_chain`: Pre-built summarization pipeline
- **ChatGroq**: Groq API integration using Gemma2-9b-it model

### **Content Loaders**
- **YoutubeLoader**: Extracts transcripts from YouTube videos
- **UnstructuredURLLoader**: Scrapes and processes website content

### **Configuration & Security**
- **dotenv**: Environment variable management for API keys
- **os**: Operating system interface for environment variables

## 🚀 Features

### **Smart URL Processing**
- Automatically detects YouTube vs website URLs
- Handles multiple YouTube URL formats (`youtube.com`, `youtu.be`)
- Cleans URLs by removing tracking parameters

### **Robust Error Handling**
- Input validation for URLs and API keys
- Specific error messages for different failure types
- Graceful handling of API service interruptions

### **Security**
- API key input with password masking
- SSL verification options for web scraping
- Custom headers to avoid bot detection

## 📦 Dependencies

```python
streamlit          # Web application framework
langchain         # AI application framework
langchain-groq    # Groq API integration
langchain-community # Community loaders
validators        # URL validation
python-dotenv     # Environment variable management
```

## 🔧 Setup Requirements

1. **Groq API Key**: Required for AI summarization
2. **Python Environment**: Python 3.7+ recommended
3. **Internet Connection**: For accessing YouTube and websites

## 💡 How It Works

1. **User Input**: Enter YouTube URL or website URL
2. **URL Processing**: Application detects content type and cleans URL
3. **Content Loading**: 
   - YouTube: Extracts video transcript
   - Website: Scrapes webpage content
4. **AI Processing**: Groq AI generates 300-word summary
5. **Output**: Displays formatted summary to user

## 🎯 Use Cases

- **Educational**: Quickly summarize educational videos and articles
- **Research**: Extract key points from multiple sources
- **Content Creation**: Generate summaries for content curation
- **Time-Saving**: Get key insights without consuming full content

## 🔍 Technical Architecture

```
User Input → URL Validation → Content Loading → AI Processing → Summary Output
     ↓              ↓               ↓              ↓              ↓
  Streamlit    Validators    LangChain Loaders   Groq AI    Streamlit UI
```

## 🚦 Running the Application

```bash
streamlit run your_script_name.py
```

Access the application at `http://localhost:8501`

---

**Note**: This application requires valid Groq API credentials and internet access for optimal functionality.