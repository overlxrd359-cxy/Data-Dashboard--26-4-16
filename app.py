import streamlit as st
import pandas as pd
import plotly.express as px

# --- 页面配置 ---
st.set_page_config(page_title="销售数据仪表盘", page_icon="📊", layout="wide")

# --- 标题 ---
st.title("📊 简易销售数据仪表盘")
st.markdown("---")

# --- 加载数据 ---
@st.cache_data # 缓存数据，提高加载速度
def load_data():
    try:
        df = pd.read_csv("sales_data.csv")
        df['日期'] = pd.to_datetime(df['日期']) # 确保日期格式正确
        return df
    except FileNotFoundError:
        st.error("❌ 未找到 sales_data.csv 文件，请先生成数据！")
        return None

df = load_data()

if df is not None:
    # --- 侧边栏过滤器 ---
    st.sidebar.header("🔍 筛选条件")
    
    # 获取唯一类别
    categories = df['类别'].unique()
    selected_category = st.sidebar.multiselect(
        "选择产品类别:",
        options=categories,
        default=categories
    )
    
    # 根据筛选条件过滤数据
    filtered_df = df[df['类别'].isin(selected_category)]
    
    if filtered_df.empty:
        st.warning("⚠️ 所选类别下没有数据。")
    else:
        # --- 关键指标 (KPIs) ---
        total_sales = filtered_df['总金额'].sum()
        avg_order_value = filtered_df['总金额'].mean()
        total_orders = filtered_df.shape[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 总销售额", f"¥{total_sales:,.2f}")
        col2.metric("📈 平均订单价值", f"¥{avg_order_value:,.2f}")
        col3.metric("📦 总订单数", total_orders)
        
        st.markdown("---")
        
        # --- 图表区域 ---
        col_chart1, col_chart2 = st.columns(2)
        
        # 图表 1: 每日销售趋势
        with col_chart1:
            st.subheader("📅 每日销售趋势")
            daily_sales = filtered_df.groupby('日期')['总金额'].sum().reset_index()
            fig_line = px.line(daily_sales, x='日期', y='总金额', title='销售额随时间变化')
            st.plotly_chart(fig_line, use_container_width=True)
            
        # 图表 2: 各类别销售占比
        with col_chart2:
            st.subheader("🥧 类别销售占比")
            category_sales = filtered_df.groupby('类别')['总金额'].sum().reset_index()
            fig_pie = px.pie(category_sales, values='总金额', names='类别', title='销售额分布')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        # --- 原始数据展示 ---
        st.subheader("📋 详细数据表")
        st.dataframe(filtered_df.sort_values(by='日期', ascending=False), use_container_width=True)

else:
    st.info("💡 提示: 请运行 generate_data.py 生成测试数据后再刷新页面。")

#streamlit run app.py 终端运行