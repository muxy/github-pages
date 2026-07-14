# Extension Config

A caller with administrative authorization can use this POST request to define global (cross-channel) configuration data for the current extension.

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
    "/config/extension": {
      "post": {
        "summary": "Extension Config",
        "description": "",
        "operationId": "extension-config-2",
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
                    "value": "{\n  \"release_date\": \"2021-10-31\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "release_date": {
                      "type": "string",
                      "example": "2021-10-31"
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
              "code": "curl --request POST \\\n  --url https://sandbox.api.muxy.io/v1/e/config/extension \\\n  --header 'authorization: <Client ID> <admin or backend JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '{ \"release_date\": \"2021-10-31\" }'"
            },
            {
              "language": "javascript",
              "code": "const medkit = new Muxy.SDK();\nawait medkit.loaded();\n\nconst state = medkit.setChannelConfig({\n  \"release_date\": \"2021-10-31\"\n});"
            }
          ],
          "samples-languages": [
            "curl",
            "javascript"
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
  "_id": "6140c2ea9ed947004d5565d3:6169eb6ed27fb50010b80b77"
}
```