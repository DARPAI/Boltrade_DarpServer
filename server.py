from typing import Any
import asyncio
import requests
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
import urllib.parse
import json
import uvicorn
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from mcp.shared.exceptions import McpError
load_dotenv()

API_BASE = "portal.boltrade.ai"

server = Server("gems-api")
sse = SseServerTransport("/messages/")

def setup_logging():
    """Configure logging settings"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/boltrade_api_{timestamp}.log'
    
    # Configure logging format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  
        ]
    )
    return logging.getLogger('boltrade_api')

logger = setup_logging()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-sol-top-score-list",
            description="get solana tokens top scoring cryptocurrency list ,must contain CA address price and symbol and volume_h24 and market_cap and liquidity_usd and score and token_age ",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 10
                    },
                    "start": {
                        "type": "integer",
                        "description": "Starting position for pagination",
                        "minimum": 1,
                        "default": 1
                    }
                    # "chain": {
                    #     "type": "string",
                    #     "description": "Blockchain to filter results",
                    #     "enum": ["solana"],
                    #     "default": "solana"
                    # },
                    # "frame": {
                    #     "type": "string",
                    #     "description": "Time frame for data analysis",
                    #     "enum": ["30d"],
                    #     "default": "30d"
                    # }
                }
            }
        ),
        types.Tool(
            name="get-sol-smart-money-listing",
            description="get new solana tokens listings with smart money tracking,must contain CA address price and symbol and volume_h24 and market_cap and liquidity_usd and score and token_age ",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 10
                    },
                    "start": {
                        "type": "integer",
                        "description": "Starting position for pagination",
                        "minimum": 1,
                        "default": 1
                    }
                    # "chain": {
                    #     "type": "string",
                    #     "description": "Blockchain to filter results",
                    #     "enum": ["solana"],
                    #     "default": "solana"
                    # },
                    # "frame": {
                    #     "type": "string",
                    #     "description": "Time frame for data analysis",
                    #     "enum": ["1d"],
                    #     "default": "1d"
                    # }
                }
            },
            # outputSchema={
            #     "type": "object",
            #     "properties": {
            #         "name": {"type": "string"},
            #         "address": {"type": "string"},
            #         "symbol": {"type": "string"},
            #         "current_price": {"type": "number"},
               
            #         "pnl": {"type": "number"},
            #         "token_age": {"type": "string"},
            #         "TokenAgeDuration": {"type": "number"},
            #         "avg_price": {"type": "number"},
            #         "price_change_24h": {"type": "number"},
            #         "NumberOfSmartMoney": {"type": "integer"},
            #         "usdt_value": {"type": "number"},
            #         "total_spent": {"type": "number"},
            #         "liquidity": {"type": "number"},
            #         "market_cap": {"type": "number"},
            #         "fdv": {"type": "number"},
            #         "roi": {"type": "number"},
            #         "score": {"type": "number"},
            #         "realized_percent": {"type": "number"},
            #         "hold_in_token": {"type": "number"},
            #         "hold_in_usdt": {"type": "number"},
            #         "tx_buy": {"type": "integer"},
            #         "tx_sell": {"type": "integer"},
            #         "buy_volume_in_usdt": {"type": "number"},
            #         "sell_volume_in_usdt": {"type": "number"}
            #     }
            # }
             #    "image_url": {"type": "string"},
        )
    ]


# @server.list_prompts()
# async def list_prompts() -> list[Prompt]:
#     return [
#         Prompt(
#             name="find-sol-top-score",
#             description="Find the top performing cryptocurrency gems with detailed metrics,must contain CA address",
#             arguments=[
#                 PromptArgument(
#                     name="start", description="page number", required=True
#                 )
#             ],
#         )
#     ]

# @server.get_prompt()
# async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
#     if not arguments or "start" not in arguments:
#         raise McpError(INVALID_PARAMS, "start is required")

#     url = arguments["start"]

#     try:
#         # content, prefix = await fetch_url(url, user_agent_manual)
#         # # TODO: after SDK bug is addressed, don't catch the exception
#         logger.info("start: get_prompt")
#     except McpError as e:
#         return GetPromptResult(
#             description=f"Failed to fetch {url}",
#             messages=[
#                 PromptMessage(
#                     role="user",
#                     content=TextContent(type="text", text=str(e)),
#                 )
#             ],
#         )
#     return GetPromptResult(
#         description=f"Contents of {url}",
#         messages=[
#             PromptMessage(
#                 role="user", content=TextContent(type="text", text=prefix + content)
#             )
#         ],
#     )
# @server.list_prompts()
# async def handle_list_prompts() -> list[types.Prompt]:
#     """
#     List available prompts.
#     """
#     return [
#         types.Prompt(
#             name="find-sol-top-score-prompt",
#             description="Find top scoring cryptocurrency gems",
#             text="Find the top performing cryptocurrency gems with detailed metrics,must contain CA address"
#         ),
#         types.Prompt(
#             name="smart-money-prompt",
#             description="Track smart money movements in new token listings",
#             text="Show me new token listings with smart money tracking data,must contain CA address"
#         )
#     ]

def make_boltrade_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Boltrade API with proper error handling."""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Origin': 'https://app.boltrade.ai',
        'Referer': 'https://app.boltrade.ai/',
    }

    # Load proxy configuration from environment variables
    username = os.getenv('PROXY_USERNAME')
    password = os.getenv('PROXY_PASSWORD')
    proxy_host = os.getenv('PROXY_HOST')
    proxy_port = os.getenv('PROXY_PORT')
    
    if not all([username, password, proxy_host, proxy_port]):
        logger.error("Missing proxy configuration in environment variables")
        return None
    
    proxies = {
        'http': f'http://{username}:{password}@{proxy_host}:{proxy_port}',
        'https': f'http://{username}:{password}@{proxy_host}:{proxy_port}'
    }
        
    logger.info("="*100)
    logger.info("BOLTRADE API REQUEST111:")
    logger.info("="*100)
    logger.info(f"URL: {url}")
    logger.info("Headers:")
    for key, value in headers.items():
        logger.info(f"{key}: {value}")
    logger.info(f"Using proxy: {proxy_host}:{proxy_port}")
    
    try:
        response = requests.get(
            url, 
            headers=headers,
            proxies=proxies,
            timeout=10,
            verify=False  # Disable SSL verification
        )
        response.raise_for_status()
        response_data = response.json()

        logger.info("="*100)
        logger.info("BOLTRADE API RESPONSE:")
        logger.info("="*100)
        logger.info(f"Status Code: {response.status_code}")
        logger.info("Response Headers:")
        for key, value in response.headers.items():
            logger.info(f"{key}: {value}")
        
        logger.info("Response Body:")
        logger.info("-"*100)
        logger.info(json.dumps(response_data, indent=2, ensure_ascii=False))
        logger.info("-"*100)
        
        return response_data
    except Exception as e:
        logger.error("="*100)
        logger.error("BOLTRADE API ERROR:")
        logger.error("="*100)
        logger.error(f"Error Type: {type(e).__name__}")
        logger.error(f"Error Message: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Error Response Status: {e.response.status_code}")
            logger.error("Error Response Headers:")
            for key, value in e.response.headers.items():
                logger.error(f"{key}: {value}")
            try:
                error_body = e.response.json()
                logger.error("Error Response Body:")
                logger.error(json.dumps(error_body, indent=2, ensure_ascii=False))
            except:
                logger.error("Error Response Body:")
                logger.error(e.response.text)
        return None

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    print("\n" + "*"*100)
    print(f"TOOL CALL: {name}")
    print("*"*100)
    print("Arguments:")
    print(json.dumps(arguments, indent=2, ensure_ascii=False) if arguments else "None")

    if name == "get-sol-top-score-list":
        request_data = {
            "limit": 10,
            "start": 1,
            "chain": "solana",
            "frame": "30d"
        }
        
        if arguments is not None:
            for key in request_data.keys():
                if key in arguments:
                    request_data[key] = arguments[key]
        if request_data["start"] < 1:
            request_data["start"] = 1
        request_data["limit"] = 10
        print("\nProcessed Request Data:")
        print(json.dumps(request_data, indent=2, ensure_ascii=False))
        
        gems_url = f"https://{API_BASE}/onchain/v1/findgems/top_score?{urllib.parse.urlencode(request_data)}"
     
        gems_data = await asyncio.to_thread(make_boltrade_request, gems_url)

        if not gems_data:
            return [types.TextContent(type="text", text="Failed to retrieve gems data")]

        # Extract and format core token metrics
        formatted_tokens = []
        for token in gems_data.get("users", []):
            core_metrics = {
                "usd_price": token.get("usd_price"),
                "CA address": token.get("token_address"),
                "symbol": token.get("symbol"),
              #      "name": token.get("name"), 说明 不用了
              #      "image_url": token.get("image_url"),
              #  "url": token.get("url", ""),
                "volume_h24": token.get("volume_h24"),
                "fdv": token.get("fdv"),
                "market_cap": token.get("market_cap"),
                "price_change_h24": token.get("price_change_h24"),
                "liquidity_usd": token.get("liquidity_usd"),
                "score": token.get("score"),
                "token_age": token.get("token_age")
             #   "TokenAgeDuration": token.get("TokenAgeDuration"),
             #   "avg_price": token.get("avg_price"),
           #     "roi": token.get("roi"),
            #    "NumberOfUsers": token.get("NumberOfUsers")
            }
            formatted_tokens.append(core_metrics)

        logger.info("="*100)
        logger.info("TOP SCORE LIST - FORMATTED DATA:")
        logger.info("="*100)
        logger.info(json.dumps(formatted_tokens))
        logger.info("="*100)

        return [
            types.TextContent(
                type="text",
                text=json.dumps(formatted_tokens)
            )
        ]

    elif name == "get-sol-smart-money-listing":
        logger.info("="*100)
        logger.info("TOOL CALL: sol-smart-money-new-listing")
        logger.info("="*100)
        logger.info("Arguments:")
        logger.info(json.dumps(arguments, indent=2, ensure_ascii=False) if arguments else "None")

        request_data = {
            "limit": 10,
            "start": 1,
            "chain": "solana",
            "frame": "1d"
        }
        
        if arguments is not None:
            for key in request_data.keys():
                if key in arguments:
                    request_data[key] = arguments[key]
        if request_data["start"] < 1:  #librechat 填入0 ？？？
            request_data["start"] = 1
        request_data["limit"] = 10
        logger.info("Processed Request Data:")
        logger.info(json.dumps(request_data, indent=2, ensure_ascii=False))
        
        url = f"https://{API_BASE}/onchain/v1/findgems/smart_money_new_listing_buy?{urllib.parse.urlencode(request_data)}"

        response_data = await asyncio.to_thread(make_boltrade_request, url)

        if not response_data:
            return  [types.TextContent(type="text", text="Failed to retrieve smart money data")]

        # Extract and format core metrics
        formatted_tokens =''
        formattedjson = []
        for token in response_data.get("smart_money_new_listing_buy", []):
            core_metrics = {
                #   "name": token.get("name"),
                "CA address": token.get("address"),
                "symbol": token.get("symbol"),
                "current_price": token.get("current_price"),
                #"image_url": token.get("image_url"),
                "pnl": token.get("pnl"),
                "token_age": token.get("token_age"),
                #    "TokenAgeDuration": token.get("TokenAgeDuration"),
                "avg_price": token.get("avg_price"),
                "price_change_24h": token.get("price_change_24h"),
                "NumberOfSmartMoney": token.get("NumberOfSmartMoney"),
                "usdt_value": token.get("usdt_value"),
                "total_spent": token.get("total_spent"),
                "liquidity": token.get("liquidity"),
                "market_cap": token.get("market_cap"),
                "fdv": token.get("fdv"),
                #     "roi": token.get("roi"),
                "score": token.get("score"),
                # "realized_percent": token.get("realized_percent"),
                # "hold_in_token": token.get("hold_in_token"),
                # "hold_in_usdt": token.get("hold_in_usdt"),
                # "tx_buy": token.get("tx_buy"),
                # "tx_sell": token.get("tx_sell"),
                # "buy_volume_in_usdt": token.get("buy_volume_in_usdt"),
                # "sell_volume_in_usdt": token.get("sell_volume_in_usdt"),
            
                "risk": token.get("risk"),
                "websites": token.get("websites"),
                "telegram_handle": token.get("telegram_handle"),
                "twitter_handle": token.get("twitter_handle"),
                "discord_url": token.get("discord_url")
                #   "pumpfun_link": token.get("pumpfun_link") 
            }
            # Convert numeric values to formatted strings with appropriate labels
        #     formatted_text = (
        #         f"Contract Address: {core_metrics['address']}\n"
        #         f"Token Symbol: {core_metrics['symbol']}\n"
        #         f"Current Price: ${core_metrics['current_price']:.8f}\n"
        #         f"PnL: {core_metrics['pnl']:.2f}%\n"
        #         f"Token Age: {core_metrics['token_age']}\n"
        #         f"Token Duration: {core_metrics['TokenAgeDuration']} hours\n"
        #    #     f"Average Price: ${core_metrics['avg_price']:.8f}\n"
        #         f"24h Price Change: {core_metrics['price_change_24h']:.2f}%\n"
        #         f"Smart Money Count: {core_metrics['NumberOfSmartMoney']}\n"
        #         f"USDT Value: ${core_metrics['usdt_value']:,.2f}\n"
        #     #    f"Total Spent: ${core_metrics['total_spent']:,.2f}\n"
        #         f"Liquidity: ${core_metrics['liquidity']:,.2f}\n"
        #         f"Market Cap: ${core_metrics['market_cap']:,.2f}\n"
        #         f"Fully Diluted Value: ${core_metrics['fdv']:,.2f}\n"
        #      #   f"ROI: {core_metrics['roi']:.2f}%\n"
        #         f"Score: {core_metrics['score']:.2f}\n"
        #         f"Risk Level: {core_metrics['risk']}\n"
        #         f"Websites: {core_metrics['websites']}\n"
        #         f"Telegram: {core_metrics['telegram_handle']}\n"
        #         f"Twitter: {core_metrics['twitter_handle']}\n"
        #         f"Discord: {core_metrics['discord_url']}\n"
        #        # f"pumpfun_link: {core_metrics['pumpfun_link']}\n"
                
        #     )
            formattedjson.append(core_metrics)
        #    core_metrics = formatted_text
         #   formatted_tokens = formatted_tokens + core_metrics

        logger.info("="*100)
        logger.info("FORMATTED TOKENS:")
        logger.info("="*100)
        logger.info(formatted_tokens)
        logger.info("="*100)
        logger.info("FORMATTED JSON:")
        logger.info("="*100)
        logger.info(json.dumps(formattedjson))
        
        return [
            types.TextContent(
                type="text",
              #  text=formatted_tokens
                text=json.dumps(formattedjson)
            )
        ]

    else:
        raise ValueError(f"Unknown tool: {name}")

 
async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0], streams[1], #server.create_initialization_options()
            InitializationOptions(
                    server_name="boltrader",
                    server_version="0.1.1",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(tools_changed=True),
                        experimental_capabilities={},
                    ),
                ),
        )

routes = [
    Route("/sse", endpoint=handle_sse),
    Mount("/messages/", app=sse.handle_post_message),
]

app = Starlette(routes=routes, debug=True)

def start_server(host: str = "0.0.0.0", port: int = 3002):
    logger.info(f"Starting server on {host}:{port}")
    try:
        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        logger.error(f"Server startup error: {str(e)}")
        raise

if __name__ == "__main__":
    start_server() 