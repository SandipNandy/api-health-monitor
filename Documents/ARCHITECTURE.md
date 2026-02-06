# System Architecture

## Overview
```mermaid
graph TB
    subgraph "Data Collection"
        A[GitHub Actions] --> B[Monitor Script]
        B --> C{API Endpoints}
        C --> D[Health Checks]
    end
    
    subgraph "Data Processing"
        D --> E[Results Processing]
        E --> F[Threshold Analysis]
        F --> G[Status Classification]
    end
    
    subgraph "Data Storage"
        G --> H[Google Sheets]
        G --> I[Local Cache]
    end
    
    subgraph "Output & Alerts"
        H --> J[GitHub Summary]
        H --> K[Email Reports]
        I --> L[Dashboard]
    end
    
    subgraph "Configuration"
        M[Environment Variables] --> B
        N[Config Files] --> B
    end