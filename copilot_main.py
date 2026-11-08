import os
from dotenv import load_dotenv
from copilot import CopilotClient
from copilot.session import PermissionHandler

load_dotenv()


async def ask_copilot(question: str) -> str:
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env")

    client = CopilotClient(github_token=token, use_logged_in_user=False)

    try:
        await client.start()

        session = await client.create_session()

        try:
            response = await session.send_and_wait(question)
            return response.data.content

        finally:
            await session.disconnect()

    finally:
        await client.stop()


async def ask_copilot_with_tools(question: str) -> str:
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env")

    client = CopilotClient(github_token=token, use_logged_in_user=False)

    try:
        await client.start()

        session = await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            system_message={"content": """
        You are an enterprise assistant.

        You have access to an MCP server called enterprise-tools.

        When the user asks for customer information,
        use the get_customer tool.

        Do not invent customer information.

        You have no internet access.
        Use only the provided MCP tools.
        If information is unavailable, say so.
        """},
            mcp_servers={
                # "enterprise-tools": {
                #     "type": "http",
                #     "url": "http://127.0.0.1:8001/mcp",
                #     "tools": ["*"],
                # }
                "enterprise-tools": {
                    "type": "stdio",
                    "command": "python",
                    "args": ["my_mcp_server_stdio.py"],
                    "tools": ["*"],
                }
            },
        )

        try:
            response = await session.send_and_wait(question)
            return response.data.content

        finally:
            await session.disconnect()

    finally:
        await client.stop()


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(ask_copilot_with_tools(input("Enter your question: "))))
