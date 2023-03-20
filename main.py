def parse_sql(sql_query):
    final_query = {
      'fields' : '',
      'table' : '',
      'where' : {},
      'order_by' : {},
      'limit' : 0
    }
    words = []
    columns = []
    table = []
    where = []
    order_by = []
    limit = []
    
    # This is where the input SQL query is stripped of all the extra characters and split on the spaces
    clean_query = sql_query.split(' ')
    
    for i in clean_query:
        words.append(i.lower())

    temp_words = words.copy()
    temp = 0

    for i, val in enumerate(words):
       if '=' in val:
          equal_sign = val.index('=')
          temp_words[i + temp] = val[:equal_sign]
          temp_words.insert(i + temp + 1,'=')
          temp_words.insert(i + temp + 2, val[(equal_sign + 1):len(val)])
          temp += 2
          
    words = temp_words
    words = [i.strip(", '") for i in words]

    # These for loops are going through the SQL query searching for specific info to add into the appointed list
    for i in words:
      if i == 'from':
        break
      else:
        columns.append(i)

    for i in words:
       if i == 'where' or i == 'order':
          break
       elif i not in columns and i != 'from':
          table.append(i)

    for i in words[::-1]:
       if 'limit' not in words:
          break
       if i == 'limit':
          break
       else:
          limit.append(i)

    for i in limit:
       if i.isdigit():
          int(i)
       else:
          limit.clear()

    for i in words[::-1]:
       if 'order' not in words:
          break
       if i == 'by':
          break
       else:
          order_by.append(i)    

    for i in words[::-1]:
       if 'where' not in words:
          break
       if i == "where":
          break
       elif i not in order_by and i not in limit and i != 'order' and i != 'by' and i != '':
          where.append(i)

    # This will clean up all the lists and put them in the right order
    if 'limit' in order_by:
       order_by.pop(0)
       order_by.pop(0)

    if len(where) > 1:
       where.reverse()

    order_by.reverse()
    limit.reverse()    
    columns.pop(0)

    # This is where all the lists that were created are added into the final dictionary
    final_query['fields'] = columns
    final_query['table'] = table[0]

    if len(where) >= 1:
         final_query['where'][where[0]] = where[2]
    
    if len(order_by) >= 1:
        final_query['order_by']['field'] = order_by[0]
        final_query['order_by']['order'] = order_by[1]
      
    if len(limit) >= 1:
      limit[0] = int(limit[0])
      final_query['limit'] = final_query['limit'] + limit[0]
          
    return final_query
    

query = "SELECT * FROM Products"
query1 = "SELECT name, make, model, price FROM Products ORDER BY price DESC"
query2 = "SELECT name, model FROM Products WHERE make = 'Apple'"
query3 = "SELECT first_name, last_name, email FROM Cohorts WHERE first_name='John'"
query4 = "SELECT city, state from Customers where state='UT' ORDER BY city ASC"
query5 = "SELECT * FROM Courses ORDER BY name ASC LIMIT 20"
query6 = "SELECT name, model, price FROM Products WHERE make='Apple' AND active=1"
query7 = "SELECT name, model, price FROM Products WHERE make LIKE '%Apple%' AND price < 1100.00 ORDER BY price DESC"


print(parse_sql(query))
print(parse_sql(query1))
print(parse_sql(query2)) 
print(parse_sql(query3))  
print(parse_sql(query4)) 
print(parse_sql(query5)) 
print(parse_sql(query6)) 
print(parse_sql(query7))   