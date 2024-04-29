import unittest
from app.tools_loader import load_tools
import tests.tools.stubs as stubs

CREATE_STRINGSTUB_PATH = "tests.tools.create_stringstub"

class ToolsLoaderTester(unittest.TestCase):
    def test_if_loads_from_toollist(self):
       tool_list = [CREATE_STRINGSTUB_PATH]
       result = load_tools(tool_list)
       expected = [stubs.stringstub]
       self.assertEqual(result, expected, "Loader did not load tools correctly")
