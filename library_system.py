"""Library fine and book renewal tracker for a campus library."""
import ast
import json
import operator
from datetime import datetime

# Global state
loans = {}
FINE_PER_DAY = 2
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def add_book_loan(student_id, book_id, dates=None):
    """Record that a student borrowed a book."""
    if not student_id:
        print(f"Cannot record loan of {book_id}: missing student id")
        return
    if not isinstance(book_id, str) or not book_id:
        print(f"Cannot record loan for {student_id}: "
              "book id must be a non-empty string")
        return
    if dates is None:
        dates = []
    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(f"{student_id} borrowed {book_id} "
          f"(loan dates on record: {len(dates)})")


def return_book(student_id, book_id):
    """Remove a book from a student's loans, reporting unknown loans."""
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        print(f"Cannot return {book_id}: {student_id} has no such loan")


def calculate_fine(days_overdue):
    """Return the fine for a number of overdue days (never negative)."""
    return max(days_overdue, 0) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew a book; renewing must not change the global fine rate."""
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    """Load loan records from a JSON file into the global loans dict."""
    try:
        with open(file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(f"Could not load records from {file}: {err}")
        return
    loans.clear()
    loans.update(data)


def save_records(file="loans.json"):
    """Save the global loans dict to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(loans))


def _eval_node(node, days):
    """Evaluate an arithmetic expression where `days` is the only name."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, days)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "days":
        return days
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left, days),
                                   _eval_node(node.right, days))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand, days))
    raise ValueError("Unsupported expression in fine rule")


def fine_from_rule(rule, days):
    """Compute a fine from a rule such as 'days * 2 + 10' without eval()."""
    return _eval_node(ast.parse(rule, mode="eval"), days)


def print_report():
    """Print every student and the books they currently hold."""
    print("Loan Report")
    for student, books in loans.items():
        print(student, "->", books)


def main():
    """Run the demo scenario."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # book id should be a string
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    try:
        print("S102 owes:", calculate_fine(int(days)))
    except ValueError:
        print(f"'{days}' is not a whole number of days")
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
