# Accumulate

Retrieves a snapshot of accumulated data from an existing accumulation buffer.

[block:callout]
{
  "type": "info",
  "title": "Single-channel or extension-wide data accumulation",
  "body": "If the JWT used to access this endpoint has the `broadcaster` role, the response contains data for that broadcaster's channel; that is, the `channel_id` value is the broadcaster's Twitch ID.\n\nIf the JWT used is  extension-level, with the `admin` or `backend` role, the response contains all data points for the entire extension across all channels."
}
[/block]

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "REST API",
    "version": "1.0"
  },
  "servers": [
    {
      "url": "https://api.muxy.io/v1/e"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {
          "clientCredentials": {
            "tokenUrl": "https://example.com/oauth2/token",
            "scopes": {}
          }
        }
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/accumulate": {
      "get": {
        "summary": "Accumulate",
        "description": "",
        "operationId": "accumulate-1",
        "parameters": [
          {
            "name": "id",
            "in": "query",
            "description": "The name of the accumulation buffer from which to retrieve data.",
            "schema": {
              "type": "string",
              "default": "default"
            }
          },
          {
            "name": "start",
            "in": "query",
            "description": "Unix millisecond timestamp of earliest entry to include in the result.",
            "schema": {
              "type": "integer",
              "format": "int32",
              "default": 0
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"data\": [\n    {\n      \"observed\": 1634401498121,  // The Unix millisecond timestamp of this entry\n      \"channel_id\": \"12345\",      // Twitch Channel ID associated with this entry\n      \"opaque_user_id\": \"U12345\", // An Opaque ID of the viewer who sent this entry (or empty string if Twitch ID is known)\n      \"user_id\": \"12345\",         // The Twitch ID of the viewer who sent this entry (or empty string if unknown)\n      \"data\": {}                  // An arbitrary object of data sent by the viewer\n    }\n  ],\n  \"latest\": 1634401498121 // Unix epoch time (in milliseconds) of most recent entry\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "data": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "observed": {
                            "type": "integer",
                            "example": 1634401498121,
                            "default": 0
                          },
                          "channel_id": {
                            "type": "string",
                            "example": "12345"
                          },
                          "opaque_user_id": {
                            "type": "string",
                            "example": "U12345"
                          },
                          "user_id": {
                            "type": "string",
                            "example": "12345"
                          },
                          "data": {
                            "type": "object",
                            "properties": {}
                          }
                        }
                      }
                    },
                    "latest": {
                      "type": "integer",
                      "example": 1634401498121,
                      "default": 0
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "x-readme": {
          "code-samples": [
            {
              "language": "curl",
              "code": "curl --request GET \\\n  --url https://api.muxy.io/v1/e/accumulate \\\n  --header 'authorization: <Client ID> <broadcaster, admin, or backend JWT>' \\\n  --header 'content-type: application/json'"
            }
          ],
          "samples-languages": [
            "curl"
          ]
        }
      }
    }
  },
  "x-readme": {
    "headers": [
      {
        "key": "Authorization",
        "value": "<Twitch Client ID> <JWT>"
      }
    ],
    "explorer-enabled": false,
    "proxy-enabled": false
  },
  "x-readme-fauxas": true,
  "_id": "6140c2ea9ed947004d5565d3:616afc307e8df4003111184a"
}
```