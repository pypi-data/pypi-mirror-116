from .logger import Logger
from .constants import *
from .exceptions import *
from .network_utils import *

class NetworkManager():
    def layout_subnet_plan(self, subnet_plan, summary):
        Logger.info(f"Laying out subnet plan '{subnet_plan['name']}'...")
        return layout_subnet_plan(subnet_plan, summary)


Networks = NetworkManager()