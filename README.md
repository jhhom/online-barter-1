## Online Barter

**Live at**\
https://serene-tundra-55963.herokuapp.com/

A semantic web application to barter for items online.

**What semantic functionality is available?**

`market` page will rank the items that has the same category as the user's most favourited category.

**How does it work?**

The functionality can be found on [`market` view](https://github.com/maxosen/online-barter-1/blob/main/market/views.py#L123-L128).
```python
most_favourited = statistics.mode(
    [item.category for item in Item.objects.filter(favourited_by=request.user)]
)
results \
    .extra(select={'match': f'category="{most_favourited}"'}) \
    .order_by('-match')
```

The results are ordered by the category that match the most favourited items first.

## Admin
https://serene-tundra-55963.herokuapp.com/admin

## Available pages
Following pages are available:

1. `*/market`
2. `*/add_item`
3. `*/login`
4. `*/logout`
5. `*/register`
6. `*/settings`
7. `*/traded_items`
8. `*/item/?id=<item-id>` (Replace `<item-id>` with actual item id)
9. `*/profile`
10. `*/admin`

Where `*` represents the home URL:\
`https://serene-tundra-55963.herokuapp.com/`

**Following pages require login**

1. profile
2. traded_items
3. add_item
4. settings

**Following pages are not mobile-friendly ❌📱**:

1. market
2. traded_items
3. item

All pages except `admin` and `index` are defined in [`market/views.py`](https://github.com/maxosen/online-barter-1/blob/main/market/views.py) and registered in [`market/urls.py`](https://github.com/maxosen/online-barter-1/blob/main/market/urls.py)

