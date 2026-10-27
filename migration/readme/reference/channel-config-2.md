# Channel Config

A caller with broadcaster authorization can use this PATCH request to modify extension configuration data for their own channel, using [JSONPatch](http://jsonpatch.com) syntax.

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
      "patch": {
        "summary": "Channel Config",
        "description": "",
        "operationId": "channel-config-2",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "RAW_BODY": {
                    "type": "string"
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
                    "value": "{\n  \"settings\": {\n    \"color_theme\": \"dark\",\n    \"enable_features\": true\n  }\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "settings": {
                      "type": "object",
                      "properties": {
                        "color_theme": {
                          "type": "string",
                          "example": "dark"
                        },
                        "enable_features": {
                          "type": "boolean",
                          "example": true,
                          "default": true
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
              "code": "curl --request PATCH \\\n  --url https://api.muxy.io/v1/e/config/channel \\\n  --header 'authorization: <Client ID> <broadcaster JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '[{ \"op\": \"add\", \"path\": \"/settings/enable_features\", \"value\": true }]'"
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
  "_id": "6140c2ea9ed947004d5565d3:6169f227e43aeb0078742e50"
}
```