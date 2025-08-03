# formatters.py

def format_contact(item):
    return f"👤 Contact: {item.get('fullname', 'N/A')}, Company: {item.get('company', 'N/A')}, Phone: {item.get('phone', 'N/A')}"

def format_account(item):
    return f"🏢 Account: {item.get('name', 'N/A')}, Phone: {item.get('phone', 'N/A')}"

def format_activity(item):
    return f"📅 Activity: {item.get('subject', 'N/A')} | Status: {item.get('status', 'N/A')} | Date: {item.get('start', 'N/A')}"

def format_lead(item):
    return f"🧲 Lead: {item.get('topic', 'N/A')} | Status: {item.get('status', 'N/A')} | Owner: {item.get('owner', 'N/A')}"

def format_opportunity(item):
    return f"💼 Opportunity: {item.get('name', 'N/A')} | Est. Revenue: {item.get('revenue', 'N/A')} | Close Date: {item.get('close_date', 'N/A')}"


# This registry maps types to functions dynamically
format_registry = {
    "contact": format_contact,
    "account": format_account,
    "activity": format_activity,
    "lead": format_lead,
    "opportunity": format_opportunity,
}


def format_items(items: list, data_type: str) -> list:
    """
    Dynamically formats a list of items based on their type.
    """
    formatter = format_registry.get(data_type)
    if not formatter:
        return [str(i) for i in items]  # fallback: plain string
    return [formatter(item) for item in items]
