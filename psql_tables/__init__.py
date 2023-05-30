import sqlalchemy

from .action import create_table as create_action_table
from .purchase import create_table as create_purchase_table

metadata = sqlalchemy.MetaData()

action = create_action_table(metadata)
purchase = create_purchase_table(metadata)
