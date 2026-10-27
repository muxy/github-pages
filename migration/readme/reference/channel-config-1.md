# Channel Config

A caller with broadcaster authorization can use this POST request to define extension configuration data for their own channel.

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
    "/config/channel": {
      "post": {
        "summary": "Channel Config",
        "description": "",
        "operationId": "channel-config-1",
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
                    "value": "{\n  \"broadcaster_birthday\": \"2000-01-01\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "broadcaster_birthday": {
                      "type": "string",
                      "example": "2000-01-01"
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
              "code": "curl --request POST \\\n  --url https://sandbox.api.muxy.io/v1/e/config/channel \\\n  --header 'authorization: <Client ID> <broadcaster JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '{ \"broadcaster_birthday\": \"2000-01-01\" }'"
            },
            {
              "language": "javascript",
              "code": "const medkit = new Muxy.SDK();\nawait medkit.loaded();\n\nconst state = medkit.setChannelConfig({\n  \"broadcaster_birthday\": \"2000-01-01\"\n});"
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
  "_id": "6140c2ea9ed947004d5565d3:6169f069c6387600717594f5"
}
```