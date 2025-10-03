import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================================
# МНОГОЯЗЫЧНЫЕ ПЕРЕВОДЫ
# ============================================================================

TRANSLATIONS = {
    "kz": {
        "title": "💰 Қаржы Калькуляторы",
        "subtitle": "Қаржылық есептеулерге арналған кәсіби құрал",
        "author": "👨‍💻 Әзірлеуші",
        "author_name": "**Сәкен Тойбеков**",
        "courses": "📚 [Менің курстарым](https://coursesapp-e9669.web.app)",
        "bot": "🤖 [Телеграм бот](https://t.me/saken_assistant_bot)",
        "contacts": "📞 +7(701)7319631",
        # Вкладки
        "loans": "🧮 Несиелер",
        "investment": "📈 Инвестициялық талдау",
        "eps": "🏦 ТЖМ калькуляторы",
        "deposits": "💳 Депозиттер",
        # Калькулятор кредитов
        "calculate_schedule": "Несиені өтеу кестесін есептеу",
        "loan_amount": "Несие сомасы (₸)",
        "interest_rate": "Пайыздық мөлшерлеме (% жылдық)",
        "loan_term": "Несие мерзімі (жыл)",
        "payment_type": "Төлем түрі",
        "annuity": "Аннуитеттік",
        "differentiated": "Дифференциалдық",
        "calculate_loan": "Несиені есептеу",
        "total_payment": "Жалпы төлем сомасы",
        "total_interest": "Жалпы пайыздар",
        "payment_schedule": "Қарызды қайтару кестесі",
        "payment_structure": "Төлем құрылымы",
        "payment_dynamics": "Кезеңдер бойынша төлем динамикасы",
        "period": "Кезең",
        "payment": "Төлем",
        "principal": "Негізгі қарыз",
        "interest": "Пайыздар",
        "balance": "Қалдық",
        # Инвестиционный анализ
        "discount_rate": "Дисконттау мөлшерлемесі (% жылдық)",
        "initial_investment": "Бастапқы инвестиция (₸)",
        "cash_flows": "Ақша ағындары",
        "investment_caption": "Бастапқы инвестицияны (теріс белгісімен) және келесі ақша ағындарын енгізіңіз.",
        "analysis_periods": "Талдау кезеңдерінің саны (жыл)",
        "cash_flow_year": "Жылдағы ақша ағыны",
        "analyze_project": "Жобаны талдау",
        "npv": "NPV (Таза келтірілген құн)",
        "irr": "IRR (Ішкі табыстылық нормасы)",
        "payback_period": "Өтелу мерзімі (PP)",
        "discounted_payback": "Дисконтталған өтелу мерзімі (DPP)",
        "cash_flow_diagram": "Ақша ағындарының диаграммасы",
        "efficiency_conclusion": "Тиімділік туралы қорытынды",
        "project_efficient": "Жоба тиімді. NPV > 0, бұл қосымша құнның пайда болғанын білдіреді.",
        "project_inefficient": "Берілген дисконттау мөлшерлемесі бойынша жоба тиімді емес. NPV <= 0.",
        "irr_higher": "Жобаның IRR ({:.2f}%) дисконттау мөлшерлемесінен ({:.2f}%) жоғары, бұл тиімділікті растайды.",
        "irr_lower": "Жобаның IRR ({:.2f}%) дисконттау мөлшерлемесінен ({:.2f}%) төмен.",
        # ЭПС калькулятор
        "eps_title": "Тиімді жылдық мөлшерлеме (ТЖМ)",
        "eps_info": "ТЖМ несиенің, барлық комиссияларды ескере отырып анықталған, нақты құнын көрсетеді",
        "eps_details": "📊 ТЖМ есептеуге не кіреді",
        "eps_include": """
        **Есепке алынатын төлемдер:**
        - Негізгі қарыз және пайыздар
        - Біржолғы комиссиялар (қарастыру, беру үшін)
        - Айлық/жылдық комиссиялар
        - Сақтандыру
        - Басқа міндетті төлемдер
        """,
        "loan_parameters": "Несиенің негізгі параметрлері",
        "nominal_rate": "Номиналды мөлшерлеме (% жылдық)",
        "nominal_rate1": "Номиналды мөлшерлеме",
        "loan_term_months": "Несие мерзімі (ай)",
        "additional_fees": "Қосымша комиссиялар мен төлемдер",
        "one_time_fees": "**Біржолғы комиссиялар:**",
        "issue_fee": "Беру комиссиясы (%)",
        "fixed_fee": "Бекітілген комиссия (₸)",
        "recurring_fees": "**Тұрақты комиссиялар:**",
        "monthly_fee": "Айлық қызмет көрсету (₸)",
        "annual_fee": "Жылдық қызмет көрсету (₸)",
        "insurance_section": "**Сақтандыру:**",
        "insurance": "Сақтандыру (% сомадан)",
        "calculate_eps": "📈 ТЖМ есептеу",
        "nominal_rate_label": "Номиналды мөлшерлеме",
        "effective_rate": "Тиімді мөлшерлеме (ТЖМ)",
        "difference": "Айырмашылық",
        "from_nominal": "номиналды мөлшерлемеден",
        "payment_details": "📋 Төлем мәліметтері",
        "month": "Ай",
        "fees": "Комиссиялар",
        "total_payment_single": "Жалпы төлем",
        "overpayment_structure": "📊 Несие бойынша үстеме төлемнің құрылымы",
        "fees_insurance": "Комиссиялар және сақтандыру",
        "monthly_fees": "Айлық комиссиялар",
        "annual_fees": "Жылдық комиссиялар",
        "issue_fee_full": "Беру комиссиясы",
        "issue_fee_fixed": "Тұрақты комиссия",
        "total_overpayment": "**Несие бойынша жалпы үстеме төлем:** {:,.0f} ₸ (несие сомасынан {:.1f}%)",
        "of_loan_amount": "несие сомасынан",
        "overpayment_distribution": "Несие бойынша үстеме төлемнің үлестірілуі",
        "no_additional_fees": "Қосымша төлемдер жоқ",
        "eps_conclusions": "💡 Қорытындылар",
        "eps_warning": "**Назар аударыңыз!** ТЖМ номиналды мөлшерлемеден айтарлықтай жоғары. Несиенің нақты құны жарияланғаннан {:.2f}% жоғары.",
        "eps_recommendation": "**Ұсыныстар:** Басқа ұсыныстарды қарастырыңыз немесе шарттарды талқылауға тырысыңыз.",
        "eps_info_moderate": "ТЖМ номиналды мөлшерлемеден орташа деңгейде жоғары. Айырмашылығы ({:.2f}%) құрайды.",
        "eps_success": "Тамаша шарттар! ТЖМ номиналды мөлшерлемеге іс жүзінде сәйкес келеді.",
        # Калькулятор вкладов
        "deposit_title": "Депозиттер мен салымдар калькуляторы",
        "deposit_success": "Пайыздарды капитализациялаумен салымның табыстылығын есептеңіз",
        "deposit_parameters": "Салым параметрлері",
        "deposit_amount": "Салым сомасы (₸)",
        "deposit_rate": "Пайыздық мөлшерлеме (% жылдық)",
        "deposit_term": "Салым мерзімі (ай)",
        "capitalization_type": "Капитализация түрі",
        "capitalization_frequency": "Капитализация жиілігі",
        "monthly_cap": "Айлық",
        "quarterly_cap": "Ширек жылдық",
        "yearly_cap": "Жылдық",
        "end_term": "Мерзім соңында",
        "additional_conditions": "Қосымша шарттар",
        "deposit_topup": "**Салымды толықтыру:**",
        "monthly_topup": "Айлық толықтыру (₸)",
        "taxation": "**Салық салу:**",
        "tax_free": "Салық салынбайды",
        "tax_rate": "Салық мөлшерлемесі (%)",
        "inflation": "**Инфляцияны есепке алу:**",
        "include_inflation": "Инфляцияны есепке алу",
        "inflation_rate": "Инфляция болжамы (% жылдық)",
        "calculate_deposit": "💸 Табыстылықты есептеу",
        "deposit_results": "📊 **Салымды есептеу нәтижелері**",
        "initial_amount": "Бастапқы сома",
        "total_topup": "Толықтырулар сомасы",
        "final_amount": "Жинақталған сома",
        "accrued_interest": "Есептелген пайыздар",
        "net_income": "Таза табыс",
        "tax_payment": "Төленетін салық",
        "inflation_analysis": "📊 Инфляцияны есепке алу",
        "real_final_amount": "Нақты қорытынды сома",
        "real_income": "Нақты табыс",
        "real_annual_yield": "Нақты жылдық табыстылық",
        "nominal_yield": "Номиналды табыстылық",
        "positive_real_yield": "💰 **Оң нақты табыстылық!** Салымдар сатып алу қабілетін сақтайды.",
        "low_real_yield": "⚠️ **Төмен нақты табыстылық.** Салым инфляциядан ішінара қорғайды.",
        "negative_real_yield": "📉 **Теріс нақты табыстылық.** Салымның сатып алу қабілеті төмендейді.",
        "with_inflation": "инфляцияны ескере отырып",
        "without_inflation": "инфляцияны есепке алмай",
        "annual_yield": "💫 Тиімді жылдық табыстылық",
        "deposit_growth": "📈 Салымның өсу динамикасы",
        "deposit_growth_month": "Салымның айлар бойынша өсуі",
        "month_label": "Ай",
        "amount_label": "Сома, ₸",
        "capitalization_comparison": "🔍 Капитализация түрлерін салыстыру",
        "income": "Табыс",
        "deposit_recommendations": "💡 Ұсыныстар",
        "best_income_message": "**Ең жоғары табысты** **{}** капитализация қамтамасыз етеді: **{:.0f} ₸**",
        "topup_benefit": "**Салымды толықтыру** күрделі пайыздардың арқасында жинақталған соманы айтарлықтай арттырады.",
        # Общие
        "not_calculated": "Есептеу мүмкін емес",
        "not_paid_off": "Өтелмеді",
        "years": "жыл",
        "footer": "Қолданба Streamlit Cloud-та орналастырылған • Нұсқа 2.0",
    },
    "ru": {
        "title": "💰 Финансовый Калькулятор",
        "subtitle": "Профессиональный инструмент для финансовых расчетов",
        "author": "👨‍💻 О разработчике",
        "author_name": "**Сакен Тойбеков**",
        "courses": "📚 [Мои курсы](https://coursesapp-e9669.web.app)",
        "bot": "🤖 [Телеграм бот](https://t.me/saken_assistant_bot)",
        "contacts": "📞 +7(701)7319631",
        # Вкладки
        "loans": "🧮 Кредиты",
        "investment": "📈 Инвест-анализ",
        "eps": "🏦 ЭПС калькулятор",
        "deposits": "💳 Вклады и депозиты",
        # Остальные переводы аналогичны казахским, но на русском языке
        "calculate_schedule": "Расчет графика погашения кредита",
        "loan_amount": "Сумма кредита (₸)",
        "interest_rate": "Процентная ставка (% годовых)",
        "loan_term": "Срок кредита (лет)",
        "payment_type": "Тип платежа",
        "annuity": "Аннуитетный",
        "differentiated": "Дифференцированный",
        "calculate_loan": "Рассчитать кредит",
        "total_payment": "Общая сумма выплат",
        "total_interest": "Общая сумма процентов",
        "payment_schedule": "График погашения кредита",
        "payment_structure": "Структура платежей",
        "payment_dynamics": "Динамика платежа по периодам",
        "period": "Период",
        "payment": "Платеж",
        "principal": "Основной долг",
        "interest": "Проценты",
        "balance": "Остаток",
        # Инвестиционный анализ
        "discount_rate": "Ставка дисконтирования (% годовых)",
        "initial_investment": "Начальные инвестиции (₸)",
        "cash_flows": "Денежные потоки",
        "investment_caption": "Введите начальные инвестиции (со знаком '-') и последующие денежные потоки.",
        "analysis_periods": "Количество периодов анализа (лет)",
        "cash_flow_year": "Денежный поток за год",
        "analyze_project": "Проанализировать проект",
        "npv": "NPV (Чистая приведенная стоимость)",
        "irr": "IRR (Внутренняя норма доходности)",
        "payback_period": "Срок окупаемости (PP)",
        "discounted_payback": "Диск. срок окупаемости (DPP)",
        "cash_flow_diagram": "Диаграмма денежных потоков",
        "efficiency_conclusion": "Вывод об эффективности",
        "project_efficient": "Проект эффективен. NPV > 0, что означает создание дополнительной стоимости.",
        "project_inefficient": "Проект неэффективен при заданной ставке дисконтирования. NPV <= 0.",
        "irr_higher": "IRR проекта ({:.2f}%) превышает ставку дисконтирования ({:.2f}%), что подтверждает эффективность.",
        "irr_lower": "IRR проекта ({:.2f}%) ниже ставки дисконтирования ({:.2f}%).",
        # ЭПС калькулятор
        "eps_title": "Расчет эффективной процентной ставки (ЭПС)",
        "eps_info": "ЭПС показывает реальную стоимость кредита с учетом всех комиссий и дополнительных платежей",
        "eps_details": "📊 Что включается в расчет ЭПС",
        "eps_include": """
        **Учитываемые платежи:**
        - Основной долг и проценты
        - Единовременные комиссии (за рассмотрение, выдачу)
        - Ежемесячные/ежегодные комиссии
        - Страховки
        - Прочие обязательные платежи
        """,
        "loan_parameters": "Основные параметры кредита",
        "nominal_rate": "Номинальная ставка (% годовых)",
        "nominal_rate1": "Номинальная ставка",
        "loan_term_months": "Срок кредита (месяцев)",
        "additional_fees": "Дополнительные комиссии и платежи",
        "one_time_fees": "**Единовременные комиссии:**",
        "issue_fee": "Комиссия за выдачу (%)",
        "fixed_fee": "Фиксированная комиссия (₸)",
        "recurring_fees": "**Постоянные комиссии:**",
        "monthly_fee": "Ежемесячное обслуживание (₸)",
        "annual_fee": "Ежегодное обслуживание (₸)",
        "insurance_section": "**Страхование:**",
        "insurance": "Страховка (% от суммы)",
        "calculate_eps": "📈 Рассчитать ЭПС",
        "nominal_rate_label": "Номинальная ставка",
        "effective_rate": "Эффективная ставка (ЭПС)",
        "difference": "Разница",
        "from_nominal": "от номинальной",
        "payment_details": "📋 Детализация платежей",
        "month": "Месяц",
        "fees": "Комиссии",
        "total_payment_single": "Всего платеж",
        "overpayment_structure": "📊 Структура переплаты по кредиту",
        "fees_insurance": "Комиссии и страховки",
        "monthly_fees": "Ежемесячные комиссии",
        "annual_fees": "Ежегодные комиссии",
        "issue_fee_full": "Комиссия за выдачу",
        "issue_fee_fixed": "Фиксированная комиссия",
        "total_overpayment": "Общая переплата",
        "of_loan_amount": "от суммы кредита",
        "overpayment_distribution": "Распределение переплаты по кредиту",
        "no_additional_fees": "Дополнительных платежей нет",
        "total_overpayment": "**Общая переплата по кредиту:** {:,.0f} ₸ ({:.1f}% от суммы кредита)",
        "eps_conclusions": "💡 Выводы",
        "eps_warning": "**Внимание!** ЭПС значительно выше номинальной ставки. Реальная стоимость кредита на {:.2f}% выше заявленной.",
        "eps_recommendation": "**Рекомендации:** Рассмотрите другие предложения или попробуйте обсудить условия.",
        "eps_info_moderate": "ЭПС умеренно превышает номинальную ставку. Разница составляет {:.2f}%.",
        "eps_success": "Отличные условия! ЭПС практически соответствует номинальной ставке.",
        # Калькулятор вкладов
        "deposit_title": "Калькулятор вкладов и депозитов",
        "deposit_success": "Рассчитайте доходность вклада с учетом капитализации процентов",
        "deposit_parameters": "Параметры вклада",
        "deposit_amount": "Сумма вклада (₸)",
        "deposit_rate": "Процентная ставка (% годовых)",
        "deposit_term": "Срок вклада (месяцев)",
        "capitalization_type": "Тип капитализации",
        "capitalization_frequency": "Периодичность капитализации",
        "monthly_cap": "Ежемесячная",
        "quarterly_cap": "Ежеквартальная",
        "yearly_cap": "Ежегодная",
        "end_term": "В конце срока",
        "additional_conditions": "Дополнительные условия",
        "deposit_topup": "**Пополнение вклада:**",
        "monthly_topup": "Ежемесячное пополнение (₸)",
        "taxation": "**Налогообложение:**",
        "tax_free": "Не облагается налогом",
        "tax_rate": "Ставка налога (%)",
        "inflation": "**Учет инфляции:**",
        "include_inflation": "Учитывать инфляцию",
        "inflation_rate": "Прогноз инфляции (% годовых)",
        "calculate_deposit": "💸 Рассчитать доходность",
        "deposit_results": "📊 **Результаты расчета вклада**",
        "initial_amount": "Начальная сумма",
        "total_topup": "Сумма пополнений",
        "final_amount": "Итоговая сумма",
        "accrued_interest": "Начисленные проценты",
        "net_income": "Чистый доход",
        "tax_payment": "Налог к уплате",
        "inflation_analysis": "📊 Учет инфляции",
        "real_final_amount": "Реальная итоговая сумма",
        "real_income": "Реальный доход",
        "real_annual_yield": "Реальная годовая доходность",
        "nominal_yield": "Номинальная доходность",
        "positive_real_yield": "💰 **Положительная реальная доходность!** Ваш вклад сохраняет покупательную способность.",
        "low_real_yield": "⚠️ **Низкая реальная доходность.** Вклад лишь частично защищает от инфляции.",
        "negative_real_yield": "📉 **Отрицательная реальная доходность.** Покупательная способность вклада снижается.",
        "with_inflation": "с учетом инфляции",
        "without_inflation": "без учета инфляции",
        "annual_yield": "💫 Эффективная годовая доходность",
        "deposit_growth": "📈 Динамика роста вклада",
        "deposit_growth_month": "Рост вклада по месяцам",
        "month_label": "Месяц",
        "amount_label": "Сумма, ₸",
        "capitalization_comparison": "🔍 Сравнение типов капитализации",
        "income": "Доход",
        "deposit_recommendations": "💡 Рекомендации",
        "best_income_message": "**Наибольший доход** обеспечивает **{}** капитализация: **{:.0f} ₸**",
        "topup_benefit": "**Пополнение вклада** значительно увеличивает итоговую сумму благодаря сложным процентам.",
        # Общие
        "not_calculated": "Не может быть рассчитан",
        "not_paid_off": "Не окупится",
        "years": "лет",
        "footer": "Приложение размещено на Streamlit Cloud • Версия 2.0",
    },
}


def t(key):
    """Функция перевода"""
    return TRANSLATIONS[st.session_state.language].get(key, key)


# ============================================================================
# КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ
# ============================================================================

st.set_page_config(
    page_title="ФинКалькулятор",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Инициализация языка
if "language" not in st.session_state:
    st.session_state.language = "ru"

# ============================================================================
# БОКОВАЯ ПАНЕЛЬ С ПЕРЕКЛЮЧАТЕЛЕМ ЯЗЫКОВ
# ============================================================================

with st.sidebar:
    st.title(t("author"))

    # Переключатель языка
    language = st.radio(
        "Тіл / Язык:",
        ["Қазақша", "Русский"],
        index=1 if st.session_state.language == "ru" else 0,
        key="language_selector",
    )

    # Обновляем язык в session_state
    st.session_state.language = "kz" if language == "Қазақша" else "ru"

    st.write(t("author_name"))
    st.write(t("courses"))
    st.write(t("bot"))
    st.markdown("---")

# ============================================================================
# ЗАГОЛОВОК
# ============================================================================

st.title(t("title"))
st.markdown(f"*{t('subtitle')}*")

# ============================================================================
# ВКЛАДКИ
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([t("loans"), t("investment"), t("eps"), t("deposits")])

# ============================================================================
# 1. КАЛЬКУЛЯТОР КРЕДИТОВ
# ============================================================================

with tab1:
    st.header(t("calculate_schedule"))

    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input(
            t("loan_amount"), min_value=0.0, value=1000000.0, step=10000.0
        )
        interest_rate = st.number_input(
            t("interest_rate"), min_value=0.0, value=10.0, step=0.1
        )
    with col2:
        loan_term = st.number_input(t("loan_term"), min_value=1, value=5, step=1)
        payment_type = st.selectbox(
            t("payment_type"), [t("annuity"), t("differentiated")]
        )

    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term * 12

    def calculate_annuity(principal, rate, periods):
        if rate == 0:
            return principal / periods
        annuity_payment = (
            principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
        )
        return annuity_payment

    def generate_schedule(principal, rate, periods, p_type):
        schedule = []
        remaining_balance = principal

        if p_type == t("annuity"):
            payment = calculate_annuity(principal, rate, periods)
            for i in range(1, periods + 1):
                interest_payment = remaining_balance * rate
                principal_payment = payment - interest_payment
                remaining_balance -= principal_payment
                if i == periods:
                    principal_payment += remaining_balance
                    payment += remaining_balance
                    remaining_balance = 0
                schedule.append(
                    {
                        t("period"): i,
                        t("payment"): payment,
                        t("interest"): interest_payment,
                        t("principal"): principal_payment,
                        t("balance"): max(remaining_balance, 0),
                    }
                )
        else:
            principal_payment = principal / periods
            for i in range(1, periods + 1):
                interest_payment = remaining_balance * rate
                payment = principal_payment + interest_payment
                remaining_balance -= principal_payment
                schedule.append(
                    {
                        t("period"): i,
                        t("payment"): payment,
                        t("interest"): interest_payment,
                        t("principal"): principal_payment,
                        t("balance"): max(remaining_balance, 0),
                    }
                )

        return pd.DataFrame(schedule)

    if st.button(t("calculate_loan"), type="primary", key="loan_calc"):
        schedule_df = generate_schedule(
            loan_amount, monthly_rate, num_payments, payment_type
        )

        total_payment = schedule_df[t("payment")].sum()
        total_interest = schedule_df[t("interest")].sum()

        st.metric(t("total_payment"), f"{total_payment:,.2f} ₸")
        st.metric(t("total_interest"), f"{total_interest:,.2f} ₸")

        st.subheader(t("payment_schedule"))
        display_df = schedule_df.copy()
        for col in [t("payment"), t("interest"), t("principal"), t("balance")]:
            display_df[col] = display_df[col].map("{:,.2f} ₸".format)
        st.dataframe(display_df, use_container_width=True)

        st.subheader(t("payment_structure"))
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=schedule_df[t("period")],
                y=schedule_df[t("principal")],
                mode="lines",
                stackgroup="one",
                name=t("principal"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=schedule_df[t("period")],
                y=schedule_df[t("interest")],
                mode="lines",
                stackgroup="one",
                name=t("interest"),
            )
        )
        fig.update_layout(
            title=t("payment_dynamics"),
            xaxis_title=(
                "Номер платежа" if st.session_state.language == "ru" else "Төлем нөмірі"
            ),
            yaxis_title="Сумма, ₸" if st.session_state.language == "ru" else "Сома, ₸",
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# 2. ИНВЕСТИЦИОННЫЙ АНАЛИЗ
# ============================================================================

with tab2:
    st.header(t("investment"))

    discount_rate = (
        st.number_input(
            t("discount_rate"),
            min_value=0.0,
            value=10.0,
            step=0.1,
            key="disc_rate",
        )
        / 100
    )

    st.subheader(t("cash_flows"))
    st.caption(t("investment_caption"))

    initial_investment = st.number_input(
        t("initial_investment"), value=-1000000.0, step=10000.0
    )

    num_cash_flows = st.slider(
        t("analysis_periods"), min_value=1, max_value=20, value=5
    )

    cash_flows = [initial_investment]
    for i in range(1, num_cash_flows + 1):
        cf = st.number_input(
            f"{t('cash_flow_year')} {i} (₸)",
            value=300000.0,
            step=10000.0,
            key=f"cf_{i}",
        )
        cash_flows.append(cf)

    if st.button(t("analyze_project"), type="primary", key="inv_analysis"):
        cash_flows_array = np.array(cash_flows)

        npv = npf.npv(discount_rate, cash_flows_array)
        try:
            irr = npf.irr(cash_flows_array) * 100
        except:
            irr = t("not_calculated")

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

        col1, col2 = st.columns(2)
        with col1:
            st.metric(t("npv"), f"{npv:,.2f} ₸")
            if isinstance(irr, str):
                st.metric(t("irr"), irr)
            else:
                st.metric(t("irr"), f"{irr:.2f} %")
        with col2:
            st.metric(
                t("payback_period"),
                f"{pp_years:.2f} {t('years')}" if pp_years else t("not_paid_off"),
            )
            st.metric(
                t("discounted_payback"),
                f"{dpp_years:.2f} {t('years')}" if dpp_years else t("not_paid_off"),
            )

        st.subheader(t("cash_flow_diagram"))
        years = list(range(len(cash_flows_array)))
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=years,
                y=cash_flows_array,
                name=t("cash_flows"),
                marker_color=["red" if x < 0 else "green" for x in cash_flows_array],
            )
        )
        fig.add_trace(
            go.Scatter(
                x=years,
                y=cumulative_cf,
                mode="lines+markers",
                name=(
                    "Накопленный поток"
                    if st.session_state.language == "ru"
                    else "Жиналған ағын"
                ),
                line=dict(color="blue", width=3),
            )
        )
        fig.update_layout(
            title=t("cash_flows"),
            xaxis_title=(
                "Период (годы)"
                if st.session_state.language == "ru"
                else "Кезең (жылдар)"
            ),
            yaxis_title=(
                "Сумма, ₸" if st.session_state.language == "ru" else "Сома, ₸"
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(t("efficiency_conclusion"))
        if npv > 0:
            st.success(t("project_efficient"))
        else:
            st.error(t("project_inefficient"))

        if not isinstance(irr, str) and irr > discount_rate * 100:
            st.success(t("irr_higher").format(irr, discount_rate * 100))
        elif not isinstance(irr, str):
            st.warning(t("irr_lower").format(irr, discount_rate * 100))

# ============================================================================
# 3. ЭПС КАЛЬКУЛЯТОР
# ============================================================================

with tab3:
    st.header(t("eps_title"))
    st.info(t("eps_info"))

    with st.expander(t("eps_details")):
        st.markdown(t("eps_include"))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("loan_parameters"))
        eps_loan_amount = st.number_input(
            t("loan_amount"),
            min_value=0.0,
            value=2000000.0,
            step=100000.0,
            key="eps_loan",
        )
        eps_nominal_rate = st.number_input(
            t("nominal_rate"),
            min_value=0.0,
            value=15.0,
            step=0.1,
            key="eps_nominal",
        )
        eps_term = st.number_input(
            t("loan_term_months"), min_value=1, value=36, step=1, key="eps_term"
        )
        eps_payment_type = st.selectbox(
            t("payment_type"), [t("annuity"), t("differentiated")], key="eps_payment"
        )

    with col2:
        st.subheader(t("additional_fees"))

        st.write(t("one_time_fees"))
        eps_issue_fee = st.number_input(
            t("issue_fee"),
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="eps_issue",
        )
        eps_issue_fee_fixed = st.number_input(
            t("fixed_fee"),
            min_value=0.0,
            value=0.0,
            step=1000.0,
            key="eps_fixed",
        )

        st.write(t("recurring_fees"))
        eps_monthly_fee = st.number_input(
            t("monthly_fee"),
            min_value=0.0,
            value=500.0,
            step=500.0,
            key="eps_monthly",
        )
        eps_annual_fee = st.number_input(
            t("annual_fee"),
            min_value=0.0,
            value=0.0,
            step=1000.0,
            key="eps_annual",
        )

        st.write(t("insurance_section"))
        eps_insurance = st.number_input(
            t("insurance"),
            min_value=0.0,
            value=0.5,
            step=0.1,
            key="eps_insurance",
        )

    if st.button(t("calculate_eps"), type="primary", key="calc_eps"):
        cash_flows = []
        monthly_rate = eps_nominal_rate / 100 / 12

        initial_costs = 0

        if eps_issue_fee > 0:
            initial_costs += eps_loan_amount * eps_issue_fee / 100

        initial_costs += eps_issue_fee_fixed

        if eps_insurance > 0:
            initial_costs += eps_loan_amount * eps_insurance / 100

        cash_flows.append(eps_loan_amount - initial_costs)
        # Расчет ежемесячных платежей
        if eps_payment_type == t("annuity"):
            if monthly_rate == 0:
                monthly_payment = eps_loan_amount / eps_term
            else:
                monthly_payment = (
                    eps_loan_amount
                    * (monthly_rate * (1 + monthly_rate) ** eps_term)
                    / ((1 + monthly_rate) ** eps_term - 1)
                )
        else:
            principal_payment = eps_loan_amount / eps_term

        # Генерация ежемесячных платежей
        remaining_balance = eps_loan_amount

        for month in range(1, eps_term + 1):
            monthly_cash_outflow = 0

            if eps_payment_type == t("annuity"):
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
            annual_fee_to_add = (
                eps_annual_fee if month % 12 == 0 and eps_annual_fee > 0 else 0
            )
            monthly_cash_outflow += annual_fee_to_add

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
            st.metric(t("nominal_rate1"), f"{eps_nominal_rate:.2f}%")

        with col2:
            st.metric(
                t("effective_rate"),
                f"{eps_result:.2f}%",
                delta=f"{eps_result - eps_nominal_rate:.2f}%",
            )

        with col3:
            if eps_nominal_rate > 0:
                overpayment_ratio = (
                    (eps_result - eps_nominal_rate) / eps_nominal_rate * 100
                )
                st.metric(
                    t("difference"),
                    f"{eps_result - eps_nominal_rate:.2f}%",
                    delta=f"{overpayment_ratio:.1f}% {t("from_nominal")}",
                )

        # Детализация денежных потоков
        st.subheader(t("payment_details"))

        # Создаем таблицу с первыми 12 месяцами
        schedule_data = []
        remaining = eps_loan_amount

        for month in range(1, min(13, eps_term + 1)):
            if eps_payment_type == t("annuity"):
                interest = remaining * monthly_rate
                principal = monthly_payment - interest
                total_payment = monthly_payment
                remaining -= principal
            else:
                interest = remaining * monthly_rate
                principal = eps_loan_amount / eps_term
                total_payment = principal + interest
                remaining -= principal

            # РАСЧЕТ КОМИССИЙ ДЛЯ КАЖДОГО МЕСЯЦА
            monthly_fee_to_add = eps_monthly_fee
            annual_fee_to_add = (
                eps_annual_fee if month % 12 == 0 and eps_annual_fee > 0 else 0
            )
            total_fees = monthly_fee_to_add + annual_fee_to_add

            schedule_data.append(
                {
                    t("month"): month,
                    t("principal"): principal,
                    t("interest"): interest,
                    t("fees"): total_fees,
                    t("total_payment_single"): total_payment + total_fees,
                }
            )

        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(
            schedule_df.style.format(
                {
                    t("principal"): "{:,.2f} ₸",
                    t("interest"): "{:,.2f} ₸",
                    t("fees"): "{:,.2f} ₸",
                    t("total_payment_single"): "{:,.2f} ₸",
                }
            )
        )

        # График структуры переплаты
        st.subheader(t("overpayment_structure"))

        # Учитываем все комиссии
        # Общие проценты
        if eps_payment_type == t("annuity"):
            total_interest_paid = monthly_payment * eps_term - eps_loan_amount
        else:
            remaining_balance = eps_loan_amount
            total_interest_paid = 0
            principal_payment_diff = eps_loan_amount / eps_term

            for month in range(1, eps_term + 1):
                interest_payment = remaining_balance * monthly_rate
                total_interest_paid += interest_payment
                remaining_balance -= principal_payment_diff

        # Расчет ВСЕХ комиссий включая фиксированную
        total_monthly_fees = eps_monthly_fee * eps_term
        total_annual_fees = eps_annual_fee * (eps_term // 12)
        total_issue_fee_percent = (
            eps_loan_amount * eps_issue_fee / 100
        )  # Процентная комиссия
        total_issue_fee_fixed = eps_issue_fee_fixed  # Фиксированная комиссия
        total_insurance = eps_loan_amount * eps_insurance / 100

        labels = [
            t("interest"),
            t("monthly_fees"),
            t("annual_fees"),
            t("issue_fee_full"),
            t("issue_fee_fixed"),
            t("insurance"),
        ]

        values = [
            total_interest_paid,
            total_monthly_fees,
            total_annual_fees,
            total_issue_fee_percent,
            total_issue_fee_fixed,
            total_insurance,
        ]

        # Фильтруем нулевые значения
        filtered_labels = []
        filtered_values = []
        for label, value in zip(labels, values):
            if value > 0:
                filtered_labels.append(label)
                filtered_values.append(value)

        if filtered_values:
            fig_eps = px.pie(
                values=filtered_values,
                names=filtered_labels,
                title=t("overpayment_distribution"),
            )
            st.plotly_chart(fig_eps, use_container_width=True)
        else:
            st.info(t("no_additional_fees"))

        # Дополнительная информация об общей переплате
        total_overpayment = sum(values)
        st.info(
            f"{t('total_overpayment').format(total_overpayment, total_overpayment / eps_loan_amount * 100)}"
        )

        # Выводы и рекомендации
        st.subheader(t("eps_conclusions"))

        if eps_result > eps_nominal_rate + 2:
            st.warning(f"{t('eps_warning').format(eps_result - eps_nominal_rate)}")
            st.write(t("eps_recommendation"))
        elif eps_result > eps_nominal_rate + 0.5:
            st.info(f"{t('eps_info_moderate').format(eps_result - eps_nominal_rate)}")
        else:
            st.success(f"{t('eps_success')}")

# ============================================================================
# 4. НОВАЯ ФУНКЦИЯ: КАЛЬКУЛЯТОР ВКЛАДОВ С КАПИТАЛИЗАЦИЕЙ
# ============================================================================

with tab4:
    st.header(t("deposit_title"))
    st.success(t("deposit_success"))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t("deposit_parameters"))
        deposit_amount = st.number_input(
            t("deposit_amount"),
            min_value=1000.0,
            value=100000.0,
            step=10000.0,
            key="deposit_amount",
        )
        deposit_rate = st.number_input(
            t("deposit_rate"),
            min_value=0.1,
            value=8.0,
            step=0.1,
            key="deposit_rate",
        )
        deposit_term = st.number_input(
            t("deposit_term"), min_value=1, value=12, step=1, key="deposit_term"
        )

        st.subheader(t("capitalization_type"))
        capitalization_type = st.selectbox(
            t("capitalization_frequency"),
            [t("monthly_cap"), t("quarterly_cap"), t("yearly_cap"), t("end_term")],
            key="cap_type",
        )

    with col2:
        st.subheader(t("additional_conditions"))

        # Пополнение вклада
        st.write(t("deposit_topup"))
        monthly_topup = st.number_input(
            t("monthly_topup"),
            min_value=0.0,
            value=0.0,
            step=1000.0,
            key="monthly_topup",
        )

        # Налоги
        st.write(t("taxation"))
        tax_free = st.checkbox(t("tax_free"), value=True, key="tax_free")
        if not tax_free:
            tax_rate = st.number_input(
                t("tax_rate"), min_value=0.0, value=10.0, step=0.1, key="tax_rate"
            )

        # Инфляция
        st.write(t("inflation"))
        include_inflation = st.checkbox(
            t("include_inflation"), value=False, key="include_inflation"
        )
        if include_inflation:
            inflation_rate = st.number_input(
                t("inflation_rate"),
                min_value=0.0,
                value=5.0,
                step=0.1,
                key="inflation_rate",
            )

    # Расчет вклада
    if st.button(t("calculate_deposit"), type="primary", key="calc_deposit"):

        # Определяем периодичность капитализации
        if capitalization_type == t("monthly_cap"):
            periods_per_year = 12
        elif capitalization_type == t("quarterly_cap"):
            periods_per_year = 4
        elif capitalization_type == t("yearly_cap"):
            periods_per_year = 1
        else:  # В конце срока
            periods_per_year = 1

        # Капитализация в конце срока только для соответствующего типа
        capitalization_at_end = capitalization_type == t("end_term")

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

        # Отображение результатов
        st.success(t("deposit_results"))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(t("initial_amount"), f"{deposit_amount:,.0f} ₸")
            st.metric(t("total_topup"), f"{monthly_topup * deposit_term:,.0f} ₸")

        with col2:
            st.metric(t("final_amount"), f"{final_amount:,.0f} ₸")
            st.metric(t("accrued_interest"), f"{total_interest:,.0f} ₸")

        with col3:
            st.metric(t("net_income"), f"{net_interest:,.0f} ₸")
            if tax_amount > 0:
                st.metric(t("tax_payment"), f"{tax_amount:,.0f} ₸")

        # Годовая доходность
        annual_yield = (net_interest / deposit_amount) * (12 / deposit_term) * 100
        st.metric(t("annual_yield"), f"{annual_yield:.2f}%")

        # Учет инфляции
        if include_inflation and inflation_rate > 0:
            st.markdown("---")
            st.success(t("inflation_analysis"))

            inflation_factor = (1 + inflation_rate / 100) ** (deposit_term / 12)
            real_final_amount = net_final_amount / inflation_factor
            real_income = (
                real_final_amount - deposit_amount - (monthly_topup * deposit_term)
            )
            real_annual_yield = (
                (real_income / deposit_amount) * (12 / deposit_term) * 100
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    t("real_final_amount"),
                    f"{real_final_amount:,.0f} ₸",
                    delta=f"-{(final_amount - real_final_amount):,.0f} ₸",
                )

            with col2:
                st.metric(
                    t("real_income"),
                    f"{real_income:,.0f} ₸",
                    delta=f"-{(net_interest - real_income):,.0f} ₸",
                )

            with col3:
                st.metric(
                    t("real_annual_yield"),
                    f"{real_annual_yield:.2f}%",
                    delta=f"-{(annual_yield - real_annual_yield):.2f}%",
                )

            # Визуализация
            fig_inflation = go.Figure()

            fig_inflation.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=real_annual_yield,
                    number={"suffix": "%"},
                    delta={
                        "reference": annual_yield,
                        "relative": False,
                        "valueformat": ".2f",
                        "suffix": "%",
                    },
                    title={
                        "text": f"{t('real_annual_yield')}<br><span style='font-size:0.8em;color:gray'>{t('with_inflation')}</span>"
                    },
                    domain={"row": 0, "column": 0},
                )
            )

            fig_inflation.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=annual_yield,
                    number={"suffix": "%"},
                    delta={
                        "reference": real_annual_yield,
                        "relative": False,
                        "valueformat": ".2f",
                        "suffix": "%",
                    },
                    title={
                        "text": f"{t('nominal_yield')}<br><span style='font-size:0.8em;color:gray'>{t('without_inflation')}</span>"
                    },
                    domain={"row": 0, "column": 1},
                )
            )

            fig_inflation.update_layout(
                grid={"rows": 1, "columns": 2, "pattern": "independent"}
            )
            st.plotly_chart(fig_inflation, use_container_width=True)

            # Вывод о реальной доходности
            if real_annual_yield > 0:
                st.success(t("positive_real_yield"))
            elif real_annual_yield > -2:
                st.warning(t("low_real_yield"))
            else:
                st.error(t("negative_real_yield"))

        # График роста вклада
        st.subheader(t("deposit_growth"))

        # Строим график по месяцам
        months = list(range(0, deposit_term + 1))
        amounts = [deposit_amount]
        current_amount = deposit_amount
        monthly_rate = deposit_rate / 100 / 12

        for month in range(1, deposit_term + 1):
            if capitalization_type == t("monthly_cap") or capitalization_at_end:
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
            title=t("deposit_growth_month"),
            labels={"x": t("month_label"), "y": t("amount_label")},
        )
        fig_deposit.update_traces(line=dict(color="green", width=3))
        st.plotly_chart(fig_deposit, use_container_width=True)

        # Сравнение с разными типами капитализации
        st.subheader(t("capitalization_comparison"))

        cap_types = [
            t("monthly_cap"),
            t("quarterly_cap"),
            t("yearly_cap"),
            t("end_term"),
        ]
        results = []

        for cap_type in cap_types:
            if cap_type == t("monthly_cap"):
                result = deposit_amount * (1 + deposit_rate / 100 / 12) ** deposit_term
            elif cap_type == t("quarterly_cap"):
                result = deposit_amount * (1 + deposit_rate / 100 / 4) ** (
                    deposit_term / 3
                )
            elif cap_type == t("yearly_cap"):
                result = deposit_amount * (1 + deposit_rate / 100) ** (
                    deposit_term / 12
                )
            else:  # В конце срока
                result = deposit_amount * (1 + deposit_rate / 100 * deposit_term / 12)

            results.append(result)

        comparison_df = pd.DataFrame(
            {
                t("capitalization_type"): cap_types,
                t("final_amount"): results,
                t("income"): [x - deposit_amount for x in results],
            }
        )

        st.dataframe(
            comparison_df.style.format(
                {t("final_amount"): "{:,.2f} ₸", t("income"): "{:,.2f} ₸"}
            )
        )

        # Рекомендации
        st.subheader(t("deposit_recommendations"))

        best_cap_type = cap_types[np.argmax(results)]
        best_income = max(results) - deposit_amount

        st.info(f"{t('best_income_message').format(best_cap_type, best_income)}")

        if monthly_topup > 0:
            st.success(t("topup_benefit"))


# ============================================================================
# ФУТЕР
# ============================================================================

st.markdown("---")
st.markdown(t("author"))
st.write(t("author_name"))
st.write(t("courses"))
st.write(t("bot"))
st.write(t("contacts"))
st.markdown("---")

footer_texts = {
    "kz": "Қаржы калькуляторы • 2.0 нұсқасы • © 2025",
    "ru": "Финансовый калькулятор • Версия 2.0 • © 2025",
}

st.markdown(
    f"<div style='text-align: center; color: gray;'>{footer_texts[st.session_state.language]}</div>",
    unsafe_allow_html=True,
)

# ЗАПУСК ПРИЛОЖЕНИЯ

if __name__ == "__main__":
    # Дополнительная инициализация
    pass