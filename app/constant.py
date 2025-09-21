from typing import Final

DESCRIPTION: Final[str] = 'description'
"""Key defined for JSON for returning to client request
"""

ERROR: Final[str] = 'error'
"""Key defined for JSON for returning to client request when Exception is raised.
This key would contain high overview information about why a query is fail
"""

ERROR_MESSAGE_DETAIL: Final[str] = 'error_detail'
"""Key defined for JSON for returning to client request when Exception is raised.
This key would contain detail information about why a query is fail
"""
