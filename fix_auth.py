# Script para fix auth.py - add except blocks inside search_formularios_e14 function

with open('backend/routes/auth.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# The function search_formularios_e14:
# - def at line 372 (index 371): 4 spaces
# - try: at line 374 (index 373): 8 spaces (inside function)
# - body: lines 375-430 (indices 374-429): 12-20 spaces (inside function)
# - Currently line 431 (index 430): 0 spaces ')),\n' - module level, function ended

# I need to insert except blocks at 8 spaces INSIDE the function,
# after the try body and before the function ends at 0 spaces.

# Keep lines 1 to 430 (indices 0 to 429) - the function up to where it ends
# But the except blocks need to be inserted at 8 spaces after the body.

# Actually, let me reconsider. The current structure has:
# - Lines 1-430: function code (including try at 8 spaces and body at 12-20 spaces)
# - Line 431+: orphan except blocks at 4 spaces (module level, wrong)

# What I'll do: keep lines 1-430, then add the correct except blocks at 8 spaces,
# then skip the orphan except blocks.

# The except blocks to add (at 8 spaces, inside the function):
except1 = '    except BaseAPIException as e:\n        return jsonify(e.to_dict()), e.status_code\n'
except2 = '    except Exception as e:\n        return jsonify({\n            "success": False,\n            "error": str(e)\n        }), 500\n'

# New file: lines 0-429 (first 430 lines) + except blocks + skip orphan blocks
new_lines = lines[:430] + [except1, except2]

with open('backend/routes/auth.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Done: File rewritten with except blocks inside search_formularios_e14 function')