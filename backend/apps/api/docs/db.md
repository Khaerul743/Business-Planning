# Database Schema Documentation

This document describes the PostgreSQL database schema for the project, including table structures, relationships, and data types.
**Note**: All IDs and Key relationships use `UUID` (v4).

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    Users ||--o{ Businesses : owns
    Businesses ||--o{ Agents : has
    Businesses ||--o{ Business_knowladges : has
    Businesses ||--o{ Conversations : has
    Businesses ||--o{ Human_Fallback : has
    Businesses ||--o{ Whatsapp_accounts : has
    Agents ||--o{ Agent_analytics : generates
    Agents ||--o{ Agent_configurations : has
    Agents ||--o{ Customers : manages
    Agents ||--o{ Document_knowladges : has
    Agents ||--o{ Conversations : handles
    Customers ||--o{ Conversations : participates_in
    Conversations ||--o{ Messages : contains
    Conversations ||--o{ Human_Fallback : triggers

    Users {
        uuid id PK
        string name
        string email
        string password
        string avatar
        enum role "admin, user"
        enum status "active, inactive"
        timestamp created_at
    }

    Businesses {
        uuid id PK
        uuid user_id FK
        string name
        string owner_name
        string phone_number
        string description
        string address
        timestamp created_at
        timestamp updated_at
    }

    Agents {
        uuid id PK
        uuid business_id FK
        string name
        string phone_number_id
        boolean enable_ai
        string fallback_to_human
        timestamp created_at
        timestamp updated_at
    }

    Agent_analytics {
        uuid id PK
        uuid agent_id FK
        date date
        bigint total_message
        double response_time
        bigint token
        boolean human_takeover
        text ai_response
        timestamp created_at
    }

    Agent_configurations {
        uuid id PK
        uuid agent_id FK
        string chromadb_path
        string collection_name
        string llm_provider
        string llm_model
        string base_prompt
        enum tone
        float temperature
        boolean include_memory
        string user_memory_id
        timestamp created_at
    }

    Business_knowladges {
        uuid id PK
        uuid business_id FK
        string category
        string category_description
        text content
        enum format "text, etc"
        timestamp created_at
        timestamp updated_at
    }

    Conversations {
        uuid id PK
        uuid business_id FK
        uuid agent_id FK
        uuid customer_id FK
        enum status "active, inactive"
        timestamp last_message_at
        timestamp created_at
    }

    Customers {
        uuid id PK
        uuid agent_id FK
        string wa_id
        string name
        string phone_number
        boolean enable_ai
        timestamp created_at
    }

    Document_knowladges {
        uuid id PK
        uuid agent_id FK
        string title
        string description
        string file_path
        bigint file_size
        enum status "processed, etc"
        enum file_format
        timestamp created_at
        timestamp updated_at
    }

    Human_Fallback {
        uuid id PK
        uuid business_id FK
        uuid conversation_id FK
        float confidence_level
        text last_decision_summary
        timestamp created_at
    }

    Messages {
        uuid id PK
        uuid conversation_id FK
        text content
        jsonb raw_webhook
        enum sender_type
        enum message_type "text, image, audio, file"
        timestamp created_at
    }

    Whatsapp_accounts {
        uuid id PK
        uuid business_id FK
        string waba_phone_number
        string waba_id
        string access_token
        enum status "active, etc"
        timestamp created_at
        timestamp updated_at
    }
```

## Tables Detail

### Users
- `id`: UUID (PK, gen_random_uuid())
- `name`: text
- `email`: text
- `password`: text
- `avatar`: text (Optional)
- `role`: USER-DEFINED (default 'user')
- `status`: USER-DEFINED (default 'active')

### Businesses
- `id`: UUID (PK, gen_random_uuid())
- `user_id`: UUID (FK -> Users.id)
- `name`: text
- `owner_name`: text (Optional)
- `phone_number`: text
- `description`: text
- `address`: text

### Agents
- `id`: UUID (PK)
- `business_id`: UUID (FK -> Businesses.id)
- `name`: text
- `phone_number_id`: text (Unique)
- `enable_ai`: boolean (default true)
- `fallback_to_human`: text

### Agent_configurations
- `id`: UUID (PK, gen_random_uuid())
- `agent_id`: UUID (FK -> Agents.id)
- `llm_provider`: text
- `llm_model`: text
- `tone`: USER-DEFINED
- `temperature`: real (default 0.7)

### Agent_analytics
- `id`: UUID (PK, gen_random_uuid())
- `agent_id`: UUID (FK -> Agents.id)
- `date`: date
- `total_message`: bigint
- `response_time`: double precision
- `token`: bigint
- `human_takeover`: boolean
- `ai_response`: text

### Customers
- `id`: UUID (PK, gen_random_uuid())
- `agent_id`: UUID (FK -> Agents.id)
- `phone_number`: text
- `wa_id`: text
- `name`: text (Optional)
- `enable_ai`: boolean (default true)

### Conversations
- `id`: UUID (PK, gen_random_uuid())
- `business_id`: UUID (FK -> Businesses.id)
- `agent_id`: UUID (FK -> Agents.id)
- `customer_id`: UUID (FK -> Customers.id)
- `status`: USER-DEFINED (default 'active')
- `last_message_at`: timestamp

### Messages
- `id`: UUID (PK, gen_random_uuid())
- `conversation_id`: UUID (FK -> Conversations.id)
- `content`: text
- `sender_type`: USER-DEFINED
- `message_type`: USER-DEFINED (default 'text')
- `raw_webhook`: jsonb
- `created_at`: timestamp

### Business_knowladges
- `id`: UUID (PK, gen_random_uuid())
- `business_id`: UUID (FK -> Businesses.id)
- `category`: text
- `category_description`: text
- `content`: text
- `format`: USER-DEFINED (default 'text')

### Document_knowladges
- `id`: UUID (PK, gen_random_uuid())
- `agent_id`: UUID (FK -> Agents.id)
- `title`: text
- `description`: text
- `file_path`: text
- `status`: USER-DEFINED (default 'processed')

### Human_Fallback
- `id`: UUID (PK, gen_random_uuid())
- `business_id`: UUID (FK -> Businesses.id)
- `conversation_id`: UUID (FK -> Conversations.id)
- `confidence_level`: double precision
- `last_decision_summary`: text

### Whatsapp_accounts
- `id`: UUID (PK, gen_random_uuid())
- `business_id`: UUID (FK -> Businesses.id presumably)
- `waba_phone_number`: text
- `waba_id`: text
- `access_token`: text
- `status`: USER-DEFINED (default 'active')
