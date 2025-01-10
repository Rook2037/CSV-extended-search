import streamlit as st
import pandas as pd
from utils import perform_search, get_data_statistics

st.set_page_config(
    page_title="CSV可視化ツール",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("CSV可視化・分析ツール 📊")

    # ファイルアップロードセクション
    st.header("1. CSVファイルのアップロード")
    uploaded_file = st.file_uploader("CSVファイルを選択してください", type="csv")

    if uploaded_file is not None:
        try:
            # CSVファイルの読み込み
            df = pd.read_csv(uploaded_file)

            # 基本情報の表示
            st.header("2. データの概要")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"総行数: {len(df)}")
            with col2:
                st.write(f"総列数: {len(df.columns)}")

            # 統計情報セクション
            st.header("3. データの統計情報")
            stats = get_data_statistics(df)
            st.write(stats)

            # 検索セクション
            st.header("4. 検索とフィルタリング")
            search_terms = st.text_input(
                "検索キーワードを入力してください（複数の単語はスペースで区切ってください）",
                help="入力された全ての単語を含む行が表示されます"
            )

            # 列フィルター
            st.subheader("列の選択")
            columns_to_display = st.multiselect(
                "表示する列を選択してください",
                options=list(df.columns),
                default=list(df.columns)
            )

            # ソートオプション
            st.subheader("データの並び替え")
            sort_column = st.selectbox("並び替えの基準となる列", options=["なし"] + list(df.columns))
            sort_order = st.radio("並び順", options=["昇順", "降順"])

            # フィルターとソートの適用
            filtered_df = df[columns_to_display]

            if sort_column != "なし":
                filtered_df = filtered_df.sort_values(
                    by=sort_column,
                    ascending=(sort_order == "昇順")
                )

            # 検索条件の適用
            if search_terms:
                filtered_df = perform_search(filtered_df, search_terms)

            # 結果の表示
            st.header("5. 結果")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )

            # フィルター済みデータのダウンロード
            st.download_button(
                label="フィルター済みデータをCSVでダウンロード",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='filtered_data.csv',
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"ファイルの処理中にエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()