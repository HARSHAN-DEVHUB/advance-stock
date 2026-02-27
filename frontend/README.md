# Frontend

React-based web interface for the Stock Prediction API.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Backend API running on port 8000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

This will start the Vite development server on `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` folder.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx      # Dashboard overview
│   │   ├── PredictForm.jsx    # Prediction form
│   │   ├── TrainModel.jsx     # Model training controls
│   │   └── StockData.jsx      # Data viewer
│   ├── styles/
│   │   ├── App.css           # Main styles
│   │   └── index.css         # Global styles
│   ├── App.jsx               # Main app component
│   └── main.jsx              # Entry point
├── index.html
├── vite.config.js
└── package.json
```

## ✨ Features

- 📊 **Dashboard**: View API status and model information
- 🔮 **Predictions**: Make stock price predictions with technical indicators
- 🎯 **Training**: Fetch data and train models
- 📈 **Data Viewer**: Browse raw and processed stock data
- 📱 **Responsive Design**: Works on mobile and desktop
- 🎨 **Modern UI**: Clean, professional interface

## 🛠️ Technologies

- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Recharts**: Data visualization
- **Lucide React**: Modern icons
- **Axios**: HTTP client

## 🌐 API Integration

The frontend connects to the backend API through a proxy configured in `vite.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),
  },
}
```

All API calls are made to `/api/*` which proxies to `http://localhost:8000/*`

## 📝 Usage

1. Start the backend API first:
   ```bash
   cd ../backend
   python start.py
   ```

2. Start the frontend:
   ```bash
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

## 🎨 Customization

### Colors

Edit CSS variables in `src/styles/index.css`:

```css
:root {
  --primary: #0066ff;
  --success: #28a745;
  --danger: #dc3545;
  /* ... */
}
```

### Adding New Components

1. Create a new `.jsx` file in `src/components/`
2. Import and use it in `App.jsx`
3. Add styling in `src/styles/App.css`

## 🐛 Troubleshooting

### CORS Errors
Make sure the backend has CORS enabled for `http://localhost:3000`

### API Not Found
Verify the backend is running on port 8000

### Build Errors
Delete `node_modules` and `package-lock.json`, then run `npm install` again
