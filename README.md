Technical Implementation: Hybrid Retrieval
Vector Search: Used for semantic similarity (understanding that "revenue" and "earnings" are related).

BM25 Keyword Search: Implemented to handle "Out-of-Vocabulary" terms like specific part numbers, dates, or rare names that standard embeddings might overlook.

Outcome: Improved retrieval accuracy for technical documentation by combining the strengths of both neural and lexical search.