import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px
import plotly.graph_objects as go
import chardet
from io import StringIO
from datetime import datetime, timedelta

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
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🧮 Кредиты",
        "📈 Инвест-анализ",
        "🏦 ЭПС калькулятор",
        "💳 Вклады и депозиты",
    ]
)

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

with tab3:
    st.header("🏦 Расчет эффективной процентной ставки (ЭПС)")
    st.info(
        "ЭПС показывает реальную стоимость кредита с учетом всех комиссий и дополнительных платежей"
    )

    with st.expander("📊 Что включается в расчет ЭПС"):
        st.markdown(
            """
        **Учитываемые платежи:**
        - Основной долг и проценты
        - Единовременные комиссии (за рассмотрение, выдачу)
        - Ежемесячные/ежегодные комиссии
        - Страховки
        - Прочие обязательные платежи
        """
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Основные параметры кредита")
        eps_loan_amount = st.number_input(
            "Сумма кредита (₸)",
            min_value=0.0,
            value=500000.0,
            step=10000.0,
            key="eps_loan",
        )
        eps_nominal_rate = st.number_input(
            "Номинальная ставка (% годовых)",
            min_value=0.0,
            value=15.0,
            step=0.1,
            key="eps_nominal",
        )
        eps_term = st.number_input(
            "Срок кредита (месяцев)", min_value=1, value=36, step=1, key="eps_term"
        )
        eps_payment_type = st.selectbox(
            "Тип платежа", ["Аннуитетный", "Дифференцированный"], key="eps_payment"
        )

    with col2:
        st.subheader("Дополнительные комиссии и платежи")

        # Единовременные комиссии
        st.write("**Единовременные комиссии:**")
        eps_issue_fee = st.number_input(
            "Комиссия за выдачу (%)",
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="eps_issue",
        )
        eps_issue_fee_fixed = st.number_input(
            "Фиксированная комиссия (₸)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key="eps_fixed",
        )

        # Постоянные комиссии
        st.write("**Постоянные комиссии:**")
        eps_monthly_fee = st.number_input(
            "Ежемесячное обслуживание (₸)",
            min_value=0.0,
            value=100.0,
            step=50.0,
            key="eps_monthly",
        )
        eps_annual_fee = st.number_input(
            "Ежегодное обслуживание (₸)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key="eps_annual",
        )

        # Страховка
        st.write("**Страхование:**")
        eps_insurance = st.number_input(
            "Страховка (% от суммы)",
            min_value=0.0,
            value=0.5,
            step=0.1,
            key="eps_insurance",
        )

    # Расчет ЭПС
    if st.button("📈 Рассчитать ЭПС", type="primary", key="calc_eps"):

        # Рассчитываем денежные потоки для ЭПС
        cash_flows = []

        # Месячная процентная ставка
        monthly_rate = eps_nominal_rate / 100 / 12

        # Начальные расходы (минус означает отток денег)
        initial_costs = 0

        # Комиссия за выдачу
        if eps_issue_fee > 0:
            initial_costs += eps_loan_amount * eps_issue_fee / 100

        # Фиксированная комиссия
        initial_costs += eps_issue_fee_fixed

        # Страховка
        if eps_insurance > 0:
            initial_costs += eps_loan_amount * eps_insurance / 100

        # Первый поток: получение кредита минус начальные расходы
        cash_flows.append(eps_loan_amount - initial_costs)

        # Расчет ежемесячных платежей
        if eps_payment_type == "Аннуитетный":
            # Аннуитетный платеж
            if monthly_rate == 0:
                monthly_payment = eps_loan_amount / eps_term
            else:
                monthly_payment = (
                    eps_loan_amount
                    * (monthly_rate * (1 + monthly_rate) ** eps_term)
                    / ((1 + monthly_rate) ** eps_term - 1)
                )
        else:
            # Дифференцированный платеж
            principal_payment = eps_loan_amount / eps_term

        # Генерация ежемесячных потоков
        remaining_balance = eps_loan_amount

        for month in range(1, eps_term + 1):
            monthly_cash_outflow = 0

            if eps_payment_type == "Аннуитетный":
                # Для аннуитета платеж постоянный
                interest_payment = remaining_balance * monthly_rate
                principal_payment = monthly_payment - interest_payment
                monthly_cash_outflow = monthly_payment
                remaining_balance -= principal_payment
            else:
                # Для дифференцированного
                interest_payment = remaining_balance * monthly_rate
                monthly_cash_outflow = principal_payment + interest_payment
                remaining_balance -= principal_payment

            # Добавляем ежемесячное обслуживание
            monthly_cash_outflow += eps_monthly_fee

            # Добавляем ежегодное обслуживание (если месяц кратен 12)
            if month % 12 == 0 and eps_annual_fee > 0:
                monthly_cash_outflow += eps_annual_fee

            cash_flows.append(-monthly_cash_outflow)

        # Расчет ЭПС (IRR денежных потоков)
        try:
            eps_result = npf.irr(cash_flows) * 12 * 100  # Переводим в годовую ставку
            eps_result = max(eps_result, 0)  # ЭПС не может быть отрицательной
        except:
            eps_result = eps_nominal_rate  # Если не получается рассчитать, используем номинальную

        # Визуализация результатов
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Номинальная ставка", f"{eps_nominal_rate:.2f}%")

        with col2:
            st.metric(
                "Эффективная ставка (ЭПС)",
                f"{eps_result:.2f}%",
                delta=f"{eps_result - eps_nominal_rate:.2f}%",
            )

        with col3:
            overpayment_ratio = (eps_result - eps_nominal_rate) / eps_nominal_rate * 100
            st.metric(
                "Разница",
                f"{eps_result - eps_nominal_rate:.2f}%",
                delta=f"{overpayment_ratio:.1f}% от номинальной",
            )

        # Детализация денежных потоков
        st.subheader("📋 Детализация платежей")

        # Создаем таблицу с первыми 12 месяцами
        schedule_data = []
        remaining = eps_loan_amount

        for month in range(1, min(13, eps_term + 1)):
            if eps_payment_type == "Аннуитетный":
                interest = remaining * monthly_rate
                principal = monthly_payment - interest
                total_payment = monthly_payment
                remaining -= principal
            else:
                interest = remaining * monthly_rate
                principal = eps_loan_amount / eps_term
                total_payment = principal + interest
                remaining -= principal

            schedule_data.append(
                {
                    "Месяц": month,
                    "Основной долг": principal,
                    "Проценты": interest,
                    "Комиссии": eps_monthly_fee
                    + (eps_annual_fee if month % 12 == 0 else 0),
                    "Всего платеж": total_payment
                    + eps_monthly_fee
                    + (eps_annual_fee if month % 12 == 0 else 0),
                }
            )

        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(
            schedule_df.style.format(
                {
                    "Основной долг": "{:,.2f} ₸",
                    "Проценты": "{:,.2f} ₸",
                    "Комиссии": "{:,.2f} ₸",
                    "Всего платеж": "{:,.2f} ₸",
                }
            )
        )

        # График структуры переплаты
        st.subheader("📊 Структура переплаты по кредиту")

        total_interest = sum([x["Проценты"] for x in schedule_data]) * (
            eps_term / min(12, eps_term)
        )
        total_fees = (
            initial_costs
            + (eps_monthly_fee * eps_term)
            + (eps_annual_fee * (eps_term // 12))
        )

        fig_eps = px.pie(
            values=[total_interest, total_fees],
            names=["Проценты", "Комиссии и страховки"],
            title="Распределение переплаты по кредиту",
        )
        st.plotly_chart(fig_eps, use_container_width=True)

        # Выводы и рекомендации
        st.subheader("💡 Выводы")

        if eps_result > eps_nominal_rate + 2:
            st.warning(
                f"**Внимание!** ЭПС значительно выше номинальной ставки. Реальная стоимость кредита на {eps_result - eps_nominal_rate:.2f}% выше заявленной."
            )
            st.write(
                "**Рекомендации:** Рассмотрите другие предложения или попробуйте negotiate условия."
            )
        elif eps_result > eps_nominal_rate + 0.5:
            st.info(
                f"ЭПС умеренно превышает номинальную ставку. Разница составляет {eps_result - eps_nominal_rate:.2f}%."
            )
        else:
            st.success(
                f"Отличные условия! ЭПС практически соответствует номинальной ставке."
            )

# ============================================================================
# 4. НОВАЯ ФУНКЦИЯ: КАЛЬКУЛЯТОР ВКЛАДОВ С КАПИТАЛИЗАЦИЕЙ
# ============================================================================

with tab4:
    st.header("💳 Калькулятор вкладов и депозитов")
    st.success("Рассчитайте доходность вклада с учетом капитализации процентов")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Параметры вклада")
        deposit_amount = st.number_input(
            "Сумма вклада (₸)",
            min_value=1000.0,
            value=100000.0,
            step=10000.0,
            key="deposit_amount",
        )
        deposit_rate = st.number_input(
            "Процентная ставка (% годовых)",
            min_value=0.1,
            value=8.0,
            step=0.1,
            key="deposit_rate",
        )
        deposit_term = st.number_input(
            "Срок вклада (месяцев)", min_value=1, value=12, step=1, key="deposit_term"
        )

        st.subheader("Тип капитализации")
        capitalization_type = st.selectbox(
            "Периодичность капитализации",
            ["Ежемесячная", "Ежеквартальная", "Ежегодная", "В конце срока"],
            key="cap_type",
        )

    with col2:
        st.subheader("Дополнительные условия")

        # Пополнение вклада
        st.write("**Пополнение вклада:**")
        monthly_topup = st.number_input(
            "Ежемесячное пополнение (₸)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            key="monthly_topup",
        )

        # Налоги
        st.write("**Налогообложение:**")
        tax_free = st.checkbox("Не облагается налогом", value=True, key="tax_free")
        if not tax_free:
            tax_rate = st.number_input(
                "Ставка налога (%)", min_value=0.0, value=13.0, step=0.1, key="tax_rate"
            )

        # Инфляция
        st.write("**Учет инфляции:**")
        include_inflation = st.checkbox(
            "Учитывать инфляцию", value=False, key="include_inflation"
        )
        if include_inflation:
            inflation_rate = st.number_input(
                "Прогноз инфляции (% годовых)",
                min_value=0.0,
                value=5.0,
                step=0.1,
                key="inflation_rate",
            )

    # Расчет вклада
    if st.button("💸 Рассчитать доходность", type="primary", key="calc_deposit"):

        # Определяем периодичность капитализации
        if capitalization_type == "Ежемесячная":
            periods_per_year = 12
        elif capitalization_type == "Ежеквартальная":
            periods_per_year = 4
        elif capitalization_type == "Ежегодная":
            periods_per_year = 1
        else:  # В конце срока
            periods_per_year = 1

        # Капитализация в конце срока только для соответствующего типа
        capitalization_at_end = capitalization_type == "В конце срока"

        # Периодическая ставка
        periodic_rate = deposit_rate / 100 / periods_per_year

        # Количество периодов
        total_periods = deposit_term / (12 / periods_per_year)

        # Расчет без пополнения
        if monthly_topup == 0:
            if capitalization_at_end:
                # Простые проценты
                final_amount = deposit_amount * (
                    1 + deposit_rate / 100 * deposit_term / 12
                )
                total_interest = final_amount - deposit_amount
            else:
                # Сложные проценты с капитализацией
                final_amount = deposit_amount * (1 + periodic_rate) ** total_periods
                total_interest = final_amount - deposit_amount
        else:
            # Расчет с пополнением (аннуитет)
            final_amount = deposit_amount
            monthly_growth = 1 + deposit_rate / 100 / 12

            for month in range(1, deposit_term + 1):
                final_amount = final_amount * monthly_growth + monthly_topup

            total_interest = (
                final_amount - deposit_amount - (monthly_topup * deposit_term)
            )

        # Расчет налогов
        tax_amount = 0
        if not tax_free:
            # Предполагаем, что налог на весь доход
            tax_amount = total_interest * tax_rate / 100
            net_interest = total_interest - tax_amount
            net_final_amount = final_amount - tax_amount
        else:
            net_interest = total_interest
            net_final_amount = final_amount

        # Учет инфляции
        if include_inflation:
            inflation_factor = (1 + inflation_rate / 100) ** (deposit_term / 12)
            real_final_amount = net_final_amount / inflation_factor
            real_interest = real_final_amount - deposit_amount
        else:
            real_final_amount = net_final_amount
            real_interest = net_interest

        # Отображение результатов
        st.success("📊 **Результаты расчета вклада**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Начальная сумма", f"{deposit_amount:,.0f} ₸")
            st.metric("Сумма пополнений", f"{monthly_topup * deposit_term:,.0f} ₸")

        with col2:
            st.metric("Итоговая сумма", f"{final_amount:,.0f} ₸")
            st.metric("Начисленные проценты", f"{total_interest:,.0f} ₸")

        with col3:
            st.metric("Чистый доход", f"{net_interest:,.0f} ₸")
            if tax_amount > 0:
                st.metric("Налог к уплате", f"{tax_amount:,.0f} ₸")

        # Годовая доходность
        annual_yield = (net_interest / deposit_amount) * (12 / deposit_term) * 100
        st.metric("💫 Эффективная годовая доходность", f"{annual_yield:.2f}%")

        # График роста вклада
        st.subheader("📈 Динамика роста вклада")

        # Строим график по месяцам
        months = list(range(0, deposit_term + 1))
        amounts = [deposit_amount]
        current_amount = deposit_amount
        monthly_rate = deposit_rate / 100 / 12

        for month in range(1, deposit_term + 1):
            if capitalization_type == "Ежемесячная" or capitalization_at_end:
                current_amount = current_amount * (1 + monthly_rate) + monthly_topup
            else:
                # Для других типов капитализации - упрощенный расчет
                current_amount = (
                    current_amount + (deposit_amount * monthly_rate) + monthly_topup
                )
            amounts.append(current_amount)

        fig_deposit = px.line(
            x=months,
            y=amounts,
            title="Рост вклада по месяцам",
            labels={"x": "Месяц", "y": "Сумма, ₸"},
        )
        fig_deposit.update_traces(line=dict(color="green", width=3))
        st.plotly_chart(fig_deposit, use_container_width=True)

        # Сравнение с разными типами капитализации
        st.subheader("🔍 Сравнение типов капитализации")

        cap_types = ["Ежемесячная", "Ежеквартальная", "Ежегодная", "В конце срока"]
        results = []

        for cap_type in cap_types:
            if cap_type == "Ежемесячная":
                result = deposit_amount * (1 + deposit_rate / 100 / 12) ** deposit_term
            elif cap_type == "Ежеквартальная":
                result = deposit_amount * (1 + deposit_rate / 100 / 4) ** (
                    deposit_term / 3
                )
            elif cap_type == "Ежегодная":
                result = deposit_amount * (1 + deposit_rate / 100) ** (
                    deposit_term / 12
                )
            else:  # В конце срока
                result = deposit_amount * (1 + deposit_rate / 100 * deposit_term / 12)

            results.append(result)

        comparison_df = pd.DataFrame(
            {
                "Тип капитализации": cap_types,
                "Итоговая сумма": results,
                "Доход": [x - deposit_amount for x in results],
            }
        )

        st.dataframe(
            comparison_df.style.format(
                {"Итоговая сумма": "{:,.2f} ₸", "Доход": "{:,.2f} ₸"}
            )
        )

        # Рекомендации
        st.subheader("💡 Рекомендации")

        best_cap_type = cap_types[np.argmax(results)]
        best_income = max(results) - deposit_amount

        st.info(
            f"**Наибольший доход** обеспечивает **{best_cap_type}** капитализация: **{best_income:,.0f} ₸**"
        )

        if monthly_topup > 0:
            st.success(
                "**Пополнение вклада** значительно увеличивает итоговую сумму благодаря сложным процентам."
            )


# Футер
st.markdown("---")
st.markdown("### 📞 Контакты")
st.write("**Сакен Тойбеков**")
st.write("📚 [Курсы](https://coursesapp-e9669.web.app)")
st.write("🤖 [Телеграм бот](https://t.me/saken_assistant_bot)")
st.markdown("---")

# st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: gray;'>
    <p>Приложение размещено на Streamlit Cloud • Версия 2.0</p>
</div>
""",
    unsafe_allow_html=True,
)

# Запуск приложения: в терминале выполнить команду `streamlit run app.py`
