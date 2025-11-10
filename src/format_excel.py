def format_excel(df, required_cols):
    """指定の列がすべて含まれているかチェックする"""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"次の列が見つかりません: {missing_str}")
    return True