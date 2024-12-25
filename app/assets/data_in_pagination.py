import streamlit as st


@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df


def pagination_container(dataset, data_editor=False):
    """
    将 dataset 进行分页展示
    :param dataset: 进行分页的数据源
    :param data_editor: True 是否允许编辑 DataFrame 中的数据
    """

    pagination = st.container()
    top_menu = pagination.columns(3)
    with top_menu[0]:
        sort = pagination.radio("Sort Data", options=["Yes", "No"])
    if sort == "Yes":
        with top_menu[1]:
            sort_field = pagination.selectbox("Sort By", options=dataset.columns)
        with top_menu[2]:
            sort_direction = pagination.radio(
                "Direction", options=["⬆️", "⬇️"], horizontal=True
            )
        dataset = dataset.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )
    pagination_data_container = pagination.container()

    bottom_menu = pagination.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = pagination.selectbox("Page Size", options=[25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
        )
        current_page = pagination.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        pagination.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(dataset, batch_size)
    # data in single pages
    page_data = pages[current_page - 1]
    if data_editor:
        pagination_data_container.data_editor(
            data=page_data, num_rows="dynamic", use_container_width=True
        )
    else:
        pagination_data_container.dataframe(data=page_data, use_container_width=True)
