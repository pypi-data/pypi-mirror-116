import re


def _repl(m, args, result) -> str:
    k = m.group(1)
    if k in args:
        result.append(args[k])
        return '%s'
    else:
        return m.group(0)


def transform_named_sql(named_sql: str, args: dict, pattern=r":(\w+)") -> (str, []):
    """
    eg.
    named_sql = "select * from user where name=:name and password=:password"
    sql,args = transform_named_sql(named_sql,{'name':'jim','_name':'zz'})
    :param named_sql:
    :param args:
    :param pattern:
    :return:
    """
    result = []
    return re.sub(pattern, lambda x: _repl(x, args, result),named_sql) ,result


