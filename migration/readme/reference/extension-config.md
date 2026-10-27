# All Config

Retrieves all configuration data for the current extension.

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
    "/config": {
      "get": {
        "summary": "All Config",
        "description": "",
        "operationId": "extension-config",
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"channel\": {}, // Object containing the per-channel config data \n  \"extension\": {} // Object containing the global extension config data\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "channel": {
                      "type": "object",
                      "properties": {}
                    },
                    "extension": {
                      "type": "object",
                      "properties": {}
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
              "code": "curl --request GET \\\n  --url https://api.muxy.io/v1/e/config \\\n  --header 'authorization: <Client ID> <any JWT>' \\\n  --header 'content-type: application/json'"
            },
            {
              "language": "javascript",
              "code": "const medkit = new Muxy.SDK();\nawait medkit.loaded();\n\nconst config = medkit.getConfig();"
            },
            {
              "language": "node",
              "code": "type ExtensionConfig = {\n  enablePurchases?: Boolean;\n};\ntype ChannelConfig = {\n  itemAmount?: Number;\n};\ntype Config = {\n  channel: ChannelConfig;\n  extension: ExtensionConfig;\n};\n\nconst medkit = new Muxy.SDK();\nawait medkit.loaded();\n\nconst config = medkit.getConfig<Config>();\nconsole.log(config.channel.itemAmount || 100);"
            }
          ],
          "samples-languages": [
            "curl",
            "javascript",
            "node"
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
  "_id": "6140c2ea9ed947004d5565d3:6169ea45fa9c80005c9edc5b"
}
```