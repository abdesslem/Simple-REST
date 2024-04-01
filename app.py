#!/usr/bin/env python3
import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yaml")


if __name__ == "__main__":
    connex_app.run()
