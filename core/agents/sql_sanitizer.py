def sanitize_sql(sql):

    sql_upper = sql.upper()

    forbidden = ["DISTINCT", "WITH"]

    for word in forbidden:
        if word in sql_upper:
            raise ValueError(f"Forbidden SQL construct detected: {word}")

    if ";" in sql:
        sql = sql.split(";")[0]

    return sql