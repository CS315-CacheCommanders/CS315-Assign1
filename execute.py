# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_execute BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics

def update_locations(disk_locations, name_satisfied, year_condition):
    start_index = name_satisfied[1][0]
    years = name_satisfied[2]
    target_year = int(year_condition[2])
    operator = year_condition[1]
    
    for i, year in enumerate(years):
        if (operator == "=" and year == target_year) or \
            (operator == ">=" and year >= target_year) or \
            (operator == "<=" and year <= target_year):
            disk_locations.append(start_index + i)

################################
# Non Editable Region Starting #
################################
def my_execute(clause, idx):
################################
#  Non Editable Region Ending  #
################################
    clause_length = len(clause)
    leaf_nodes = idx[0].leaves
    if clause_length == 1:
        # Single condition clause: either "name" or "year" clause
        condition = clause[0]
        if condition[0] == "name":
            # Handle "name" clause
            if condition[1] == "LIKE":
                pattern = condition[2][1:-1]  # Remove surrounding quotes
                pattern_start = idx[0].pattern_search(pattern)
                pattern_end = pattern[:-1] + "zzzzzzzzz"
                if pattern_start[0][1] is None or pattern_start[0][1].keys[pattern_start[0][0]] > pattern_end:
                    disk_locations = []
                else:
                    start_index = pattern_start[0][0]
                    end_index = pattern_start[1][0]
                    start_location = pattern_start[0][1].children[start_index][1][0]
                    end_location = pattern_start[1][1].children[end_index][1][1]
                    disk_locations = list(range(start_location, end_location + 1))
            else:
                # Handle "name =" clause
                name_value = condition[2][1:-1]  # Remove surrounding quotes
                search_result = idx[0].search_name(name_value)
                if not search_result:
                    disk_locations = []
                else:
                    start_location = search_result[1][0]
                    end_location = search_result[1][1]
                    disk_locations = list(range(start_location, end_location + 1))
        else:
            # Handle "year" clause
            year = int(condition[2])
            year_offset = year - 1900
            base_offset = idx[2]
            year_range = idx[1][year_offset]
            if condition[1] == "=":
                if year_range[0] > year_range[1]:
                    disk_locations = []
                else:
                    disk_locations = list(range(base_offset + year_range[0], base_offset + year_range[1] + 1))
            elif condition[1] == ">=":
                disk_locations = list(range(base_offset + year_range[0], base_offset + base_offset))
            elif condition[1] == "<=":
                start_location = year_range[0]
                end_location = year_range[1]
                if end_location >= start_location:
                    disk_locations = list(range(base_offset, base_offset + end_location + 1))
                else:
                    disk_locations = list(range(base_offset, base_offset + start_location)) if start_location > 0 else []
    else:
        # Conjunctive query with both "name" and "year" conditions
        name_condition = clause[0]
        year_condition = clause[1]
        if name_condition[1] == "LIKE":
            pattern = name_condition[2][1:-1]  # Remove surrounding quotes
            pattern_start = idx[0].pattern_search(pattern)
            pattern_end = pattern[:-1] + "zzzzzzzzz"
            if pattern_start[0][1] is None or pattern_start[0][1].keys[pattern_start[0][0]] > pattern_end:
                disk_locations = []
            else:
                start_index = pattern_start[0][0]
                end_index = pattern_start[1][0]
                start_location = pattern_start[0][1].children[start_index][1][0]
                end_location = pattern_start[1][1].children[end_index][1][1]
                disk_locations = []
                start_node = pattern_start[0][1]
                end_node = pattern_start[1][1]
                if start_node == end_node:
                    for i in range(start_index, end_index + 1):
                        current_child = start_node.children[i]
                        update_locations(disk_locations, current_child, year_condition)
                else:
                    for i in range(start_index, len(start_node.children)):
                        current_child = start_node.children[i]
                        update_locations(disk_locations, current_child, year_condition)
                    current_node = leaf_nodes[start_node.ind + 1]
                    while current_node != end_node:
                        for child in current_node.children:
                            update_locations(disk_locations, child, year_condition)
                        current_node = leaf_nodes[current_node.ind + 1]
                    for i in range(0, end_index + 1):
                        current_child = current_node.children[i]
                        update_locations(disk_locations, current_child, year_condition)
        else:
            # Handle "name =" condition in conjunctive query
            name_value = name_condition[2][1:-1]  # Remove surrounding quotes
            search_result = idx[0].search_name(name_value)
            if not search_result:
                disk_locations = []
            else:
                start_location = search_result[1][0]
                end_location = search_result[1][1]
                disk_locations = []
                update_locations(disk_locations, search_result, year_condition)
                
	# Use this method to take a WHERE clause specification
	# and return results of the resulting query
	# clause is a list containing either one or two predicates
	# Each predicate is itself a list of 3 objects, column name, comparator and value
	# idx contains the packaged variable returned by the my_index method
	
	# THE METHOD MUST RETURN A SINGLE LIST OF INDICES INTO THE DISK MAP
    return disk_locations