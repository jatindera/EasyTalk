# DB Schema
## DB Name: <span style="color:green">EasyTalk</span>

| Table Name               | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| users                | Stores information about registered users.                              |
| user_sessions        | Tracks active user sessions, including tokens and session metadata.     |
| roles_permissions    | Defines roles and associated permissions for access control.            |
| user_roles           | Defines roles and associated permissions for access control.            |
| chat_sessions        | Manages ongoing chat sessions for users.                               |
| chat_history         | Records the conversation history between users and AI.                 |
| chat_metadata        | Stores metadata related to chat sessions (e.g., timestamps, context).   |
| ai_models            | Contains information about available AI models used in chats.          |

# 1. Table: users

| Column Name   | Data Type   | Description                                                   |
|---------------|-------------|---------------------------------------------------------------|
| user_id       | INT         | Primary key, auto-incremented, unique identifier for each user.|
| email         | VARCHAR(255)| User's email address, unique and required.                    |
| first_name    | VARCHAR(100)| User's first name (optional).                                 |
| last_name     | VARCHAR(100)| User's last name (optional).                                  |
| provider      | VARCHAR(50) | Indicates which authentication provider is used (e.g., Google, Azure). |
| provider_id   | VARCHAR(255)| Unique identifier from the authentication provider (e.g., Google ID). |
| role          | VARCHAR(50) | User's role in the system (default is 'user', e.g., admin, user). |
| created_at    | DATETIME    | Timestamp for when the user account was created.              |
| updated_at    | DATETIME    | Timestamp for when the user account was last updated.         |


---

# 2. Table: user_sessions

| Column Name   | Data Type     | Description                                                   |
|---------------|---------------|---------------------------------------------------------------|
| session_id    | INT           | Primary key, auto-incremented, unique identifier for each session. |
| user_id       | INT           | Foreign key referencing the user who owns this session.         |
| token         | VARCHAR(500)  | Unique token (e.g., JWT) for the session.  <span style="color:red">**Index**</span> created for faster lookups.                     |
| ip_address    | VARCHAR(50)   | IP address of the user during the session (optional).           |
| user_agent    | VARCHAR(255)  | Information about the user's device/browser (optional).         |
| created_at    | DATETIME      | Timestamp for when the session was created.                    |
| expires_at    | DATETIME      | Timestamp for when the session expires (optional).             |

** An index is created on the token column to optimize performance during session validation and authentication, as tokens are frequently used for API requests instead of session IDs.

---

# 3. Table: roles_permissions

| Column Name   | Data Type     | Description                                                |
|---------------|---------------|------------------------------------------------------------|
| role_id       | INT           | Primary key, auto-incremented, unique identifier for each role. |
| role_name     | VARCHAR(50)   | Name of the role (e.g., 'admin', 'user').                  |
| permission    | VARCHAR(255)  | Permission level associated with the role (e.g., 'read', 'write', 'admin access'). |
| created_at    | DATETIME      | Timestamp for when the role was created.                   |
| updated_at    | DATETIME      | Timestamp for when the role was last updated.              |


---

# 4. Table: users_roles

| Column Name   | Data Type   | Description                                                   |
|---------------|-------------|---------------------------------------------------------------|
| user_id       | INT         | Foreign key referencing the `users.user_id`.                   |
| role_id       | INT         | Foreign key referencing the `roles_permissions.role_id`.       |


---

# 5. Table: chat_sessions

| Column Name     | Data Type     | Description                                                      |
|-----------------|---------------|------------------------------------------------------------------|
| session_id      | INT           | Primary key, auto-incremented, unique identifier for each session.|
| user_id         | INT           | Foreign key referencing the `users.user_id`.                      |
| session_name    | VARCHAR(255)  | Optional name for the chat session (e.g., "Support Query").       |
| session_status  | VARCHAR(50)   | Status of the session (e.g., 'active', 'completed').              |
| created_at      | DATETIME      | Timestamp for when the chat session was created.                  |


---

# 6. Table: chat_history

| Column Name   | Data Type     | Description                                                   |
|---------------|---------------|---------------------------------------------------------------|
| message_id    | INT           | Primary key, auto-incremented, unique identifier for each message. |
| session_id    | INT           | Foreign key referencing the `chat_sessions.session_id`.        |
| user_id       | INT           | Foreign key referencing the `users.user_id`, nullable for AI responses. |
| message_text  | TEXT          | The actual content of the message sent during the session.     |
| sender        | VARCHAR(50)   | Indicates if the message was sent by 'user' or 'AI'.          |
| message_type  | VARCHAR(50)   | Type of message (e.g., 'text', 'image', 'attachment').         |
| timestamp     | DATETIME      | Timestamp for when the message was created.                   |

---

# 7. Table: chat_metadata

| Column Name    | Data Type     | Description                                                      |
|----------------|---------------|------------------------------------------------------------------|
| metadata_id    | INT           | Primary key, auto-incremented, unique identifier for each metadata record. |
| session_id     | INT           | Foreign key referencing the `chat_sessions.session_id`.           |
| ai_model       | VARCHAR(255)  | AI model used during the session (e.g., GPT-4, LLaMA).            |
| total_duration | INT           | Total duration of the session in minutes.                        |
| message_count  | INT           | Total number of messages exchanged during the session.            |
| feedback       | VARCHAR(255)  | Optional feedback from the user regarding the session.            |
| created_at     | DATETIME      | Timestamp for when the metadata was created.                     |


---

# 8. Table: ai_models

| Column Name  | Data Type     | Description                                                |
|--------------|---------------|------------------------------------------------------------|
| model_id     | INT           | Primary key, auto-incremented, unique identifier for each AI model. |
| model_name   | VARCHAR(255)  | Name of the AI model (e.g., GPT-4, LLaMA).                 |
| version      | VARCHAR(50)   | Version of the AI model (e.g., "v1", "v2").                |
| created_at   | DATETIME      | Timestamp for when the AI model record was created.         |
