from datetime import date

from sqlalchemy import select, func, distinct, and_

from modules.actions.consts import ProductType
from psql_tables import action as action_table
from psql_tables import purchase as purchase_table


def action_purchases_join():
    return action_table.join(
        right=purchase_table,
        onclause=action_table.c.id == purchase_table.c.action_id
    )


def daily_metrics_query(start: date, end: date):
    a_p_join = action_purchases_join()
    query = select(
        action_table.c.site_id,
        func.date(action_table.c.datetime),
        func.sum(purchase_table.c.quantity).label('daily_purchases'),
        func.count(distinct(action_table.c.user_id)).label('daily_users')
    ).select_from(a_p_join).where(
        and_(
            action_table.c.datetime >= start,
            action_table.c.datetime <= end
        )
    ).group_by(
        action_table.c.site_id,
        func.date(action_table.c.datetime)
    )
    return query


def aggregate_table_query(start: date, end: date):
    metrics_query = daily_metrics_query(start=start, end=end)
    query = select(
        metrics_query.c.site_id.label('site_id'),
        func.avg(metrics_query.c.daily_purchases).label('avg_daily_purchases'),
        func.sum(metrics_query.c.daily_purchases).label('purchases'),
        func.avg(metrics_query.c.daily_users).label('avg_daily_users')
    ).select_from(
        metrics_query
    ).group_by(
        metrics_query.c.site_id
    )
    return query


def daily_product_purchases_query(product: ProductType, start: date, end: date):
    a_p_join = action_purchases_join()
    query = select(
        action_table.c.site_id,
        func.date(action_table.c.datetime),
        func.sum(purchase_table.c.quantity).label('daily_purchases')
    ).select_from(a_p_join).where(
        and_(
            purchase_table.c.type == product.value,
            action_table.c.datetime >= start,
            action_table.c.datetime <= end
        ),
    ).group_by(
        action_table.c.site_id,
        func.date(action_table.c.datetime)
    )
    return query


def total_product_purchases(product: ProductType, start: date, end: date):
    d_p_query = daily_product_purchases_query(product=product, start=start, end=end)

    query = select(
        d_p_query.c.site_id.label('site_id'),
        func.sum(d_p_query.c.daily_purchases).label(f'{product.value}_purchases')
    ).select_from(
        d_p_query
    ).group_by(
        d_p_query.c.site_id
    )
    return query


def avg_daily_product_purchases(product: ProductType, start: date, end: date):
    d_p_query = daily_product_purchases_query(product=product, start=start, end=end)

    query = select(
        d_p_query.c.site_id.label('site_id'),
        func.avg(d_p_query.c.daily_purchases).label(f'{product.value}_avg_daily_purchases')
    ).select_from(
        d_p_query
    ).group_by(
        d_p_query.c.site_id
    )
    return query


def unique_users(start: date, end: date):
    query = select(
        action_table.c.site_id.label('site_id'),
        func.count(distinct(action_table.c.user_id)).label('unique_users')
    ).where(
        and_(
            action_table.c.datetime >= start,
            action_table.c.datetime <= end
        )
    ).group_by(action_table.c.site_id)
    return query
