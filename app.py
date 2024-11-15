import streamlit as st
import pandas as pd
from wallet_analyzer import WalletAnalyzer
from datetime import datetime
import time

# 配置頁面
st.set_page_config(
    page_title="Solana錢包分析",
    page_icon="🔍",
    layout="wide"
)

# 設置樣式
st.markdown("""
   <style>
   /* ===== 1. 基礎布局設置 ===== */
   /* 隱藏 Streamlit 默認的頂部菜單和標題 */
   #MainMenu {visibility: hidden;}
   header {visibility: hidden;}
   
   /* 設置主背景色 */
   .main {
       background-color: #f3f4f6;
   }
   
   /* 調整整體容器的內邊距 */
   .block-container {
       padding-top: 0rem !important;
       padding-bottom: 0rem !important;
       padding-left: 1rem;
       padding-right: 1rem;
       max-width: 100% !important;
   }

   /* ===== 2. 區塊布局調整 ===== */
   /* 壓縮所有區塊的間距 */
   div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
       background-color: white;
       padding: 0.5rem !important;
       border-radius: 0.5rem;
       box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
       margin-bottom: 0.25rem !important;
   }

   /* ===== 3. 右側交易記錄區域高度調整 ===== */
   /* 設置固定高度和滾動 */
   [data-testid="column"]:last-child .stDataFrame {
       height: 650px !important;
       overflow-y: auto !important;
   }
   
   /* 確保表格內容正確顯示 */
   [data-testid="column"]:last-child .stDataFrame > div {
       height: 100% !important;
   }
   
   [data-testid="column"]:last-child .stDataFrame [data-testid="StyledDataFrameDataCell"] {
       min-height: 35px !important;
       max-height: 35px !important;
       line-height: 35px !important;
   }

   /* Tab 容器高度調整 */
   [data-testid="column"]:last-child .stTabs {
       height: 750px !important;
   }

   [data-testid="column"]:last-child [data-baseweb="tab-panels"] {
       height: calc(100% - 50px) !important;
   }

   [data-testid="column"]:last-child [data-baseweb="tab-panel"] {
       height: 100% !important;
       overflow: hidden !important;
   }

   /* ===== 4. 標題和文本樣式 ===== */
   /* 減小標題的大小和間距 */
   h1, h2, h3 {
       margin-top: 0 !important;
       margin-bottom: 0.25rem !important;
       padding: 0 !important;
       font-size: 1.2rem !important;
   }

   /* ===== 5. 輸入區域樣式 ===== */
   /* 文本輸入框樣式 */
   .stTextArea > div {
       border: none !important;
   }

   .stTextArea > div:focus-within {
       box-shadow: none !important;
       border-color: transparent !important;
   }

   .stTextArea textarea {
       border: 1px solid #e5e7eb !important;
       border-radius: 0.375rem !important;
   }

   .stTextArea textarea:focus {
       box-shadow: none !important;
       border-color: #e5e7eb !important;
   }

   /* 按鈕樣式 */
   .stButton > button {
       padding: 0.3rem 1rem !important;
       font-size: 0.8rem !important;
       width: 100%;
       background-color: #0D0D0D !important;
       color: #FFF !important;
       border: none;
       border-radius: 0.375rem;
       font-weight: 500;
       margin-top: 0.5rem;
       transition: all 0.3s ease;
   }

   .stButton > button:hover {
       color: #9B9B9B !important;
   }

   .stButton > button:active,
   .stButton > button[disabled] {
       background-color: rgba(13, 13, 13, 0.5) !important;
       cursor: not-allowed;
   }

   /* ===== 6. 指標卡片樣式 ===== */
   div[data-testid="column"] > div > div {
       padding: 0.3rem !important;
       margin-bottom: 0.25rem !important;
   }
   
   div[data-testid="stMetricLabel"] > div {
       font-size: 0.7rem !important;
       margin-bottom: 0.1rem !important;
       color: #6b7280;
   }
   
   div[data-testid="stMetricValue"] > div {
       font-size: 1rem !important;
       font-weight: 600;
   }

    /* ===== 7. 標籤頁樣式 ===== */
    /* 防止 Streamlit 主題覆蓋 */
    .st-emotion-cache-1y4p8pa,
    [data-testid="stAppViewContainer"] div[data-baseweb="tab-list"] {
        background-color: transparent !important;
        gap: 0 !important;
        padding: 0 !important;
    }

    /* Tab 容器底線 */
    .st-emotion-cache-1y4p8pa div[role="tablist"],
    [data-testid="stAppViewContainer"] div[role="tablist"] {
        border-bottom: 1px solid #e5e7eb !important;
    }

    /* 常規 Tab 樣式 */
    div[role="tablist"] button[role="tab"] {
        color: #6b7280 !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
        margin: 0 !important;
    }

    /* 選中狀態樣式 */
    div[role="tablist"] button[role="tab"][aria-selected="true"] {
        color: #0D0D0D !important;
        background-color: transparent !important;
        border-bottom: 2px solid #0D0D0D !important;
        font-weight: 500 !important;
    }

    /* 覆蓋選中指示器的顏色 */
    .st-emotion-cache-137l8c5,
    div[data-baseweb="tab-highlight"] {
        background-color: #0D0D0D !important;
    }

    /* Tab 內容區域 */
    [role="tabpanel"] {
        padding: 1rem 0 !important;
    }


   /* ===== 8. 表格樣式 ===== */
   .stDataFrame {
       font-size: 0.7rem !important;
       padding: 0.2rem !important;
   }
   
   .stDataFrame th {
       padding: 0.2rem !important;
       background-color: #f3f4f6 !important;
       position: sticky !important;
       top: 0 !important;
       z-index: 1 !important;
   }
   
   .stDataFrame td {
       padding: 0.2rem !important;
   }

   /* ===== 9. 滾動條樣式 ===== */
   ::-webkit-scrollbar {
       width: 6px;
       height: 6px;
   }
   
   ::-webkit-scrollbar-track {
       background: #f1f1f1;
       border-radius: 3px;
   }
   
   ::-webkit-scrollbar-thumb {
       background: #888;
       border-radius: 3px;
   }
   
   ::-webkit-scrollbar-thumb:hover {
       background: #555;
   }

   /* ===== 10. 顏色標示 ===== */
   .metric-positive {
       color: #10B981 !important;
   }
   
   .metric-negative {
       color: #EF4444 !important;
   }

   /* ===== 11. 響應式調整 ===== */
   @media (max-width: 640px) {
       .block-container {
           padding-left: 0.5rem;
           padding-right: 0.5rem;
       }
       
       div[data-testid="metric-container"] {
           padding: 0.75rem;
       }
       
       .stTabs [data-baseweb="tab"] {
           padding: 0.375rem 0.75rem;
           font-size: 0.813rem;
       }
   }
   </style>
    <style>
    /* 歷史檢索按鈕容器 */
    .history-container {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    /* 歷史檢索按鈕樣式 */
    .history-container [data-testid="stButton"] button {
        width: 100%;
        text-align: left;
        background-color: white !important;
        color: #1f2937 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem !important;
        font-size: 0.875rem !important;
        transition: all 0.2s;
        margin-top: 0 !important;
    }
    
    .history-container [data-testid="stButton"] button:hover {
        background-color: #f3f4f6 !important;
        border-color: #d1d5db !important;
    }
    
    /* 加強歷史檢索標題樣式 */
    .history-container h3 {
        margin-bottom: 0.5rem;
        color: #374151;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def format_number(num, use_full_number=False):
    """格式化數字顯示"""
    if isinstance(num, (int, float)):
        if use_full_number:
            return f"{int(num):,}"  # 顯示完整數字，帶千位分隔符
        if abs(num) >= 1e6:
            return f"{num/1e6:,.2f}M"
        elif abs(num) >= 1e3:
            return f"{num/1e3:,.2f}K"
        else:
            return f"{num:,.2f}"
    return str(num)

def get_market_cap_for_token(token_address, token_analysis):
    """從token_analysis中獲取代幣的首購市值"""
    if token_address in token_analysis['profit_tokens']:
        return token_analysis['profit_tokens'][token_address]['market_cap']
    if token_address in token_analysis['loss_tokens']:
        return token_analysis['loss_tokens'][token_address]['market_cap']
    return None

def get_timestamp_for_token(token_address, token_analysis):
    """從token_analysis中獲取代幣的首購時間戳"""
    if token_address in token_analysis['profit_tokens']:
        return token_analysis['profit_tokens'][token_address]['timestamp']
    if token_address in token_analysis['loss_tokens']:
        return token_analysis['loss_tokens'][token_address]['timestamp']
    return None


def main():
    # 初始化 session state
    if 'analyzed_wallets' not in st.session_state:
        st.session_state.analyzed_wallets = {}
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None

    # 創建三列佈局
    left_col, middle_col, right_col = st.columns([1, 2, 1.5])
    
    with left_col:
        st.markdown("### 🔍 Solana錢包分析器")
        with st.container():
            st.markdown("#### 🧑🏻‍💻 請輸入錢包地址")
            wallet_address = st.text_area(
                "輸入錢包地址",
                placeholder="每行輸入一個地址...",
                label_visibility="collapsed"
            )
            analyze_button = st.button("開始分析")

            if st.session_state.analyzed_wallets:
                st.markdown("### 📋 歷史檢索")
                st.markdown('<div class="history-container">', unsafe_allow_html=True)
                
                for address in st.session_state.analyzed_wallets:
                    data = st.session_state.analyzed_wallets[address]
                    # 創建新的按鈕文字格式
                    button_text = (
                        f"{address[:3]}哥｜"
                        f"Win:{data['analysis']['勝率']:.1f}%、"
                        f"RR:{data['analysis']['盈虧比']:.2f}、"
                        f"Boom:{data['token_analysis']['five_x_rate']*100:.2f}%"
                    )
                    if st.button(
                        button_text,
                        key=f"history_{address}",
                        help=f"點擊查看完整分析結果"
                    ):
                        st.session_state.current_analysis = address
                        st.rerun()  # 強制頁面重新運行
                
                st.markdown('</div>', unsafe_allow_html=True)

    # 如果是從歷史記錄點擊的
    if st.session_state.current_analysis:
        address = st.session_state.current_analysis
        saved_data = st.session_state.analyzed_wallets[address]
        
        with middle_col:
            st.markdown("### 錢包基礎分析")
            st.code(address, language=None)
            
            # 使用columns創建4x2網格布局
            metrics = [
                {"label": "總交易次數", "value": saved_data['analysis']['總交易次數']},
                {"label": "勝率", "value": f"{saved_data['analysis']['勝率']:.1f}%", 
                 "is_positive": saved_data['analysis']['勝率'] > 50},
                {"label": "平均獲利", "value": f"{saved_data['analysis']['平均獲利']:.1f}%", 
                 "is_positive": True},
                {"label": "平均虧損", "value": f"{saved_data['analysis']['平均虧損']:.1f}%", 
                 "is_positive": False},
                {"label": "盈虧比", "value": f"{saved_data['analysis']['盈虧比']:.2f}", 
                 "is_positive": saved_data['analysis']['盈虧比'] > 1},
                {"label": "5倍爆擊率", 
                 "value": f"{saved_data['token_analysis']['five_x_rate']*100:.2f}%"},
                {"label": "Rug盤比例", 
                 "value": f"{saved_data['token_analysis']['rug_ratio']*100:.2f}%", 
                 "is_positive": False},
                {"label": "Bot機率", 
                 "value": f"{saved_data['token_analysis']['quick_trade_ratio']:.2f}%"}
            ]
            
            # 創建4x2網格
            cols = st.columns(4)
            for i, metric in enumerate(metrics):
                with cols[i % 4]:
                    if "is_positive" in metric:
                        color = "#10B981" if metric["is_positive"] else "#EF4444"
                    else:
                        color = "#1F2937"
                    
                    st.markdown(
                        f"""
                        <div style="padding: 1rem; background-color: white; border-radius: 0.5rem; border: 1px solid #E5E7EB; margin-bottom: 1rem;">
                            <div style="color: #6B7280; font-size: 0.875rem;">{metric['label']}</div>
                            <div style="font-size: 1.25rem; font-weight: 600; color: {color};">{metric['value']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # 區間分析標籤頁
            fixed_tab, dynamic_tab = st.tabs(["固定市值區間分析", "動態市值區間分析"])
            
            with fixed_tab:
                if saved_data['advanced_results']['fixed_ranges']:
                    # 定義固定的八個區間
                    fixed_ranges = [
                        '$0K-$8.888K',
                        '$0K-$10K',
                        '$5K-$10K',
                        '$5K-$15K',
                        '$15K-$30K',
                        '$30K-$50K',
                        '$50K-$100K',
                        '>$100K'
                    ]
                    
                    # 創建DataFrame
                    df = pd.DataFrame([
                        {
                            '市值區間': name,
                            '交易次數': data['交易次數'],
                            '勝率': data['勝率'],
                            '平均獲利': data['平均獲利'],
                            '平均虧損': data['平均虧損'],
                            '5倍爆擊率': data['5倍爆擊率'],
                            '評分': data['綜合得分']
                        }
                        for name, data in saved_data['advanced_results']['fixed_ranges'].items()
                        if name in fixed_ranges
                    ])
                    
                    # 確保按照指定順序排序
                    df['排序'] = df['市值區間'].map({range_: i for i, range_ in enumerate(fixed_ranges)})
                    df = df.sort_values('排序').drop('排序', axis=1)
                    
                    # 創建樣式函數
                    def style_number(val, column):
                        if column in ['平均獲利', '平均虧損']:
                            color = '#10B981' if val > 0 else '#EF4444'
                            return f'color: {color}'
                        return ''
                    
                    # 應用樣式
                    styled_df = df.style.apply(lambda x: [style_number(v, x.name) for v in x], axis=0)
                    
                    # 顯示 DataFrame
                    st.dataframe(
                        styled_df,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "交易次數": st.column_config.NumberColumn(
                                "交易次數",
                                format="%d"
                            ),
                            "勝率": st.column_config.NumberColumn(
                                "勝率",
                                format="%.1f%%"
                            ),
                            "平均獲利": st.column_config.NumberColumn(
                                "平均獲利",
                                format="%.1f%%"
                            ),
                            "平均虧損": st.column_config.NumberColumn(
                                "平均虧損",
                                format="%.1f%%"
                            ),
                            "5倍爆擊率": st.column_config.NumberColumn(
                                "5倍爆擊率",
                                format="%.1f%%"
                            ),
                            "評分": st.column_config.NumberColumn(
                                "評分",
                                format="%.2f"
                            )
                        }
                    )

            with dynamic_tab:
                if saved_data['advanced_results']['dynamic_range']['range']:
                    best_range = saved_data['advanced_results']['dynamic_range']['range']
                    metrics = saved_data['advanced_results']['dynamic_range']['metrics']
                    
                    # 將兩個數字都以相同的方式格式化
                    lower_cap = f"${int(best_range[0]):,}"
                    upper_cap = f"${int(best_range[1]):,}"
                    range_str = f"最佳交易市值區間: {lower_cap} - {upper_cap}"
                    
                    st.markdown(
                        f"""
                        <div style='background-color: rgb(240, 248, 255); padding: 1rem; border-radius: 0.5rem;'>
                            <span style='font-size: 1rem;'>{range_str}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    dynamic_metrics = [
                        {"label": "交易次數", "value": metrics['交易次數']},
                        {"label": "勝率", "value": f"{metrics['勝率']:.1f}%", "is_positive": metrics['勝率'] > 50},
                        {"label": "平均獲利", "value": f"{metrics['平均獲利']:.1f}%", "is_positive": True},
                        {"label": "平均虧損", "value": f"{metrics['平均虧損']:.1f}%", "is_positive": False},
                        {"label": "盈虧比", "value": f"{metrics['盈虧比']:.2f}", "is_positive": metrics['盈虧比'] > 1},
                        {"label": "綜合得分", "value": f"{metrics['綜合得分']:.1f}", "is_positive": True}
                    ]
                    
                    dynamic_cols = st.columns(3)
                    for i, metric in enumerate(dynamic_metrics):
                        with dynamic_cols[i % 3]:
                            if "is_positive" in metric:
                                color = "#10B981" if metric["is_positive"] else "#EF4444"
                            else:
                                color = "#1F2937"
                            
                            st.markdown(
                                f"""
                                <div style="padding: 1rem; background-color: white; border-radius: 0.5rem; border: 1px solid #E5E7EB; margin-bottom: 1rem;">
                                    <div style="color: #6B7280; font-size: 0.875rem;">{metric['label']}</div>
                                    <div style="font-size: 1.25rem; font-weight: 600; color: {color};">{metric['value']}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

        with right_col:
            # 交易記錄標籤頁
            record_tab1, record_tab2 = st.tabs(["30日交易紀錄", "快速交易紀錄"])
            
            with record_tab1:
                records = []
                for tx in saved_data['transactions']:
                    token_address = tx['token'].get('address') if 'token' in tx else None
                    market_cap = (
                        get_market_cap_for_token(token_address, saved_data['token_analysis'])
                        if token_address else None
                    )
                    
                    records.append({
                        '時間': datetime.strptime(tx['時間戳'], '%Y-%m-%d %H:%M:%S'),
                        '代幣名稱': tx['代幣名稱'],
                        '首購市值': float(market_cap) if market_cap is not None else None,
                        '收益率': tx['收益率'] * 100
                    })

                records_df = pd.DataFrame(records)
                records_df = records_df.sort_values('時間', ascending=False)

                # 定義樣式函數
                def style_number(val, column):
                    if column == '收益率':
                        color = '#10B981' if val > 0 else '#EF4444'
                        return f'color: {color}'
                    return ''

                styled_records_df = records_df.style.apply(lambda x: [style_number(v, x.name) for v in x], axis=0)

                st.dataframe(
                    styled_records_df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "時間": st.column_config.DatetimeColumn(
                            "時間",
                            format="YYYY-MM-DD HH:mm:ss"
                        ),
                        "代幣名稱": st.column_config.TextColumn(
                            "代幣名稱"
                        ),
                        "首購市值": st.column_config.NumberColumn(
                            "首購市值",
                            help="Initial Market Cap",
                            format="$%.0f"
                        ),
                        "收益率": st.column_config.NumberColumn(
                            "收益率",
                            format="%.1f%%"
                        )
                    }
                )
            
            with record_tab2:
                if saved_data['token_analysis'].get('quick_trade_details'):
                    quick_trades = []
                    for trade in saved_data['token_analysis']['quick_trade_details']:
                        quick_trades.append({
                            '代幣名稱': trade['token_symbol'],
                            '首購市值': float(trade['buy_market_cap']) if trade['buy_market_cap'] is not None else None,
                            '收益率': trade['profit_rate'] * 100 if trade['profit_rate'] is not None else None,
                            '交易間隔(秒)': trade['interval']
                        })
                    
                    quick_trades_df = pd.DataFrame(quick_trades)
                    quick_trades_df = quick_trades_df.sort_values('首購市值')
                    
                    styled_quick_trades_df = quick_trades_df.style.apply(
                        lambda x: [style_number(v, x.name) for v in x], 
                        axis=0
                    )
                    
                    st.dataframe(
                        styled_quick_trades_df,
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "代幣名稱": st.column_config.TextColumn(
                                "代幣名稱"
                            ),
                            "首購市值": st.column_config.NumberColumn(
                                "首購市值",
                                help="Initial Market Cap",
                                format="$%.0f"
                            ),
                            "交易間隔(秒)": st.column_config.NumberColumn(
                                "交易間隔(秒)",
                                format="%d"
                            ),
                            "收益率": st.column_config.NumberColumn(
                                "收益率",
                                format="%.1f%%"
                            )
                        }
                    )
                else:
                    st.info("沒有快速交易記錄")

# 如果按下分析按鈕
    if analyze_button and wallet_address:
        st.write("開始初始化分析流程...")
        addresses = wallet_address.strip().split('\n')
        addresses = [addr.strip() for addr in addresses if addr.strip()]
        
        if not addresses:
            st.error("請輸入至少一個有效的錢包地址")
            return
    
        try:
            analyzer = WalletAnalyzer()
            st.write("初始化成功")
        except Exception as e:
            st.error(f"初始化分析器失敗: {str(e)}")
            st.info("正在嘗試使用備用方案...")
            time.sleep(5)
            analyzer = WalletAnalyzer()  # 再次嘗試初始化
    
        last_address = None  # 記錄最後一個成功分析的地址
        
        for address in addresses:
            st.write(f"開始分析錢包: {address}")
            try:
                st.write("開始發送請求...")
                transactions = analyzer.fetch_transactions(address)
                
                if isinstance(transactions, list):
                    st.write(f"成功獲取交易數據，交易數量: {len(transactions)}")
                else:
                    st.write(f"請求響應格式異常: {type(transactions)}")
                    continue
                
                if not transactions:
                    st.warning(f"無法獲取錢包 {address} 的交易記錄")
                    continue
    
                st.write("開始進行基礎分析...")
                analysis = analyzer.analyze_transactions(transactions)
                if analysis:
                    st.write("完成基礎分析")
                else:
                    st.error("基礎分析失敗")
                    continue
                
                st.write("開始進行代幣分析...")
                try:
                    token_analysis = analyzer.analyze_tokens_by_profit(address, transactions)
                    st.write("完成代幣分析")
                except Exception as e:
                    st.error(f"代幣分析過程中發生錯誤: {str(e)}")
                    continue
                
                st.write("開始進行進階分析...")
                try:
                    advanced_results = analyzer.advanced_analysis(address, transactions, token_analysis)
                    st.write("完成進階分析")
                except Exception as e:
                    st.error(f"進階分析過程中發生錯誤: {str(e)}")
                    continue
                
                # 保存分析結果到 session state
                st.session_state.analyzed_wallets[address] = {
                    'analysis': analysis,
                    'token_analysis': token_analysis,
                    'advanced_results': advanced_results,
                    'transactions': transactions
                }
                last_address = address
                st.write(f"完成錢包 {address} 的分析")
                
            except Exception as e:
                st.error(f"分析錢包時發生錯誤: {str(e)}")
                import traceback
                st.error(f"詳細錯誤追蹤:\n{traceback.format_exc()}")
                continue
    
            # 顯示處理進度
            st.write("---")
    
        # 分析完成後，設置最後一個成功的地址為當前分析
        if last_address:
            st.session_state.current_analysis = last_address
            st.write("準備更新顯示結果...")
            time.sleep(1)  # 給一點時間讓用戶看到進度
            st.rerun()  # 強制頁面重新運行
        else:
            st.error("所有錢包分析均失敗，請檢查輸入地址或稍後重試")

if __name__ == "__main__":
    main()
