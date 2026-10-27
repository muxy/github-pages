# Extension Viewer State

Viewers can make this POST request to define extension state data for themselves on the current channel.

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
    "/extension_viewer_state": {
      "post": {
        "summary": "Extension Viewer State",
        "description": "",
        "operationId": "extension-viewer-state-1",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "RAW_BODY"
                ],
                "properties": {
                  "RAW_BODY": {
                    "type": "string",
                    "description": "Accepts arbitrary JSON data"
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
                    "value": "{\n  \"favorite_color\": \"blue\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "favorite_color": {
                      "type": "string",
                      "example": "blue"
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
                    "value": "Malformed input body"
                  }
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
              "code": "curl --request POST \\\n  --url https://sandbox.api.muxy.io/v1/e/extension_viewer_state \\\n  --header 'authorization: <Client ID> <viewer JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '{ \"favorite_color\": \"blue\" }'"
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
  "_id": "6140c2ea9ed947004d5565d3:6169e849ab6271007840508f"
}
```