import streamlit as st
import pandas as pd
from utils import perform_search, get_data_statistics

st.set_page_config(
    page_title="CSV可視化ツール",
    page_icon="📊",
    layout="wide"
)

def show_row_details(row):
    """選択された行の詳細をモーダルウィンドウで表示"""
    with st.modal("データ詳細"):
        st.subheader("選択行の詳細情報")
        # 2列レイアウトで項目と値を表示
        for col1, col2 in zip(row.index[::2], row.index[1::2] if len(row.index) > 1 else [None]):
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"**{col1}:**")
                st.write(row[col1])
            if col2:  # 2列目のデータがある場合のみ表示
                with cols[1]:
                    st.markdown(f"**{col2}:**")
                    st.write(row[col2])

        # 奇数個の列がある場合、最後の列を別途表示
        if len(row.index) % 2 != 0 and len(row.index) > 1:
            last_col = row.index[-1]
            st.markdown(f"**{last_col}:**")
            st.write(row[last_col])

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
            st.write("行をクリックすると詳細が表示されます")

            # 選択可能なデータフレームの表示
            if not filtered_df.empty:
                selected_row_index = st.selectbox(
                    "行を選択してください",
                    options=range(len(filtered_df)),
                    format_func=lambda x: f"行 {x+1}",
                    key="row_selector"
                )

                # データフレームの表示
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    height=400,
                    hide_index=True
                )

                # 選択された行の詳細表示
                if st.button("選択した行の詳細を表示"):
                    selected_row = filtered_df.iloc[selected_row_index]
                    show_row_details(selected_row)

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