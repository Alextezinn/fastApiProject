from sqlalchemy import or_

from fastApiProject.db import database
from fastApiProject.models import *


async def get_posts(page, theme, rating, q):
    if theme != "" or rating != "" or q != "":
        query = await get_query_post_by_filter(theme, rating, q)

        try:
            posts_page = await database.fetch_all(query=query)
        except Exception:
            return []

        return [dict(result) for result in posts_page]

    return await get_pagination_post(page)


async def get_pagination_post(page):
    query = posts.select().offset((page-1)*10).limit(10)
    posts_page = await database.fetch_all(query=query)
    return [dict(result) for result in posts_page]


async def get_query_post_by_filter(theme, rating, q):
    query = posts.select()

    if theme != "":
        query = query.where(posts.c.subject.contains(theme))

    if rating != "":
        try:
            if "__" in rating:
                bottom_rating, top_rating = rating.split("__")
                query = query.where(posts.c.rating>=int(bottom_rating),
                                    posts.c.rating<=int(top_rating))
            else:
                query = query.where(posts.c.rating == int(rating))

        except ValueError:
            query = None

    if q != "":
        query = query.where(or_(posts.c.subject.contains(q),
                                posts.c.name.contains(q)))

    return query
