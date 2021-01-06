def get_best_books():
    ten_best_books = list(
        mongo.db.books.find().sort("average_grade", -1).limit(10)
    )

    number_count = 1
    for book in ten_best_books:
        book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)
        book["place"] = number_count
        book["stars"] = int(round(float(book["average_grade"]), 0))

        number_count += 1

    return ten_best_books


def get_colours():
    return [
        'darkgreen', 'acid', 'sandy', 'orange', 'brown'
        ]


def get_groups():
    cat_groups = list(mongo.db.category_groups.find())
    category_groups = []
    colours = get_colours()
    length = len(colours)
    index = 0
    for group in cat_groups:
        category_groups.append(
            {
                "group_name": group['group_name'],
                "colour": colours[index % length]
            }
        )
        index += 1

    return category_groups