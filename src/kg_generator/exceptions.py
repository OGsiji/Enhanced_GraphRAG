class KGGeneratorError(Exception):
    """Base exception for KG Generator"""
    pass

class PDFProcessingError(KGGeneratorError):
    """Raised when PDF processing fails"""
    pass

class KnowledgeGraphError(KGGeneratorError):
    """Raised when knowledge graph operations fail"""
    pass
