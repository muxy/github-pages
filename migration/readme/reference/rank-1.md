# Rank

Retrieves all current ranking data being stored in the given buffer. Each entry in the returned `data` array provides a  `key` value (a response string that has been submitted), and a `score` value (the number of users who have submitted that response).

[block:callout]
{
  "type": "info",
  "title": "One entry per user",
  "body": "If a viewer submits multiple responses, only the most recent response is counted."
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
    "/rank": {
      "get": {
        "summary": "Rank",
        "description": "",
        "operationId": "rank-1",
        "parameters": [
          {
            "name": "id",
            "in": "query",
            "description": "The ranking-buffer ID that identifies a question for which responses are ranked.",
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
                    "value": "{\n  \"data\": [\n    {\n      \"key\": \"DOTA\",\n      \"score\": 12\n    },\n    {\n      \"key\": \"FIFA 2014\",\n      \"score\": 8\n    }\n  ]\n}"
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
                          "key": {
                            "type": "string",
                            "example": "DOTA"
                          },
                          "score": {
                            "type": "integer",
                            "example": 12,
                            "default": 0
                          }
                        }
                      }
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
              "code": "curl --request GET \\\n  --url https://api.muxy.io/v1/e/rank?id=next-game \\\n  --header 'authorization: <Client ID> <backend, admin, or broadcaster JWT>' \\\n  --header 'content-type: application/json'"
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
  "_id": "6140c2ea9ed947004d5565d3:616b037bbd6426006926e1f3"
}
```