import pandas as pd
import numpy as np

def perform_search(df: pd.DataFrame, search_terms: str) -> pd.DataFrame:
    """
    データフレームに対して複数キーワード検索を実行します。

    Args:
        df: 入力データフレーム
        search_terms: スペース区切りの検索キーワード

    Returns:
        全ての検索キーワードを含む行のみのデータフレーム
    """
    if not search_terms.strip():
        return df

    # 検索キーワードを分割して小文字に変換
    terms = [term.lower().strip() for term in search_terms.split()]

    # 全ての検索キーワードを含む行を特定するマスクを作成
    mask = pd.Series([True] * len(df), index=df.index)

    for term in terms:
        term_mask = pd.Series([False] * len(df), index=df.index)
        # 全ての列に対して検索
        for column in df.columns:
            term_mask |= df[column].astype(str).str.lower().str.contains(term, na=False)
        mask &= term_mask

    return df[mask]

def get_data_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    データフレームの統計情報を生成します。

    Args:
        df: 入力データフレーム

    Returns:
        各列の統計情報を含むデータフレーム
    """
    stats = []

    for column in df.columns:
        column_stats = {
            "列名": column,
            "データ型": str(df[column].dtype),
            "ユニーク値数": df[column].nunique(),
            "欠損値数": df[column].isna().sum()
        }

        # 数値型の列に対する追加の統計情報
        if np.issubdtype(df[column].dtype, np.number):
            column_stats.update({
                "平均値": df[column].mean(),
                "中央値": df[column].median(),
                "標準偏差": df[column].std(),
                "最小値": df[column].min(),
                "最大値": df[column].max()
            })

        stats.append(column_stats)

    stats_df = pd.DataFrame(stats)
    return stats_df.set_index("列名")