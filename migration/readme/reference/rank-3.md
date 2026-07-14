# Rank

Deletes all entries associated with the provided `id` query parameter. Requires a JWT with `broadcaster`, `admin`, or `backend` role.

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
    "/rank": {
      "delete": {
        "summary": "Rank",
        "description": "",
        "operationId": "rank-3",
        "parameters": [
          {
            "name": "id",
            "in": "query",
            "description": "The ID that identifies a question being ranked.",
            "schema": {
              "type": "string",
              "default": "default"
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
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
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
                    "value": "\"Malformed json body\""
                  }
                },
                "schema": {
                  "type": "string",
                  "example": "Malformed json body"
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
              "code": "curl --request DELETE \\\n  --url https://api.muxy.io/v1/e/rank?id=next-game \\\n  --header 'authorization: <Client ID> <broadcaster, admin, or backend JWT>' \\\n  --header 'content-type: application/json'"
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
  "_id": "6140c2ea9ed947004d5565d3:616b0b3bf81055000f10467d"
}
```