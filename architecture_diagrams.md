# Pune VMS System - Architecture Diagrams

## System Block Diagram

```mermaid
graph TB
    subgraph "External Systems"
        A[Iteris Vantage Argus API]
        B[VINOX VMS System]
        C[Traffic Sensors/Cameras]
    end
    
    subgraph "Pune VMS Backend"
        subgraph "API Gateway"
            D[Django REST Framework]
            E[Authentication Layer]
            F[CORS Middleware]
        end
        
        subgraph "Core Modules"
            G[Traffic Module]
            H[Incidents Module]
            I[Users Module]
            J[API Module]
        end
        
        subgraph "Services Layer"
            K[VINOX Service]
            L[Data Fetch Service]
            M[Message Broadcasting]
        end
        
        subgraph "Database Layer"
            N[PostgreSQL Database]
        end
    end
    
    subgraph "Client Applications"
        O[Traffic Management Dashboard]
        P[Mobile App]
        Q[Admin Panel]
    end
    
    subgraph "Physical Infrastructure"
        R[VMS Board 1-20]
        S[Traffic Signals]
        T[Intersection Controllers]
    end
    
    %% Data Flow Connections
    A --> L
    B --> K
    C --> G
    
    D --> G
    D --> H
    D --> I
    D --> J
    
    E --> D
    F --> D
    
    G --> N
    H --> N
    I --> N
    J --> N
    
    K --> B
    K --> R
    M --> K
    
    L --> N
    M --> N
    
    O --> D
    P --> D
    Q --> D
    
    R --> B
    S --> G
    T --> G
```

## Data Flow Diagram

```mermaid
flowchart TD
    subgraph "Data Sources"
        A1[Iteris API - Pairs Data]
        A2[Iteris API - Locations]
        A3[VINOX API - Players]
        A4[Traffic Sensors]
        A5[User Inputs]
    end
    
    subgraph "Data Processing"
        B1[fetch_data.py Script]
        B2[load_vms_boards.py Script]
        B3[Real-time Data Sync]
        B4[Data Validation]
        B5[Data Transformation]
    end
    
    subgraph "Database Operations"
        C1[Insert VMS Boards]
        C2[Update Traffic Data]
        C3[Log Incidents]
        C4[User Management]
        C5[Authentication Tokens]
    end
    
    subgraph "API Endpoints"
        D1[GET /vms-boards/]
        D2[GET /traffic-data/]
        D3[POST /incidents/]
        D4[POST /auth/login/]
        D5[POST /emergency-messages/]
    end
    
    subgraph "Output Actions"
        E1[Display Traffic Data]
        E2[Send Emergency Messages]
        E3[Update VMS Boards]
        E4[Generate Reports]
        E5[User Authentication]
    end
    
    %% Flow Connections
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B3
    A5 --> B4
    
    B1 --> B2
    B1 --> B5
    B3 --> B5
    B4 --> B5
    
    B2 --> C1
    B5 --> C2
    B4 --> C3
    B5 --> C4
    B4 --> C5
    
    C1 --> D1
    C2 --> D2
    C3 --> D3
    C4 --> D4
    C5 --> D5
    
    D1 --> E1
    D2 --> E1
    D3 --> E4
    D4 --> E5
    D5 --> E2
    E2 --> E3
```

## Authentication Flow Diagram

```mermaid
sequenceDiagram
    participant Client
    participant DjangoAPI
    participant AuthMiddleware
    participant UserDB
    participant TokenDB
    
    Client->>DjangoAPI: POST /auth/login/ (credentials)
    DjangoAPI->>AuthMiddleware: Check authentication
    AuthMiddleware->>UserDB: Validate user credentials
    UserDB-->>AuthMiddleware: User validation result
    AuthMiddleware-->>DjangoAPI: Authentication status
    
    alt Valid Credentials
        DjangoAPI->>TokenDB: Generate/retrieve token
        TokenDB-->>DjangoAPI: Authentication token
        DjangoAPI-->>Client: Token + User data
    else Invalid Credentials
        DjangoAPI-->>Client: 401 Unauthorized
    end
    
    Client->>DjangoAPI: API Request (with token)
    DjangoAPI->>AuthMiddleware: Validate token
    AuthMiddleware->>TokenDB: Verify token
    TokenDB-->>AuthMiddleware: Token validation
    AuthMiddleware-->>DjangoAPI: User context
    DjangoAPI-->>Client: API Response
```

## Emergency Message Broadcasting Flow

```mermaid
flowchart TD
    subgraph "Message Creation"
        A[User creates emergency message]
        B[Validate user permissions]
        C[Format message content]
    end
    
    subgraph "Message Processing"
        D[Determine target boards]
        E[Prioritize message]
        F[Queue for delivery]
    end
    
    subgraph "VINOX Integration"
        G[Authenticate to VINOX]
        H[Send message via API]
        I[Receive delivery confirmation]
    end
    
    subgraph "Physical Display"
        J[VINOX processes message]
        K[Broadcast to VMS boards]
        L[Display on physical boards]
    end
    
    subgraph "Logging & Monitoring"
        M[Log message delivery]
        N[Track display status]
        O[Generate reports]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    I --> M
    M --> N
    N --> O
```

## Incident Management Workflow

```mermaid
stateDiagram-v2
    [*] --> Incident Detected
    Incident Detected --> Incident Logged
    Incident Logged --> Under Investigation
    Under Investigation --> Resolved
    Under Investigation --> Escalated
    Escalated --> Under Investigation
    Resolved --> Closed
    Closed --> [*]
    
    Incident Detected: Sensor/User Report
    Incident Logged: Database Entry
    Under Investigation: Analysis Phase
    Escalated: High Priority
    Resolved: Issue Fixed
    Closed: Documentation Complete
```

## Database Schema Relationships

```mermaid
erDiagram
    User ||--o{ UserProfile : has
    User ||--o{ Incident : resolves
    UserProfile ||--o{ VMSBoard : manages
    
    Intersection ||--o{ Signal : contains
    Intersection ||--o{ TrafficData : generates
    Intersection ||--o{ VMSBoard : located_at
    
    Route ||--o{ TravelTime : has
    
    VMSBoard {
        int board_id PK
        string vms_player_name
        string corridor_name
        int pair_id
        string location
        decimal latitude
        decimal longitude
        boolean is_active
        datetime last_update
    }
    
    Intersection {
        int id PK
        string name
        decimal latitude
        decimal longitude
        string location_description
        string zone
        boolean is_active
        int signal_count
        int camera_count
    }
    
    Signal {
        int id PK
        string signal_id UK
        string current_phase
        int cycle_time
        int green_time
        int red_time
        int yellow_time
        string controlled_by
        boolean is_active
        int battery_level
        datetime last_changed
        int intersection_id FK
    }
    
    Incident {
        int id PK
        string incident_type
        string location
        decimal latitude
        decimal longitude
        int severity
        text description
        string detected_by
        datetime detected_at
        boolean resolved
        datetime resolved_at
        int resolved_by FK
        text resolution_notes
    }
    
    TrafficData {
        int id PK
        int intersection_id FK
        int vehicle_count
        float average_speed
        string congestion_level
        string source
        datetime timestamp
    }
    
    TravelTime {
        int id PK
        int route_id FK
        float distance_km
        float average_speed_kmh
        float travel_time_minutes
        string congestion_level
        string source
        datetime timestamp
    }
    
    User {
        int id PK
        string username UK
        string email
        string password
        boolean is_active
        boolean is_staff
        boolean is_superuser
    }
    
    UserProfile {
        int id PK
        int user_id FK
        string role
        string phone
        string department
        boolean is_active
        datetime created_at
        datetime updated_at
    }
```

## API Request-Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant Django
    participant Middleware
    participant ViewSet
    participant Database
    participant ExternalAPI
    
    Client->>Django: HTTP Request
    Django->>Middleware: Process Request
    Middleware->>Middleware: CORS Check
    Middleware->>Middleware: Auth Check
    Middleware-->>Django: Request Validated
    
    Django->>ViewSet: Route to View
    ViewSet->>Database: Query Data
    
    alt External Data Needed
        ViewSet->>ExternalAPI: API Call
        ExternalAPI-->>ViewSet: Response Data
    end
    
    Database-->>ViewSet: Data Results
    ViewSet->>ViewSet: Serialize Data
    ViewSet-->>Django: Response
    Django-->>Client: HTTP Response
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Web Server"
            A[Nginx/Apache]
        end
        
        subgraph "Application Server"
            B[Django Application]
            C[Gunicorn/uWSGI]
        end
        
        subgraph "Database"
            D[PostgreSQL Server]
            E[Redis Cache]
        end
        
        subgraph "External Services"
            F[Iteris API]
            G[VINOX System]
        end
    end
    
    subgraph "Monitoring & Logging"
        H[Application Logs]
        I[Performance Metrics]
        J[Error Tracking]
    end
    
    A --> B
    B --> C
    C --> D
    B --> E
    B --> F
    B --> G
    
    B --> H
    C --> I
    B --> J
```

## Key System Components Summary

### 1. **Frontend Layer**
- Traffic Management Dashboard
- Mobile Applications
- Admin Control Panel

### 2. **API Gateway**
- Django REST Framework
- Authentication & Authorization
- CORS Handling
- Request Validation

### 3. **Business Logic Layer**
- Traffic Management Module
- Incident Management Module
- User Management Module
- External API Integration

### 4. **Data Layer**
- PostgreSQL Database
- Redis Caching
- File Storage

### 5. **External Integrations**
- Iteris Vantage Argus API
- VINOX VMS System
- Traffic Sensors

### 6. **Infrastructure**
- Web Servers
- Application Servers
- Database Servers
- Monitoring Systems

This architecture provides a scalable, maintainable, and robust system for managing Pune's Variable Message Sign infrastructure with real-time data processing and emergency response capabilities.
