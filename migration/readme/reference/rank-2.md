# Rank

Use this call to submit a user's response to a given question. Only one value per viewer is retained.

[block:callout]
{
  "type": "info",
  "title": "Data Expiration",
  "body": "All entries sent by viewers to this endpoint expire 24 hours after the last entry is sent."
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
      "post": {
        "summary": "Rank",
        "description": "",
        "operationId": "rank-2",
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
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "key": {
                    "type": "string",
                    "description": "A string submitted by the user in response to this question, as the `key` value in a JSON object."
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
                    "value": "{\n  \"accepted\": true,         // Whether the entry has been added to the rankings\n  \"original\": \"Serious Sam\" // Optional. The previous value submitted by this viewer, if any. \n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "accepted": {
                      "type": "boolean",
                      "example": true,
                      "default": true
                    },
                    "original": {
                      "type": "string",
                      "example": "Serious Sam"
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
              "code": "curl --request POST \\\n  --url https://api.muxy.io/v1/e/rank?id=next-game \\\n  --header 'authorization: <Client ID> <any JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '{ \"key\": \"Last of Us\" }'"
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
  "_id": "6140c2ea9ed947004d5565d3:616b09cf76a2b5000f9560fd"
}
```