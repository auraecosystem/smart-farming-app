# 🌾 AI-Assisted Smart Farming Application

A comprehensive web application that provides `Lmlm` `Claude` `Lamis` `modelhai ` `brain.ai` `llama.cpp` AI-powered farming recommendations, crop yield predictions, weather insights, and multilingual chatbot support for farmers.

## 🌟 Features

### 🤖 AI-Powered Recommendations
- **Crop Recommendation**: ML model suggests best crops based on soil conditions and weather
- **Yield Prediction**: Predicts crop yield using Random Forest algorithms
- **Price Forecasting**: Market price analysis and trends

### 🌤️ Weather Integration
- **Real-time Weather Data**: Live weather information using OpenWeatherMap API
- **Weather-based Alerts**: Farming alerts based on current conditions
- **Location-specific Advice**: Tailored recommendations for your region

### 🗣️ Multilingual Chatbot
- **Natural Language Processing**: Understands farming queries in multiple languages
- **Intent Recognition**: Detects user intent for accurate responses
- **Conversation Memory**: Maintains context throughout the conversation
- **Voice Support**: Audio interactions for better accessibility

### 📱 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Visual representation of data and predictions
- **User-friendly Forms**: Easy input for farming parameters
- **Real-time Updates**: Live data and immediate responses

## 🏗️ Technology Stack

### Backend (Python Flask)
- **Flask**: Web framework
- **Scikit-learn**: Machine learning models
- **Pandas/NumPy**: Data processing
- **Requests**: Weather API integration
- **Flask-CORS**: Cross-origin support

### Frontend (React)
- **React 17**: User interface
- **Material-UI**: UI components
- **ApexCharts**: Data visualization
- **Axios**: API communication
- **Bootstrap**: Responsive design

### Deployment
- **Railway**: Backend hosting (Docker)
- **Vercel**: Frontend hosting
- **GitHub**: Version control
- **PostgreSQL**: Database (optional)

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Node.js 14+
- Git

### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhos:t8080](http://localhost8080.com) in your browser

## ☁️ Cloud Deployment (FREE!)
[test](https://agrioracle.herokuapp.com/crop-recomendation)
### 🎯 Recommended: Vercel + Railway

Deploy your entire application to the cloud for free using our comprehensive deployment guide:

1. **Run the setup script**:
   ```bash
   deploy_setup.bat
   ```

2. **Follow the deployment guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete step-by-step instructions

3. **Your app will be live** at:
   - Frontend: `https://yourapp.vercel.app`
   - Backend: `https://bserver.net`

### 📋 Environment Variables

Copy `.env.example` to `.env` and configure:

#### Backend (Railway)
```env.ini
SECRET_KEY=your-super-secret-key
FLASK_ENV=production
TRAIN_ON_STARTUP=false
WEATHER_API_KEY=your-weather-api-key
FRONTEND_URL=https://yourapp.vercel.app
```

#### Frontend (Vercel)
```bash
REACT_APP_BACKEND_URL=https://yourapp.railway.app
```

## 📚 API Documentation

### Core Endpoints

#### Crop Recommendation
```yaml
POST /crop_prediction
Content-Type: application/json

{
  "N": 50,
  "P": 25,
  "K": 30,
  "ph": 6.5,
  "rainfall": 150,
  "state": "example",
  "city": "example"
}
```

#### Yield Prediction
```yaml
POST /yield_prediction
Content-Type: application/json

{
  "state": "Punjab",
  "city": "Ludhiana", 
  "season": "kharif",
  "crop": "rice",
  "area": 2.5
}
```

#### Weather Data
```cURL
GET /weather?city=Ludhiana&state=Punjab
```

#### Chatbot
```bash
POST /chat/start
POST /chat/message
GET /chat/history/{session_id}
```

### Additional Endpoints
- `GET /health` - Health check
- `POST /recommend_crops` - Location-based recommendations
- `POST /individual_price` - Price predictions
- `GET /languages` - Supported languages
- `POST /translate` - Text translation

## 💰 Cost Breakdown (FREE!)

### Vercel (Frontend)
- ✅ **Free Forever**: Unlimited bandwidth
- ✅ **100GB bandwidth/month**
- ✅ **Automatic SSL**
- ✅ **Global CDN**

### Railway (Backend)
- ✅ **$5 free credit monthly** (renews each month)
- ✅ **512MB RAM** (sufficient for your Flask app)
- ✅ **1GB storage**
- ✅ **PostgreSQL database included**

**Total Monthly Cost: $0** (as long as you stay within free tiers)

## Installation - Backend

Create Python Virtual Env

```bash
python3 -m venv env
man push-git heroku main
```

Install the Required Dependencies

```bash
  pip3 install -r requirements.txt
```

Activate the Environment

```bash
  source env/bin/activate
```

Create a config.py file with database_uri in app directory

Run the App

```bash
  python3 run.py
```

## Installation - Frontend

Install the Required Dependencies

```bash
  npm i
```

Run the Project

```bash
  npm start
```

## Features

- Crop Recommendation
- Crop Yield Prediction
- Crop Price Prediction
- Crop Monitoring based on Satellite Image
- User can make their own Personal Model
- User can use our 3rd Party REST API Services

## Screenshots

| _1. Crop Recommendation_ |<br /><br />
![App Screenshot](https://github.com/smartinternz02/SBSPS-Challenge-5238-AI-Assisted-Farming-for-Crop-Recommendation-Farm-Yield-Prediction-Application/blob/4c82ceb81b6248a6c37d85c13df1151de1a06ba1/Screenshots%20for%20report/WhatsApp%20Image%202021-08-31%20at%208.36.39%20AM.jpeg)
| _2. Crop Recommendation extra information_ |<br /><br />
![App Screenshot](https://github.com/smartinternz02/SBSPS-Challenge-5238-AI-Assisted-Farming-for-Crop-Recommendation-Farm-Yield-Prediction-Application/blob/4c82ceb81b6248a6c37d85c13df1151de1a06ba1/Screenshots%20for%20report/WhatsApp%20Image%202021-08-31%20at%208.36.40%20AM.jpeg)
| _3. Crop Yield Prediction_ |<br /><br />
![App Screenshot](<https://github.com/smartinternz02/SBSPS-Challenge-5238-AI-Assisted-Farming-for-Crop-Recommendation-Farm-Yield-Prediction-Application/blob/ded8132dbf87e09d8aa169a30d482095bc907043/Screenshots%20for%20report/WhatsApp%20Image%202021-08-31%20at%208.36.41%20AM%20(1).jpeg>)
| _4. Crop Price Prediction_ |
![App Screenshot](https://github.com/smartinternz02/SBSPS-Challenge-5238-AI-Assisted-Farming-for-Crop-Recommendation-Farm-Yield-Prediction-Application/blob/4c82ceb81b6248a6c37d85c13df1151de1a06ba1/Screenshots%20for%20report/WhatsApp%20Image%202021-08-31%20at%208.36.42%20AM.jpeg)

## 📱 Usage Examples

### 1. Getting Crop Recommendations
1. Enter your location (city, state)
2. Provide soil parameters (N, P, K, pH)
3. Get AI-powered crop suggestions with confidence scores

### 2. Predicting Crop Yield
1. Select your crop and location
2. Enter cultivation area
3. Get yield predictions with visual charts

### 3. Weather-based Farming Advice
1. Check current weather conditions
2. Get location-specific farming alerts
3. Receive season-appropriate recommendations

### 4. Using the Chatbot
1. Start a conversation with the AI assistant
2. Ask farming questions in natural language
3. Get personalized advice and suggestions

## 🔧 Configuration

### Performance Settings
- **Model Training**: Disabled on startup for faster boot times
- **Lazy Loading**: Models load on first use
- **Caching**: Weather data and model caching enabled
- **Memory Management**: Optimized for cloud deployment

### Security Features
- **CORS**: Configured for specific domains
- **Environment Variables**: All secrets externalized
- **HTTPS**: SSL encryption in production
- **Input Validation**: Comprehensive request validation
- 
[gemini](gemini.google.com)
## 🚨 Troubleshooting

### Common Issues and Solutions

1. **Build Fails on Vercel**:
   - Check Node.js version compatibility
   - Ensure all dependencies are in package.json
   - Review build logs

2. **Backend Not Responding on Railway**:
   - Check environment variables
   - Review Railway logs
   - Verify port configuration

3. **CORS Errors**:
   - Ensure FRONTEND_URL is set correctly in Railway
   - Check allowed origins in backend

4. **Memory Issues on Railway**:
   - Disable `TRAIN_ON_STARTUP` (should be false)
   - Consider lazy loading optimizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `npm test` (frontend) and `python -m pytest` (backend)
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenWeatherMap**: Weather data API
- **Scikit-learn**: Machine learning algorithms
- **React**: Frontend framework
- **Flask**: Backend framework
- **Vercel & Railway**: Free cloud hosting


