# Save Session Channel Data API

This documentation describes the endpoint for saving or updating WhatsApp channel connection data.

## Endpoint

**POST** `/api/whatsapp/session/save/{business_id}`

## Description

Receives session data from the WhatsApp Node.js service (e.g., when a session connects, authenticates, or gets destroyed) and upserts it into the backend's `Whatsapp_channels` database. It handles the `connected_at` timestamp by only recording it the first time the status transitions to `connected`.

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `business_id` | `UUID` | The unique identifier of the business owning the channel. |

## Request Body

**Content-Type**: `application/json`

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `phone_number` | `str` | The WhatsApp phone number representing the channel. | Yes |
| `display_name` | `str` | The display name for the channel. | No |
| `status` | `string` | The current session status. Must be one of: `"pending_qr"`, `"authenticating"`, `"connected"`, `"disconnected"`, `"destroyed"`. | Yes |

**Example Request Payload:**
```json
{
  "phone_number": "628123456789",
  "display_name": "Toko Sejahtera",
  "status": "connected"
}
```

## Responses

### Success (200 OK)

Returns the fully upserted channel data, including the computed `connected_at` field (if applicable).

**Example Response:**
```json
{
  "status": "success",
  "message": "Operation successful.",
  "data": {
    "id": "e2a12903-4f99-4a4b-8451-b0e51382fc1a",
    "business_id": "06a8a34c-12f8-42c6-bf09-33f2e3a08171",
    "phone_number": "628123456789",
    "display_name": "Toko Sejahtera",
    "status": "connected",
    "connected_at": "2026-06-08T10:35:00.000Z"
  }
}
```

### Validation Error (422 Unprocessable Entity)

Returned if the `business_id` format is invalid or if the payload fields fail schema validation (e.g., submitting an unrecognized status).

**Example Response:**
```json
{
    "detail": [
        {
            "loc": ["body", "status"],
            "msg": "Input should be 'pending_qr', 'authenticating', 'connected', 'disconnected' or 'destroyed'",
            "type": "literal_error"
        }
    ]
}
```
