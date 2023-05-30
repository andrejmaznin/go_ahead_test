from datetime import date
from typing import List

from sqlalchemy import select, and_

from libs.postgresql import get_database
from modules.actions.consts import MetricType
from modules.actions.queries import aggregate_table_query
from modules.actions.queries import avg_daily_product_purchases as avg_daily_product_purchases_query
from modules.actions.queries import total_product_purchases as total_product_purchases_query
from modules.actions.queries import unique_users as unique_users_query
from modules.actions.schemas.request import FilterSchema


def construct_query_for_filters(start: date, end: date, filters: List[FilterSchema]):
    base_query = aggregate_table_query(start=start, end=end)
    base_query_filters = []

    other_filter_queries = []

    for f in filters:
        if f.metric == MetricType.TOTAL_USERS:
            f_query = unique_users_query(start=start, end=end)

            filter_clause = and_(
                f_query.c.unique_users >= f.from_number,
                f_query.c.unique_users <= f.to_number
            ) if f.to_number else f_query.c.unique_users >= f.from_number

            filtered_f_query = select(
                f_query.c.site_id.label('site_id')
            ).select_from(
                f_query
            ).where(filter_clause).alias('total_users')
            other_filter_queries.append(filtered_f_query)

        elif f.metric == MetricType.AVG_DAILY_USERS:
            filter_clause = and_(
                base_query.c.avg_daily_users >= f.from_number,
                base_query.c.avg_daily_users <= f.to_number
            ) if f.to_number else base_query.c.avg_daily_users >= f.from_number
            base_query_filters.append(filter_clause)

        elif f.metric == MetricType.TOTAL_PURCHASES:
            if f.products is None:
                filter_clause = and_(
                    base_query.c.purchases >= f.from_number,
                    base_query.c.purchases <= f.to_number
                ) if f.to_number else base_query.c.purchases >= f.from_number
                base_query_filters.append(filter_clause)

            else:
                f_query = total_product_purchases_query(product=f.products, start=start, end=end)

                filter_clause = and_(
                    getattr(f_query.c, f'{f.products.value}_purchases') >= f.from_number,
                    getattr(f_query.c, f'{f.products.value}_purchases') <= f.to_number,
                ) if f.to_number else getattr(f_query.c, f'{f.products.value}_purchases') >= f.from_number

                filtered_f_query = select(
                    f_query.c.site_id.label('site_id')
                ).select_from(
                    f_query
                ).where(
                    filter_clause
                ).alias(f'{f.products.value}_purchases')
                other_filter_queries.append(filtered_f_query)

        elif f.metric == MetricType.AVG_DAILY_PURCHASES:
            if f.products is None:
                filter_clause = and_(
                    base_query.c.avg_daily_purchases >= f.from_number,
                    base_query.c.avg_daily_purchases <= f.to_number
                ) if f.to_number else base_query.c.avg_daily_purchases >= f.from_number
                base_query_filters.append(filter_clause)

            else:
                f_query = avg_daily_product_purchases_query(product=f.products, start=start, end=end)

                filter_clause = and_(
                    getattr(f_query.c, f'{f.products.value}_avg_daily_purchases') >= f.from_number,
                    getattr(f_query.c, f'{f.products.value}_avg_daily_purchases') <= f.to_number,
                ) if f.to_number else getattr(f_query.c, f'{f.products.value}_avg_daily_purchases') >= f.from_number

                filtered_f_query = select(
                    f_query.c.site_id.label('site_id')
                ).select_from(
                    f_query
                ).where(
                    filter_clause
                ).alias(f'{f.products.value}_avg_daily_purchases')
                other_filter_queries.append(filtered_f_query)

    base_query = select(
        base_query.c.site_id
    ).select_from(
        base_query
    ).alias('base_query')

    joins_for_base_query = base_query
    for f_q in other_filter_queries:
        joins_for_base_query = joins_for_base_query.join(
            f_q,
            onclause=base_query.c.site_id == f_q.c.site_id
        )

    base_query = select(
        base_query.c.site_id
    ).select_from(
        joins_for_base_query
    ).where(
        and_(
            *base_query_filters
        )
    )
    return base_query


async def get_site_ids_for_filters(start: date, end: date, filters: List[FilterSchema]) -> List[int]:
    query = construct_query_for_filters(start=start, end=end, filters=filters)
    async with get_database().connection() as connection:
        async with connection.transaction():
            result = await connection.fetch_all(query=query)
            return [row['site_id'] for row in result]
