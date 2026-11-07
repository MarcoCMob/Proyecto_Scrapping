from database.connection import SessionLocal
from services.job_offer_service import JobOfferService
from modulos.matching.embedding_service import EmbeddingService
from modulos.matching.text_builder import build_offer_text

emb = EmbeddingService()
tokenizer = emb.model.tokenizer

print("max_seq_length:", emb.model.max_seq_length)

with SessionLocal() as session:
    offers = JobOfferService(session).get_all_offers()

    for offer in offers:
        n = len(tokenizer(build_offer_text(offer))["input_ids"])
        print(f"{n:5d} tokens | {offer.title[:55]}")