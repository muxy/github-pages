# Accumulate

Adds developer-defined data to an accumulation buffer, along with a timestamp and caller information.

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
    "/accumulate": {
      "post": {
        "summary": "Accumulate",
        "description": "",
        "operationId": "accumulate-2",
        "parameters": [
          {
            "name": "id",
            "in": "query",
            "description": "The name of the accumulation buffer to which to write data.",
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
                  "RAW_BODY": {
                    "type": "string",
                    "description": "The developer-defined data you wish to store, in JSON-encoded format. The marshalled JSON size must be under 256 bytes."
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
                    "value": "{ }"
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
              "code": "curl --request POST \\\n  --url https://api.muxy.io/v1/e/accumulate \\\n  --header 'authorization: <Client ID> <any JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '{ \"next_game\": \"Day of the Tentacle\" }'"
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
  "_id": "6140c2ea9ed947004d5565d3:616b0022bfc1f90077bac02c"
}
```