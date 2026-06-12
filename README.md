# 🌿 Smart-Farming

A Python-based intelligent farming system that leverages data-driven insights and machine learning to optimize agricultural operations and enhance crop yield.

## 📋 Overview

Smart-Farming is a comprehensive agricultural intelligence platform built with Python and Streamlit. It provides real-time monitoring, analysis, and predictions to help farmers make data-driven decisions for better crop management and resource optimization.

## ✨ Features

- 📊 **Real-time Monitoring** - Track current farm conditions and metrics
- 📈 **Data Analytics** - Analyze historical farm data and trends
- 🤖 **ML-Powered Predictions** - Machine learning models for crop yield prediction
- 🎨 **Interactive Dashboard** - User-friendly Streamlit web interface
- 💾 **Data Management** - Synthetic data generation and management
- 🔧 **Utilities** - Helper functions for data processing and analysis

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Interactive web dashboard framework
- **Machine Learning** - Data-driven predictions and analysis
- **Data Processing** - Pandas, NumPy for data manipulation

## 📁 Project Structure

```
Smart-Farming/
├── 1_🌿_État_actuel.py          # Main dashboard page
├── pages/                        # Additional Streamlit pages
├── models/                       # Machine learning models
├── data/                         # Data storage and datasets
├── utils.py                      # Utility functions
├── generate_synthetic_data.py    # Synthetic data generation
├── requirements.txt              # Python dependencies
├── railway.toml                  # Deployment configuration
└── .streamlit/                   # Streamlit configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnesDev/Smart-Farming.git
   cd Smart-Farming
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit dashboard:
```bash
streamlit run 1_🌿_État_actuel.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 Usage

### Generate Synthetic Data
Create test datasets for development:
```bash
python generate_synthetic_data.py
```

### Access Features
- Navigate through the dashboard using the sidebar menu
- View current farm status on the main page
- Explore additional features via pages in the `pages/` directory
- Check predictions and analytics for farm insights

## 📦 Dependencies

Key packages used in this project:
- `streamlit` - Web framework for data apps
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- Plus additional ML and data processing libraries (see `requirements.txt`)

## 🌱 Features in Development

- Advanced predictive models for disease detection
- Integration with IoT sensors
- Weather forecast integration
- Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is currently unlicensed. Please add a LICENSE file if you plan to distribute it.

## 🔗 Deployment

The project includes a `railway.toml` configuration file for easy deployment on Railway platform.

## 📧 Contact

For questions or suggestions, please reach out via GitHub Issues.

---

**Happy Farming! 🚜🌾**
