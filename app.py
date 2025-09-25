import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import chardet

# Настройка страницы для мобильных устройств
st.set_page_config(
    page_title="ФинКалькулятор",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Информация в боковой панели
with st.sidebar:
    st.title("👨‍💻 О разработчике")
    st.write("**Сакен Тойбеков**")
    st.write("📚 [Мои курсы](https://coursesapp-e9669.web.app)")
    st.write("🤖 [Телеграм бот](https://t.me/saken_assistant_bot)")
    st.markdown("---")

# Главный заголовок с дополнительной информацией
st.title("💰 Финансовый Калькулятор")
st.markdown("*Профессиональный инструмент для финансовых расчетов*")

# Создаем вкладки для разделения функционала
tab1, tab2 = st.tabs(["🧮 Калькулятор кредитов", "📈 Инвестиционный анализ"])

with tab1:
    st.header("Расчет графика погашения кредита")

    # Ввод данных пользователем
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input(
            "Сумма кредита (₸)", min_value=0.0, value=1000000.0, step=10000.0
        )
        interest_rate = st.number_input(
            "Процентная ставка (% годовых)", min_value=0.0, value=10.0, step=0.1
        )
    with col2:
        loan_term = st.number_input("Срок кредита (лет)", min_value=1, value=5, step=1)
        payment_type = st.selectbox(
            "Тип платежа", ["Аннуитетный", "Дифференцированный"]
        )

    # Расчет ежемесячной ставки и количества платежей
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term * 12

    def calculate_annuity(principal, rate, periods):
        """Рассчитывает аннуитетный платеж"""
        if rate == 0:
            return principal / periods
        annuity_payment = (
            principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
        )
        return annuity_payment

    def generate_schedule(principal, rate, periods, p_type):
        """Генерирует график погашения"""
        schedule = []
        remaining_balance = principal

        if p_type == "Аннуитетный":
            payment = calculate_annuity(principal, rate, periods)
            for i in range(1, periods + 1):
                interest_payment = remaining_balance * rate
                principal_payment = payment - interest_payment
                remaining_balance -= principal_payment
                # Корректировка последнего платежа для избежания погрешности
                if i == periods:
                    principal_payment += remaining_balance
                    payment += remaining_balance
                    remaining_balance = 0
                schedule.append(
                    {
                        "Период": i,
                        "Платеж": payment,
                        "Проценты": interest_payment,
                        "Основной долг": principal_payment,
                        "Остаток долга": max(remaining_balance, 0),
                    }
                )
        else:  # Дифференцированный
            principal_payment = principal / periods
            for i in range(1, periods + 1):
                interest_payment = remaining_balance * rate
                payment = principal_payment + interest_payment
                remaining_balance -= principal_payment
                schedule.append(
                    {
                        "Период": i,
                        "Платеж": payment,
                        "Проценты": interest_payment,
                        "Основной долг": principal_payment,
                        "Остаток долга": max(remaining_balance, 0),
                    }
                )

        return pd.DataFrame(schedule)

    if st.button("Рассчитать график погашения", type="primary", key="loan_calc"):
        schedule_df = generate_schedule(
            loan_amount, monthly_rate, num_payments, payment_type
        )

        # Отображение сводной информации
        total_payment = schedule_df["Платеж"].sum()
        total_interest = schedule_df["Проценты"].sum()

        st.metric("Общая сумма выплат", f"{total_payment:,.2f} ₸")
        st.metric("Сумма выплаченных процентов", f"{total_interest:,.2f} ₸")

        # Отображение графика погашения в виде таблицы
        st.subheader("График погашения")
        # Форматирование чисел в таблице для удобочитаемости
        display_df = schedule_df.copy()
        for col in ["Платеж", "Проценты", "Основной долг", "Остаток долга"]:
            display_df[col] = display_df[col].map("{:,.2f} ₸".format)
        st.dataframe(display_df, use_container_width=True)

        # Построение графика
        st.subheader("Структура платежей")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=schedule_df["Период"],
                y=schedule_df["Основной долг"],
                mode="lines",
                stackgroup="one",
                name="Основной долг",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=schedule_df["Период"],
                y=schedule_df["Проценты"],
                mode="lines",
                stackgroup="one",
                name="Проценты",
            )
        )
        fig.update_layout(
            title="Динамика платежа по периодам",
            xaxis_title="Номер платежа",
            yaxis_title="Сумма, ₸",
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Анализ инвестиционного проекта")

    # Ввод ставки дисконтирования
    discount_rate = (
        st.number_input(
            "Ставка дисконтирования (% годовых)",
            min_value=0.0,
            value=10.0,
            step=0.1,
            key="disc_rate",
        )
        / 100
    )

    # Ввод денежных потоков
    st.subheader("Денежные потоки")
    st.caption(
        "Введите начальные инвестиции (со знаком '-') и последующие денежные потоки."
    )

    initial_investment = st.number_input(
        "Начальные инвестиции (₸)", value=-1000000.0, step=10000.0
    )

    # Динамическое добавление потоков
    num_cash_flows = st.slider(
        "Количество периодов анализа (лет)", min_value=1, max_value=20, value=5
    )

    cash_flows = [initial_investment]
    for i in range(1, num_cash_flows + 1):
        cf = st.number_input(
            f"Денежный поток за год {i} (₸)",
            value=300000.0,
            step=10000.0,
            key=f"cf_{i}",
        )
        cash_flows.append(cf)

    # Кнопка расчета
    if st.button("Проанализировать проект", type="primary", key="inv_analysis"):
        cash_flows_array = np.array(cash_flows)

        # Расчет показателей
        npv = npf.npv(discount_rate, cash_flows_array)
        try:
            irr = npf.irr(cash_flows_array) * 100  # в процентах
        except:
            irr = "Не может быть рассчитан"

        # Расчет срока окупаемости (PP)
        cumulative_cf = np.cumsum(cash_flows_array)
        pp_years = None
        for i, cum_cf in enumerate(cumulative_cf):
            if cum_cf >= 0:
                pp_years = (
                    i - 1 + (abs(cumulative_cf[i - 1]) / cash_flows_array[i])
                    if i > 0
                    else i
                )
                break

        # Расчет дисконтированного срока окупаемости (DPP)
        discounted_cf = [
            cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows_array)
        ]
        cumulative_dcf = np.cumsum(discounted_cf)
        dpp_years = None
        for i, cum_dcf in enumerate(cumulative_dcf):
            if cum_dcf >= 0:
                dpp_years = (
                    i - 1 + (abs(cumulative_dcf[i - 1]) / discounted_cf[i])
                    if i > 0
                    else i
                )
                break

        # Отображение результатов
        col1, col2 = st.columns(2)
        with col1:
            st.metric("NPV (Чистая приведенная стоимость)", f"{npv:,.2f} ₸")
            if isinstance(irr, str):
                st.metric("IRR (Внутренняя норма доходности)", irr)
            else:
                st.metric("IRR (Внутренняя норма доходности)", f"{irr:.2f} %")
        with col2:
            st.metric(
                "Срок окупаемости (PP)",
                f"{pp_years:.2f} лет" if pp_years else "Не окупится",
            )
            st.metric(
                "Диск. срок окупаемости (DPP)",
                f"{dpp_years:.2f} лет" if dpp_years else "Не окупится",
            )

        # Визуализация денежных потоков
        st.subheader("Диаграмма денежных потоков")
        years = list(range(len(cash_flows_array)))
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=years,
                y=cash_flows_array,
                name="Денежный поток",
                marker_color=["red" if x < 0 else "green" for x in cash_flows_array],
            )
        )
        fig.add_trace(
            go.Scatter(
                x=years,
                y=cumulative_cf,
                mode="lines+markers",
                name="Накопленный поток",
                line=dict(color="blue", width=3),
            )
        )
        fig.update_layout(
            title="Денежные потоки проекта",
            xaxis_title="Период (годы)",
            yaxis_title="Сумма, ₸",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Вывод об эффективности
        st.subheader("Вывод об эффективности")
        if npv > 0:
            st.success(
                f"Проект эффективен. NPV > 0, что означает создание дополнительной стоимости."
            )
        else:
            st.error(
                f"Проект неэффективен при заданной ставке дисконтирования. NPV <= 0."
            )

        if not isinstance(irr, str) and irr > discount_rate * 100:
            st.success(
                f"IRR проекта ({irr:.2f}%) превышает ставку дисконтирования ({discount_rate*100:.2f}%), что подтверждает эффективность."
            )
        elif not isinstance(irr, str):
            st.warning(
                f"IRR проекта ({irr:.2f}%) ниже ставки дисконтирования ({discount_rate*100:.2f}%)."
            )
# Футер
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: gray;'>
    <p>Приложение размещено на Streamlit Cloud • Версия 1.0</p>
</div>
""",
    unsafe_allow_html=True,
)

# Запуск приложения: в терминале выполнить команду `streamlit run app.py`
