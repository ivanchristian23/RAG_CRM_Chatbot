from crm_extractor import get_contacts
from embed_store import build_vector_store

data = get_contacts()
if data:
    build_vector_store(data)
    print("✅ Vector store built and saved.")
else:
    print("❌ No CRM data found. Vector store not created.")
