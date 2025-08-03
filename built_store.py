# from crm_extractor import (
#     get_contacts, get_accounts,
#     get_activities, get_leads, get_opportunities
# )

# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document

# embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# def to_document(text, metadata):
#     return Document(page_content=text, metadata=metadata)

# def prepare_documents():
#     docs = []

#     # Contacts
#     for contact in get_contacts():
#         docs.append(to_document(contact, {"type": "contact"}))

#     # Accounts
#     for acc in get_accounts():
#         docs.append(to_document(acc, {"type": "account"}))

#     # Activities
#     for act in get_activities():
#         docs.append(to_document(act, {"type": "activity"}))

#     # Leads
#     for lead in get_leads():
#         docs.append(to_document(lead, {"type": "lead"}))

#     # Opportunities
#     for opp in get_opportunities():
#         docs.append(to_document(opp, {"type": "opportunity"}))

#     return [d for d in docs if d.page_content.strip()]

# # Build and save the index
# all_docs = prepare_documents()

# if not all_docs:
#     print("❌ No CRM documents found.")
# else:
#     print(f"✅ Embedding {len(all_docs)} records as documents...")
#     db = FAISS.from_documents(all_docs, embedding)
#     db.save_local("faiss_index")
#     print("✅ Vector store saved at ./faiss_index")

from crm_extractor import (
    get_contacts, get_accounts,
    get_activities, get_leads, get_opportunities
)
from embed_store import build_vector_store, search

contact_chunks = get_contacts()
account_chunks = get_accounts()
activity_chunks = get_activities()
lead_chunks = get_leads()
opportunity_chunks = get_opportunities()
data = contact_chunks + account_chunks
if not data:
    print("[ERROR] No CRM data returned. Vector store not built.")
else:
    build_vector_store(data)
all_data = (
    contact_chunks + account_chunks +
    activity_chunks + lead_chunks + opportunity_chunks
)

if not all_data:
    print("[ERROR] No CRM data returned. Vector store not built.")
else:
    print(f"[INFO] Total CRM records: {len(all_data)}")
    build_vector_store(all_data)
