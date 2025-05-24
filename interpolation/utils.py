import streamlit as st


def are_x_values_unique(points):
    if _has_duplicate_x_values(points):
        st.error("**Error:** Input points must not have repeated $x$-values.")
        return False
    return True


def _has_duplicate_x_values(points):
    unique_points = set(points)
    have_same_length = len(points) == len(unique_points)
    return not have_same_length
