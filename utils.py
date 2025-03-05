"""Utility functions used in the games.py implementation."""

def vector_add(a, b):
    """Component-wise addition of two vectors (tuples, lists, or arrays).
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        A vector where each component is the sum of the corresponding components
        of a and b.
    """
    return tuple(x + y for x, y in zip(a, b))
