# Extension State

An admin or backend caller can make this PATCH request to add, modify, or remove cross-channel state data for the current extension, using [JSONPatch](http://jsonpatch.com) syntax.

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
    "/extension_state": {
      "patch": {
        "summary": "Extension State",
        "description": "",
        "operationId": "extension-state-1",
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
                    "value": "{\n  \"ice_cream\": {\n    \"flavor\": \"coffee\",\n    \"toppings\": [\"sprinkles\", \"caramel\"]\n  }\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "ice_cream": {
                      "type": "object",
                      "properties": {
                        "flavor": {
                          "type": "string",
                          "example": "coffee"
                        },
                        "toppings": {
                          "type": "array",
                          "items": {
                            "type": "string",
                            "example": "sprinkles"
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
              "code": "curl --request PATCH \\\n  --url https://api.muxy.io/v1/e/extension_state \\\n  --header 'authorization: <Client ID> <Backend JWT>' \\\n  --header 'content-type: application/json' \\\n  --data '[{ \"op\": \"add\", \"path\": \"/ice_cream/toppings\", \"value\": [\"sprinkles\", \"caramel\"] }]'"
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
  "_id": "6140c2ea9ed947004d5565d3:6169e570dad7ad001e54618d"
}
```