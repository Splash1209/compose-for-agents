build-adk-image:
	docker buildx build --builder hydrobuild --platform linux/amd64,linux/arm64 --tag jimclark106/supplier_agent:latest --push --file Dockerfile .

build-adk-ui-image:
	docker buildx build --builder hydrobuild --platform linux/amd64,linux/arm64 --tag jimclark106/supplier_agent_ui:latest --push --file Dockerfile.adk-ui .

gateway-secrets:
	@echo "⚠️  Checking for required environment variables..."
	@if [ -z "$(MONGO_ROOT_PASSWORD)" ]; then echo "❌ MONGO_ROOT_PASSWORD not set. Please set this in your .env file and source it."; exit 1; fi
	@if [ -z "$(RESEND_API_KEY)" ]; then echo "❌ RESEND_API_KEY not set"; exit 1; fi
	@if [ -z "$(BRAVE_API_KEY)" ]; then echo "❌ BRAVE_API_KEY not set"; exit 1; fi
	@if [ -z "$(OPENAI_API_KEY)" ]; then echo "❌ OPENAI_API_KEY not set"; exit 1; fi
	@echo "✅ All required variables set"
	docker mcp secret set 'mongodb.connection_string=mongodb://$(MONGO_ROOT_USERNAME):$(MONGO_ROOT_PASSWORD)@mongodb:27017/' && \
	docker mcp secret set 'resend.api_key=$(RESEND_API_KEY)' && \
	docker mcp secret set 'brave.api_key=$(BRAVE_API_KEY)' && \
	docker mcp secret export brave resend mongodb > ./.mcp.env && \
	echo $(OPENAI_API_KEY) > ./secret.openai-api-key

adk-api-server-start:
	MCPGATEWAY_ENDPOINT=http://localhost:8811/sse \
	MODEL_RUNNER_URL=http://localhost:12434/engines/llama.cpp/v1 \
	MODEL_RUNNER_MODEL=ai/qwen3:14B-Q6_K \
	uv run adk api_server --port 8000 --log_level DEBUG

adk-ui-start:
	API_BASE_URL=http://localhost:8000 \
	uv run streamlit run apps/vendor_app.py --server.port 3000

local-context:
	docker context use desktop-linux

local-compose-up:
	docker compose up front-end catalogue catalogue-db mongodb mcp-gateway

local-down:
	docker compose down

local-up: local-context local-compose-up

local-down: local-context local-down

offload-context:
	docker context use docker-cloud

offload-compose-up:
	docker compose -f compose.yaml -f compose.offload.yaml up --build

offload-up: offload-context offload-compose-up

offload-down:
	docker compose -f compose.yaml -f compose.offload.yaml down

