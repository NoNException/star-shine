from pandas import DataFrame
import streamlit as st
import math


@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df


def pagination_container(
    dataset: DataFrame,
    save_func,
    data_editor=False,
):
    """
    将 dataset 进行分页展示
    :param dataset: 进行分页的数据源
    :param save_func: 保存函数, 传入 dataset
    :param data_editor: True 是否允许编辑 DataFrame 中的数据
    """

    orginal_data_ids = [int(u["id"]) for _, u in dataset.iterrows()]
    pagination = st.container()
    top_menu = pagination.columns((2, 1, 1, 1))
    with top_menu[0]:
        sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=True)
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("Sort By", options=dataset.columns)
        with top_menu[2]:
            sort_direction = st.radio("Direction", options=["⬆️", "⬇️"], horizontal=True)
        dataset = dataset.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )
        with top_menu[3]:
            save = st.button("Save Data")
            st.session_state.save_data = save
    pagination_data_container = pagination.container()

    bottom_menu = pagination.columns((3, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[5, 25, 50, 100])
    with bottom_menu[1]:
        total_pages = math.ceil(len(dataset) / batch_size)
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(
            f"Page **{current_page}** of **{total_pages}** Total: {len(dataset)} "
        )

    pages = split_frame(dataset, batch_size)
    # data in single pages
    page_data = pages[current_page - 1]
    if data_editor:
        editor_df = pagination_data_container.data_editor(
            data=page_data, num_rows="dynamic", use_container_width=True
        )
        if st.session_state.save_data:
            # TODO 在表格中无法删除数据
            save_func(orginal_data_ids, editor_df)
            st.session_state.save_data = False
            st.rerun()

    else:
        pagination_data_container.dataframe(data=page_data, use_container_width=True)
