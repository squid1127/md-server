# API Documentation

`md-server` provides a RESTful API for creating markdown documents.

## Authentication

All API requests require an API key for authentication. The API key should be included in the `X-API-Key` header.
Example:

```http
X-API-Key: your_api_key_here
```

### Key Management

API keys can be managed using the CLI tool provided with `md-server`, in `cli.py`. You can create, list, and delete API keys as needed.

## Endpoints

Currently, there are endpoints to create and retrieve markdown documents. More endpoints may be added in the future. (That is, if it's actually maintained)

### `POST /api/new`

Create a new markdown document.

- **Request Body**: JSON object with the following fields:
  - `title` (string, required): The title of the markdown document.
  - `content` (string, required): The markdown content.
- **Response**: JSON object with the following fields:
  - `id` (string): The unique identifier of the created document.
  - `title` (string): The title of the document.
  - `content` (string): The markdown content.
  - `created_at` (string): Timestamp of when the document was created.
- **Example Request**:

```http
POST /api/new HTTP/1.1
Host: yourserver.com
Content-Type: application/json
X-API-Key: your_api_key_here

{
  "title": "My First Document",
  "content": "# Hello World\nThis is my first markdown document."
}
```

### `GET /api/documents/{id}`

Retrieve a markdown document by its ID.

- **Path Parameters**:
  - `id` (string, required): The unique identifier of the document to retrieve.
- **Response**: JSON object with the following fields:
  - `id` (string): The unique identifier of the document.
  - `title` (string): The title of the document.
  - `content` (string): The markdown content.
  - `created_at` (string): Timestamp of when the document was created.
- **Example Request**:

```http
GET /api/documents/123 HTTP/1.1
Host: yourserver.com
X-API-Key: your_api_key_here
```
