# Prompt Memory Service

The prompt memory service provides a way to store and retrieve prompts using vector search. It is implemented as a REST API and uses a FAISS index for efficient similarity search.

## API Endpoints

### `POST /add`

Adds a new prompt to the memory.

**Request Body:**

```json
{
  "prompt": "This is a new prompt."
}
```

**Response:**

```json
{
  "message": "Prompt added successfully"
}
```

### `POST /search`

Searches for similar prompts in the memory.

**Request Body:**

```json
{
  "query": "This is a search query.",
  "k": 5
}
```

**Response:**

```json
{
  "results": [
    "This is a similar prompt.",
    "This is another similar prompt."
  ]
}
```

### `GET /prompts`

Retrieves all prompts from the memory.

**Response:**

```json
{
  "prompts": [
    "This is the first prompt.",
    "This is the second prompt."
  ]
}
```

## Implementation Details

The service uses the `sentence-transformers` library to generate embeddings for the prompts and `faiss-cpu` for indexing and searching. The prompts are stored in a JSON file and the FAISS index is stored in a separate file.
