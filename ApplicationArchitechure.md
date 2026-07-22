# Application Architecture (MVC Pattern)

The application follows an **MVC-inspired architecture** to organize the tokenization workflow into separate layers. This architecture improves maintainability, scalability, testability, and separation of concerns by dividing responsibilities between request handling, business processing, and data persistence.

---

## Routes Layer

The Routes layer is responsible for defining and managing application API endpoints.

### Router Responsibilities

- Defines available API endpoints.
- Handles incoming HTTP request types:
  - GET
  - POST
  - PUT
  - DELETE
- Performs request routing.
- Forwards requests to the appropriate controller.
- Maintains endpoint organization without containing business logic.

---

## Controller Layer

The Controller layer acts as the communication bridge between the Routes layer and the Service layer.

### Controller Responsibilities

- Receives requests from API routes.
- Validates incoming request data.
- Extracts required parameters from requests.
- Invokes appropriate service operations.
- Handles service responses.
- Returns appropriate HTTP responses and status codes to the client.

### Purpose

The controller layer ensures that API-related logic remains separate from the application's core processing logic.

---

## Service Layer

The Service layer contains the core business logic responsible for executing the tokenization pipeline.

### Service Responsibilities

- Handles complex processing workflows.
- Performs data transformation and enrichment.
- Manages the complete tokenization process.

### Processing Operations Include

- Data extraction processing
- Data normalization
- Text cleaning
- Tokenization
- Language detection and processing
- Regex-based transformations
- NLP enrichment:
  - Synonyms
  - Antonyms
  - Definitions
  - Linguistic metadata
- Sanskrit and English language processing

### Design Principle

The Service layer is independent of:

- API request handling
- Database implementation details

This allows business logic to be reused across multiple endpoints and workflows.

---

## Service Directory Structure

The `services` directory contains multiple sub-directories organized according to their role in the data extraction and tokenization workflow.

Each data source maintains its own processing pipeline based on its:

- Data format
- Extraction requirements
- Normalization rules
- Processing requirements

Examples:

- LearnSanskrit extraction pipeline
- Sanskrit Samskrutam extraction pipeline
- File-based extraction pipelines
- NLP processing services

---

## Service Files Organization

Files outside service sub-directories represent reusable service components.

They are categorized as:

### Parent Tokenization Services

- Responsible for executing common tokenization workflows after data extraction and normalization.
- Designed to be instantiated as reusable service objects.

Examples:

- English tokenization service
- Sanskrit tokenization service
- Data cleaning service
- NLP enrichment services

### API Service Operations

- Service classes used directly by controllers to execute specific API operations.
- Handle endpoint-specific business workflows.

---

## Repository Layer

The Repository layer manages all database interactions.

### Responsibilities

- Handles communication with MongoDB.
- Performs CRUD operations.
- Abstracts database logic from the Service layer.
- Provides reusable database access methods.

### Operations Include

- Reading metadata
- Retrieving source information
- Storing tokenized stories
- Updating processing status
- Retrieving processed tokenized data
- Managing database queries

### Repo Design Principle

The Service layer does not directly communicate with MongoDB. All database operations are handled through repositories.
