# API Health Monitoring System 🚀

A production-ready API health monitoring system that demonstrates TPM (Technical Program Manager) skills including cross-functional collaboration, technical execution, and stakeholder management.

## It's under continous improvement, Updates are on pipeline ##

## 📊 Live Dashboard
[Google Sheets Dashboard](https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID) | [GitHub Actions](https://github.com/yourusername/api-health-monitor/actions)

## 🎯 Business Impact
- **90% reduction** in manual API verification time (from 10 hours/week to 1 hour/week)
- **Data-driven deployment decisions** with automated Go/No-Go signals
- **Real-time visibility** for engineering and product teams

## 🏗️ Architecture

### System Design



### Key Components
1. **Monitor Agent**: Multi-threaded HTTP client with timeout handling
2. **Data Processor**: SLI/SLO evaluation and classification
3. **Google Sheets Integration**: Real-time dashboard updates
4. **GitHub Actions**: Reliable scheduling and execution

## 🔧 Technical Implementation

### Data Flow
1. **Collection**: HTTP requests to configured endpoints every 15 minutes
2. **Analysis**: Response validation against SLI thresholds (latency, availability)
3. **Storage**: Results written to Google Sheets with timestamp and metadata
4. **Alerting**: Automated notifications for critical failures

### Configuration
```yaml
# .env configuration
API_ENDPOINTS=["https://api.github.com", "https://httpbin.org/status/200"]
GOOGLE_SHEET_NAME="API_Health_Log"
CHECK_INTERVAL=15  # minutes
LATENCY_WARNING=500  # ms
LATENCY_CRITICAL=1000  # ms
