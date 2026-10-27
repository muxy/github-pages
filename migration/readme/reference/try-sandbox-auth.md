# Authorization for Testing

Returns one or more JSON Web Tokens (JWT) for use in the sandbox environment.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Sandbox API",
    "version": "1.0"
  },
  "servers": [
    {
      "url": "https://sandbox.api.muxy.io/v1/e"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": "bearer",
        "x-default": "<Twitch Client ID> <JWT>"
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/authtoken": {
      "post": {
        "summary": "Authorization for Testing",
        "description": "Returns one or more JSON Web Tokens (JWT) for use in the sandbox environment.",
        "operationId": "try-sandbox-auth",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "extension_id": {
                    "type": "string",
                    "description": "The Client ID for the extension. A Twitch Extension Client ID that has been registered with Muxy. See [Quick Start](https://docs.muxy.io/docs/quick-start) for details."
                  },
                  "channel_id": {
                    "type": "string",
                    "description": "The Twitch Channel ID to simulate"
                  },
                  "user_id": {
                    "type": "string",
                    "description": "A single Twitch User ID. When role is \"broadcaster\", must match `channel_id`. To request multiple JWTs, use `user_ids` instead."
                  },
                  "role": {
                    "type": "string",
                    "description": "The user role. One of \"viewer\", \"broadcaster\", \"admin\""
                  },
                  "user_ids": {
                    "type": "array",
                    "description": "A set of Twitch user IDs. Use instead of `user_id` to request multiple JWTs with the same role.",
                    "items": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  // if `user_ids` is provided\n  \"tokens\": [\"<valid sandbox jwt>\", \"<valid sandbox jwt>\", ...]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "token": {
                      "type": "string",
                      "example": "<jwt valid for sandbox environment>"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "text/plain": {
                "examples": {
                  "Result": {
                    "value": "No such extension found"
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": []
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "6140bfba91b2a300292d7d5e:6140c0e1fb53f8005b2e1738"
}
```