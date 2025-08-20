# AI-Powered Workflow Creator

A sophisticated AI-powered workflow creation system that leverages Google's Gemini AI to generate comprehensive, industry-agnostic workflows and enquiry management systems. Built with FastAPI and designed for multi-language support.

## 🚀 Features

- **AI-Powered Workflow Generation**: Uses Google Gemini 2.0 Flash to create detailed, structured workflows
- **Multi-Language Support**: Supports English, Malayalam, Hindi, and Arabic
- **Industry-Agnostic**: Adaptable to any business domain or industry
- **Comprehensive Workflow Management**: Includes team assignments, role definitions, and progress tracking
- **RESTful API**: FastAPI-based backend with CORS support
- **Docker Support**: Containerized deployment ready
- **JSON Output**: Structured, machine-readable workflow definitions

## 🏗️ Architecture

The system consists of several key components:

- **FastAPI Backend**: RESTful API endpoints for workflow generation
- **Gemini AI Integration**: Google's latest AI model for intelligent workflow creation
- **Multi-Language Engine**: Language-specific prompt management and response generation
- **Workflow Engine**: Structured workflow definition and management system

## 📋 Prerequisites

- Python 3.9+
- Google Gemini AI API key
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vertex
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t vertex-workflow-creator .
   ```

2. **Run the container**
   ```bash
   docker run -p 8080:8080 -e GEMINI_API_KEY="your_api_key_here" vertex-workflow-creator
   ```

## 🔧 Configuration

### API Configuration

The system uses Google Gemini AI with the following configuration:
- **Model**: `gemini-2.0-flash-exp`
- **Temperature**: 1.0
- **Max Output Tokens**: 10,240
- **Response Format**: JSON

### Language Support

The system supports multiple languages through specialized prompts:
- **English**: Default language with comprehensive workflow generation
- **Malayalam**: Localized prompts for Malayalam-speaking users
- **Hindi**: Hindi language support with cultural context
- **Arabic**: Arabic language support with RTL considerations

## 📚 API Endpoints

### POST `/workflow`

Generate a new workflow based on user input.

**Request Body:**
```json
{
  "message": "Create a wedding planning workflow",
  "language": "english",
  "history": []
}
```

**Response:**
```json
{
  "workflow": {
    "enquiry_id": "12345",
    "category": "Event Management",
    "enquiry_details": {...},
    "workflow_details": {...},
    "overall_status": {...}
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### GET `/history`

Retrieve workflow generation history.

## 🎯 Usage Examples

### Basic Workflow Generation

```python
import requests

url = "http://localhost:8080/workflow"
data = {
    "message": "Create a software development project workflow",
    "language": "english"
}

response = requests.post(url, json=data)
workflow = response.json()
print(workflow)
```

### Multi-Language Support

```python
# Malayalam workflow
malayalam_data = {
    "message": "വെഡ്ഡിംഗ് പ്ലാനിംഗ് വർക്ക്ഫ്ലോ ഉണ്ടാക്കുക",
    "language": "malayalam"
}

# Hindi workflow
hindi_data = {
    "message": "वेडिंग प्लानिंग वर्कफ्लो बनाएं",
    "language": "hindi"
}
```

## 🔍 Workflow Structure

Each generated workflow includes:

- **Enquiry Details**: Client information and requirements
- **Workflow Steps**: Numbered, sequential process steps
- **Team Assignments**: Role-based team structure
- **Input Fields**: Required data collection points
- **Communication Templates**: Pre-built email templates
- **Progress Tracking**: Status and completion metrics

## 🚀 Deployment

### Production Considerations

- Set appropriate CORS origins for production
- Use environment variables for API keys
- Implement proper logging and monitoring
- Consider rate limiting for API endpoints
- Set up health checks and monitoring

### Environment Variables

```bash
GEMINI_API_KEY=your_gemini_api_key
PORT=8080
HOST=0.0.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## 🔮 Future Enhancements

- **Workflow Templates**: Pre-built templates for common industries
- **Progress Tracking**: Real-time workflow progress monitoring
- **Integration APIs**: Connect with popular project management tools
- **Advanced Analytics**: Workflow performance metrics and insights
- **Mobile App**: Native mobile application for workflow management

---

**Built with ❤️ using FastAPI and Google Gemini AI**