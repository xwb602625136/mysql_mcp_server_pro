from typing import Dict, Any, Sequence

from mcp import Tool
from mcp.types import TextContent

from .base import BaseHandler
from config import get_db_config
from handles import (
    ExecuteSQL
)


class GetTableName(BaseHandler):

    name = "get_table_name"
    description = (
        "根据表中文名搜索数据库中对应的表名"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要搜索的表中文名"
                    }
                },
                "required": ["text"]
            }
        )

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
            """根据表的中文注释搜索数据库中的表名

            参数:
                text (str): 要搜索的表中文注释关键词

            返回:
                list[TextContent]: 包含查询结果的TextContent列表
                - 返回匹配的表名、数据库名和表注释信息
                - 结果以CSV格式返回，包含列名和数据
            """
            try:
                if "text" not in arguments:
                    raise ValueError("缺少查询语句")

                text = arguments["text"]

                config = get_db_config()
                execute_sql = ExecuteSQL()

                sql = "SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_COMMENT "
                sql += f"FROM information_schema.TABLES WHERE TABLE_SCHEMA = '{config['database']}' AND TABLE_COMMENT LIKE '%{text}%';"
                return await execute_sql.run_tool({"query":sql})

            except Exception as e:
                return [TextContent(type="text", text=f"执行查询时出错: {str(e)}")]